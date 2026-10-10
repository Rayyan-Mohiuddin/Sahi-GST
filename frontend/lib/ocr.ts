import type {OcrLine} from './image-ocr';
export type OCRWorker = { recognize: (file: File) => Promise<{data: {text: string; confidence?:number; lines?:{text:string;confidence:number;bbox?:{x0:number;y0:number;x1:number;y1:number}}[]}}> ; terminate: () => Promise<unknown> };
type Options = {signal: AbortSignal; createWorker: () => Promise<OCRWorker>; timeoutMs?: number};

/** Bounded OCR lifecycle; cancel/timeout never publishes a late result. */
export async function readInvoice(file: File, {signal, createWorker, timeoutMs = 90000}: Options): Promise<string> {
  return (await readInvoiceDetailed(file,{signal,createWorker,timeoutMs})).text;
}
export async function readInvoiceDetailed(file: File, {signal, createWorker, timeoutMs = 90000}: Options): Promise<{text:string;confidence:number;lines:OcrLine[]}> {
  if (signal.aborted) throw new Error('Scan cancelled. You can retry or enter fields manually.');
  let worker: OCRWorker | undefined;
  let stopped = false;
  let rejectStop: (error: Error) => void = () => {};
  const terminate = async () => { const active = worker; worker = undefined; if(active) await active.terminate().catch(()=>{}); };
  const stop = (message: string) => {stopped = true; rejectStop(new Error(message)); void terminate();};
  const cancelled = () => stop('Scan cancelled. You can retry or enter fields manually.');
  const interrupted = new Promise<never>((_, reject) => {rejectStop = reject;});
  signal.addEventListener('abort', cancelled, {once:true});
  const timer = setTimeout(()=>stop('OCR took too long. Check your connection, retry with a clearer image, or enter fields manually.'), timeoutMs);
  const work = (async()=>{
    worker = await createWorker();
    if(stopped){await terminate();throw new Error('Scan stopped.');}
    const {data} = await worker.recognize(file);
    const lines=(data.lines||[]).map(line=>({text:line.text,confidence:line.confidence,bbox:line.bbox?{x:line.bbox.x0,y:line.bbox.y0,width:line.bbox.x1-line.bbox.x0,height:line.bbox.y1-line.bbox.y0}:undefined}));
    return {text:data.text,confidence:data.confidence??(lines.length?Math.round(lines.reduce((sum,line)=>sum+line.confidence,0)/lines.length):0),lines};
  })();
  try { return await Promise.race([work, interrupted]); }
  finally { clearTimeout(timer); signal.removeEventListener('abort', cancelled); stopped = true; await terminate(); }
}
