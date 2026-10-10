import {createWorker} from 'tesseract.js';
import {readInvoice} from '../lib/ocr.ts';
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const fixtures=JSON.parse(await readFile(path.join(root,'tests/ocr_images/manifest.json'),'utf8'));
const output=path.join(root,'.local/ocr-evaluation');
await mkdir(path.join(output,'cache'),{recursive:true});
const records=[];
for(const fixture of fixtures){
  const start=Date.now();
  try{
    const text=await readInvoice(path.join(root,'tests/ocr_images',fixture.image),{
      signal:new AbortController().signal,
      createWorker:()=>createWorker('eng',1,{cachePath:path.join(output,'cache')}),
    });
    records.push({name:fixture.name,text,elapsed_ms:Date.now()-start});
    console.log(`${fixture.name}: OCR completed in ${Date.now()-start} ms`);
  }catch(error){records.push({name:fixture.name,error:error.message,elapsed_ms:Date.now()-start});console.log(`${fixture.name}: ${error.message}`);}
}
await writeFile(path.join(output,'ocr-output.json'),JSON.stringify(records,null,2));
console.log('Synthetic OCR outputs saved. Run scripts/evaluate_ocr_fields.py to measure parser results.');
