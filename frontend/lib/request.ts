/** Bound the whole upload/response wait, including stalled mobile connections. */
export async function requestJSON(path:string, options:RequestInit={}, timeoutMs=45000){
 const controller=new AbortController();
 const cancel=()=>controller.abort();
 options.signal?.addEventListener('abort',cancel,{once:true});
 if(options.signal?.aborted)controller.abort();
 let timedOut=false;
 const timer=setTimeout(()=>{timedOut=true;controller.abort();},timeoutMs);
 try{
  const response=await fetch(path,{...options,signal:controller.signal});
  const data=await response.json().catch(()=>({error:'The server returned an unreadable response. Retry or use local OCR.'}));
  if(!response.ok||data.error)throw new Error(data.error||'Request failed. Retry or use local OCR.');
  return data;
 }catch(error){
  if(timedOut)throw new Error('The request took too long on this connection. Please retry once or use local OCR backup.');
  throw error;
 }finally{clearTimeout(timer);options.signal?.removeEventListener('abort',cancel);}
}
