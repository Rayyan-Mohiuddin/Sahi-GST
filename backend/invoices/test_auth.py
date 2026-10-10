from django.test import TestCase

class AccountPageTests(TestCase):
    def test_account_forms_use_branded_layout(self):
        for route in ['/accounts/login/', '/accounts/signup/']:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'allauth/layouts/base.html')
            self.assertContains(response, '<style>')
            self.assertContains(response, 'Back to workspace')
            self.assertContains(response, 'csrfmiddlewaretoken')

    def test_signup_login_logout(self):
        response = self.client.post('/accounts/signup/', {'username': 'release-test', 'password1': 'Invoice-Test-9472!', 'password2': 'Invoice-Test-9472!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.get('/api/session/').json()['authenticated'])
        self.client.post('/accounts/logout/')
        self.assertFalse(self.client.get('/api/session/').json()['authenticated'])
        response = self.client.post('/accounts/login/', {'login': 'release-test', 'password': 'Invoice-Test-9472!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.get('/api/session/').json()['authenticated'])
