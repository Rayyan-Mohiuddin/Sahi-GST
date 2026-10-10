import test from 'node:test';import assert from 'node:assert/strict';import {pageLimitError} from '../lib/invoice-pages.ts';
const page=(size)=>({size,type:'image/jpeg'});
test('supports several pages while limiting total size',()=>{assert.equal(pageLimitError([page(1000),page(2000)]),null);assert.match(pageLimitError(Array(6).fill(page(1000))),/1–5/);assert.match(pageLimitError([page(5*1024*1024),page(5*1024*1024),page(1)]),/combined/);});
test('rejects unsupported image formats',()=>{assert.match(pageLimitError([{size:20,type:'image/heic'}]),/JPEG/);});
test('Vercel-safe aggregate boundary',()=>{assert.equal(pageLimitError([page(3*1024*1024)]),null);assert.match(pageLimitError([page(3*1024*1024),page(1)]),/combined/);});
