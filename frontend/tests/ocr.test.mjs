import test from 'node:test';
import assert from 'node:assert/strict';
import {readInvoice} from '../lib/ocr.ts';

test('returns recognized text and releases worker', async()=>{
  let terminated=0;
  const text=await readInvoice({}, {signal:new AbortController().signal,createWorker:async()=>({recognize:async()=>({data:{text:'Invoice'}}),terminate:async()=>{terminated++;}})});
  assert.equal(text,'Invoice');assert.equal(terminated,1);
});
test('timeout releases a stuck worker',async()=>{
  let terminated=0;
  await assert.rejects(readInvoice({}, {signal:new AbortController().signal,timeoutMs:20,createWorker:async()=>({recognize:()=>new Promise(()=>{}),terminate:async()=>{terminated++;}})}),/too long/);
  assert.equal(terminated,1);
});
test('cancel during loading releases a worker that arrives later',async()=>{
  const controller=new AbortController();let release;let terminated=0;
  const creation=new Promise(resolve=>{release=resolve;});
  const task=readInvoice({}, {signal:controller.signal,createWorker:()=>creation});
  controller.abort();await assert.rejects(task,/cancelled/);
  release({recognize:async()=>{throw new Error('Must not recognize after cancellation');},terminate:async()=>{terminated++;}});
  await new Promise(resolve=>setImmediate(resolve));assert.equal(terminated,1);
});
test('cancel while recognizing does not return the late result',async()=>{
  const controller=new AbortController();let complete;let terminated=0;
  const recognition=new Promise(resolve=>{complete=resolve;});
  const task=readInvoice({}, {signal:controller.signal,createWorker:async()=>({recognize:()=>recognition,terminate:async()=>{terminated++;}})});
  await new Promise(resolve=>setImmediate(resolve));controller.abort();await assert.rejects(task,/cancelled/);
  complete({data:{text:'Late output'}});await new Promise(resolve=>setImmediate(resolve));assert.equal(terminated,1);
});
