import test from 'node:test';
import assert from 'node:assert/strict';
import {scoreImageQuality} from '../lib/image-ocr.ts';

function image(width,height,value){const data=new Uint8ClampedArray(width*height*4);for(let i=0;i<data.length;i+=4)data.set([value,value,value,255],i);return {width,height,data};}
test('flags a dark, flat camera image for retake',()=>{
  const quality=scoreImageQuality(image(24,24,18));
  assert.ok(quality.warnings.some(message=>message.includes('dark')));
  assert.ok(quality.warnings.some(message=>message.includes('blurred')));
});
test('flags glare-heavy photos',()=>{
  const quality=scoreImageQuality(image(24,24,255));
  assert.ok(quality.warnings.some(message=>message.includes('glare')));
});
test('measures a strongly skewed text-like baseline',()=>{
  const source=image(80,50,230);
  for(let x=0;x<75;x++){const y=Math.floor(8+x*.14);const i=(y*80+x)*4;source.data.set([15,15,15,255],i);}
  const quality=scoreImageQuality(source);
  assert.ok(Math.abs(quality.skew)>=3);
  assert.ok(quality.warnings.some(message=>message.includes('skewed')));
});
