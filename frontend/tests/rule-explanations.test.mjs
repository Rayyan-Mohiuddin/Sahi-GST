import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {RULE_MESSAGES,ruleExplanations} from '../lib/rule-explanations.ts';
test('all bundled templates match backend wording',()=>{
 const source=fs.readFileSync(new URL('../../backend/invoices/languages.py',import.meta.url),'utf8');
 for(const language of Object.values(RULE_MESSAGES))for(const message of Object.values(language))assert.ok(source.includes(message));
});
test('Hindi and Telugu explain issues immediately with no API or key',()=>{
 const findings=[{id:'total',rule_id:'M04',status:'issue'},{id:'unknown',rule_id:'UNKNOWN',status:'review'},{id:'pass',rule_id:'M02',status:'pass'}];
 for(const lang of ['hi','te']){
  const result=ruleExplanations(findings,lang);
  assert.deepEqual(result.map(f=>f.id),['total','unknown']);
  assert.equal(result[0].text,RULE_MESSAGES[lang].M04);
  assert.equal(result[1].text,RULE_MESSAGES[lang].default);
  assert.ok(result.every(f=>f.source==='rule'));
 }
 assert.match(ruleExplanations(findings,'hi')[0].text,/[\u0900-\u097f]/);
 assert.match(ruleExplanations(findings,'te')[0].text,/[\u0c00-\u0c7f]/);
});
