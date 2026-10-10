'use client';
import {Camera,UploadCloud} from 'lucide-react';
import {useRef,useImperativeHandle,forwardRef} from 'react';
export type UploadPickerHandle={openFiles:()=>void};
export const InvoiceUploadPicker=forwardRef<UploadPickerHandle,{busy:boolean;hasFile:boolean;onFile:(file?:File)=>void}>(({busy,hasFile,onFile},ref)=>{
  const files=useRef<HTMLInputElement>(null),camera=useRef<HTMLInputElement>(null);
  useImperativeHandle(ref,()=>({openFiles:()=>{if(!busy)files.current?.click();}}),[busy]);
  const pick=(event:React.ChangeEvent<HTMLInputElement>)=>{const file=event.target.files?.[0];event.target.value='';if(file)onFile(file);};
  return <div className="upload-actions">
    <input ref={files} disabled={busy} type="file" accept="image/jpeg,image/png" className="sr-only" aria-label="Select invoice image from files" onChange={pick}/>
    <input ref={camera} disabled={busy} type="file" accept="image/*" capture="environment" className="sr-only" aria-label="Capture invoice with camera" onChange={pick}/>
    <button className="button secondary full" disabled={busy} onClick={()=>files.current?.click()}><UploadCloud size={16}/>{hasFile?'Choose another file':'Choose from files'}</button>
    <button className="button secondary full" disabled={busy} onClick={()=>camera.current?.click()}><Camera size={16}/>Take a photo</button>
    <small>Files opens the system picker; Camera requests photo capture. Available choices depend on your browser. Use a clear JPEG/PNG.</small>
  </div>;
});
InvoiceUploadPicker.displayName='InvoiceUploadPicker';
