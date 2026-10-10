import test from 'node:test';
import assert from 'node:assert/strict';
import {attachWorkspaceHistory} from '../lib/workspace-history.ts';
function browser(url='https://example.test/'){
  let index=0;const entries=[{state:{existingNextState:true},url}],listeners=new Set();
  const port={location:{href:url},addEventListener:(_,fn)=>listeners.add(fn),removeEventListener:(_,fn)=>listeners.delete(fn)};
  port.history={get state(){return entries[index].state;},replaceState(state,_,url){entries[index]={state,url};port.location.href=url;},pushState(state,_,url){entries.splice(index+1);entries.push({state,url});index++;port.location.href=url;},back(){if(index){index--;port.location.href=entries[index].url;listeners.forEach(fn=>fn());}},forward(){if(index+1<entries.length){index++;port.location.href=entries[index].url;listeners.forEach(fn=>fn());}}};
  return {port,depth:()=>entries.length,index:()=>index};
}
test('Back closes review and preserves page; Forward reopens it',()=>{
  const b=browser();let state;const nav=attachWorkspaceHistory(b.port,s=>state=s);
  nav.setNav('invoices');nav.setModal(true);assert.equal(state.modal,true);
  b.port.history.back();assert.deepEqual(state,{nav:'invoices',modal:false});
  b.port.history.forward();assert.equal(state.modal,true);assert.equal(b.port.history.state.existingNextState,true);
});
test('close consumes the dialog entry; repeated open does not duplicate it',()=>{
  const b=browser();let state;const nav=attachWorkspaceHistory(b.port,s=>state=s);
  nav.setModal(true);nav.setModal(true);assert.equal(b.depth(),2);
  nav.setModal(false);assert.equal(b.index(),0);assert.equal(state.modal,false);
});
test('valid URL view restores without reopening an empty review',()=>{
  const b=browser('https://example.test/?view=reports');let state;const nav=attachWorkspaceHistory(b.port,s=>state=s);
  assert.deepEqual(state,{nav:'reports',modal:false});nav.setNav('settings');b.port.history.back();assert.equal(state.nav,'reports');
});
test('disposal removes the listener',()=>{
  const b=browser();let calls=0;const nav=attachWorkspaceHistory(b.port,()=>calls++);
  nav.setModal(true);nav.dispose();const before=calls;b.port.history.back();assert.equal(calls,before);
});
