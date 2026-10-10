import io
import json
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings

from .gemini import provider_failure, request_json
from .test_ai_pages import image_bytes


def http_error(code, status='UNAVAILABLE'):
    body = json.dumps({'error': {'status': status, 'message': 'private invoice and key',
                                'details': [{'secret': 'private invoice and key'}]}}).encode()
    return HTTPError('https://example.invalid/?key=private', code, 'private invoice and key',
                     {}, io.BytesIO(body))


def success():
    return io.BytesIO(json.dumps({'candidates': [{'finishReason': 'STOP', 'content': {
        'parts': [{'text': '{"ok": true}'}]}}]}).encode())


@override_settings(GEMINI_API_KEY='private-key', GEMINI_MODEL='gemini-2.5-flash')
class ProviderTransportTests(SimpleTestCase):
    @override_settings(GEMINI_MODEL='gemini-3.8-flash')
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_38_request_supports_images_and_schema_without_legacy_parameters(self, send):
        send.return_value = success()
        schema = {'type': 'OBJECT', 'properties': {'ok': {'type': 'BOOLEAN'}}}
        self.assertEqual(request_json('read invoice', [(b'example-image', 'image/png')], schema), {'ok': True})
        request = send.call_args.args[0]
        self.assertTrue(request.full_url.endswith('/gemini-3.8-flash:generateContent'))
        payload = json.loads(request.data)
        config = payload['generationConfig']
        self.assertEqual(config['thinkingConfig'], {'thinkingLevel': 'low'})
        self.assertEqual(config['responseSchema'], schema)
        self.assertEqual(config['responseMimeType'], 'application/json')
        self.assertNotIn('temperature', config)
        self.assertEqual(payload['contents'][0]['parts'][1]['inlineData']['mimeType'], 'image/png')

    @patch('invoices.gemini.urllib.request.urlopen')
    def test_25_request_retains_supported_budget_and_temperature(self, send):
        send.return_value = success()
        request_json('read invoice')
        config = json.loads(send.call_args.args[0].data)['generationConfig']
        self.assertEqual(config['thinkingConfig'], {'thinkingBudget': 0})
        self.assertEqual(config['temperature'], 0)

    @patch('invoices.gemini.time.sleep')
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_transient_failure_recovers_using_same_request(self, send, sleep):
        failure = http_error(503)
        send.side_effect = [failure, success()]
        with self.assertLogs('invoices.gemini', level='WARNING') as logs:
            self.assertEqual(request_json('private invoice'), {'ok': True})
        self.assertEqual(send.call_count, 2)
        self.assertIs(send.call_args_list[0].args[0], send.call_args_list[1].args[0])
        self.assertTrue(failure.fp.closed)
        self.assertEqual(sleep.call_count, 1)
        self.assertNotIn('private', '\n'.join(logs.output))

    @patch('invoices.gemini.time.sleep')
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_permanent_and_quota_errors_are_not_retried(self, send, sleep):
        for code in (400, 401, 403, 404, 429, 418):
            with self.subTest(code=code):
                send.reset_mock()
                failure = http_error(code)
                send.side_effect = failure
                with self.assertRaises(HTTPError):
                    request_json('private invoice')
                send.assert_called_once()
                failure.close()
        sleep.assert_not_called()

    @patch('invoices.gemini.time.sleep')
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_retries_stop_after_second_failure(self, send, sleep):
        for code in (500, 502, 503, 504):
            with self.subTest(code=code):
                send.reset_mock()
                send.side_effect = [http_error(code), http_error(code)]
                with self.assertLogs('invoices.gemini', level='WARNING'):
                    with self.assertRaises(HTTPError) as caught:
                        request_json('private invoice')
                self.assertEqual(send.call_count, 2)
                caught.exception.close()

    @patch('invoices.gemini.time.sleep')
    @patch('invoices.gemini.time.monotonic', side_effect=[0, 0, 44])
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_no_retry_when_request_budget_is_spent(self, send, monotonic, sleep):
        send.side_effect = http_error(503)
        with self.assertRaises(HTTPError) as caught:
            request_json('private invoice')
        send.assert_called_once()
        sleep.assert_not_called()
        caught.exception.close()

    @patch('invoices.gemini.time.sleep')
    @patch('invoices.gemini.time.monotonic', side_effect=[0, 0, 35, 36.5])
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_retry_timeout_uses_remaining_budget(self, send, monotonic, sleep):
        send.side_effect = [http_error(503), success()]
        with self.assertLogs('invoices.gemini', level='WARNING'):
            request_json('private invoice')
        self.assertEqual(send.call_args.kwargs['timeout'], 8.5)

    @patch('invoices.gemini.urllib.request.urlopen')
    def test_invalid_success_payload_is_not_retried(self, send):
        send.return_value = io.BytesIO(b'not JSON')
        with self.assertRaises(ValueError):
            request_json('private invoice')
        send.assert_called_once()

    def test_diagnostic_categories_never_expose_exception_text(self):
        for exc, expected in [(TimeoutError('private-key'), 'timeout'),
                              (URLError(TimeoutError('private-key')), 'timeout'),
                              (URLError('private-key'), 'connection_error'),
                              (ValueError('private invoice'), 'invalid_response')]:
            with self.subTest(expected=expected), self.assertLogs('invoices.gemini') as logs:
                data = provider_failure(exc, 'extract')
            self.assertEqual(data['error_code'], expected)
            self.assertIn(data['reference'], '\n'.join(logs.output))
            self.assertNotIn('private', json.dumps(data) + '\n'.join(logs.output))


@override_settings(GEMINI_API_KEY='private-key', GEMINI_MODEL='gemini-2.5-flash', GEMINI_FREE_TIER_CONFIRMED=True)
class ProviderEndpointTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_user(username='provider-test'))

    @patch('invoices.gemini.time.sleep')
    @patch('invoices.gemini.urllib.request.urlopen')
    def test_upstream_status_and_reference_survive_endpoint_mapping(self, send, sleep):
        send.side_effect = [http_error(503), http_error(503)]
        with self.assertLogs('invoices.gemini', level='WARNING') as logs:
            response = self.client.post('/api/extract/', {
                'file': SimpleUploadedFile('invoice.png', image_bytes(), content_type='image/png'),
                'consent': 'true',
            })
        data = response.json()
        self.assertEqual(response.status_code, 502)
        self.assertEqual(data['provider_http_status'], 503)
        self.assertEqual(data['provider_status'], 'UNAVAILABLE')
        self.assertIn('Provider HTTP 503', data['error'])
        self.assertIn(data['reference'], '\n'.join(logs.output))
        self.assertNotIn('private', response.content.decode() + '\n'.join(logs.output))

    def test_non_json_or_untrusted_provider_status_is_not_exposed(self):
        for body in (b'<html>private-key</html>', b'{"error":{"status":"private-key"}}',
                     b'{"error":{"status":[]}}', b'[]', b'{"error":null}'):
            with self.subTest(body=body):
                exc = HTTPError('https://example.invalid', 500, 'private-key', {}, io.BytesIO(body))
                with self.assertLogs('invoices.gemini') as logs:
                    data = provider_failure(exc, 'extract')
                self.assertIsNone(data['provider_status'])
                self.assertNotIn('private', json.dumps(data) + '\n'.join(logs.output))
                self.assertTrue(exc.fp.closed)
