import test from 'node:test';
import assert from 'node:assert/strict';
import {requestJSON} from '../lib/request.ts';
test('stalled mobile request releases with actionable timeout',async()=>{
 const original=globalThis.fetch;
 globalThis.fetch=async(_url,{signal})=>new Promise((resolve,reject)=>signal.addEventListener('abort',()=>reject(new Error('aborted'))));
 try{await assert.rejects(requestJSON('/api/extract/',{},10),/took too long/);}finally{globalThis.fetch=original;}
});
test('invalid success body cannot silently masquerade as extraction',async()=>{
 const original=globalThis.fetch;
 globalThis.fetch=async()=>({ok:true,json:async()=>{throw new Error('HTML');}});
 try{await assert.rejects(requestJSON('/api/extract/'),/unreadable response/);}finally{globalThis.fetch=original;}
});
