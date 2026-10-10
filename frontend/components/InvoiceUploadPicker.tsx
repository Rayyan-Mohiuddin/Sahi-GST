'use client';
import {Camera,UploadCloud,X} from 'lucide-react';
import {useRef,useImperativeHandle,forwardRef,useState,useEffect} from 'react';
export type UploadPickerHandle={openFiles:()=>void};
export const InvoiceUploadPicker=forwardRef<UploadPickerHandle,{busy:boolean;hasFile:boolean;onFiles:(files:File[],append?:boolean)=>void}>(({busy,hasFile,onFiles},ref)=>{
  const files=useRef<HTMLInputElement>(null),video=useRef<HTMLVideoElement>(null),stream=useRef<MediaStream|null>(null),mounted=useRef(true),request=useRef(0);
  const [cameraOpen,setCameraOpen]=useState(false),[ready,setReady]=useState(false),[error,setError]=useState('');
  const stop=()=>{request.current++;stream.current?.getTracks().forEach(track=>track.stop());stream.current=null;setCameraOpen(false);setReady(false);};
  useEffect(()=>{mounted.current=true;return()=>{mounted.current=false;request.current++;stream.current?.getTracks().forEach(track=>track.stop());};},[]);
  useEffect(()=>{if(ready&&video.current&&stream.current){video.current.srcObject=stream.current;void video.current.play().catch(()=>setError('Camera preview could not start. Try another browser or select a file.'));}},[ready]);
  const openCamera=async()=>{
    setError('');setCameraOpen(true);setReady(false);const version=++request.current;
    try{if(!navigator.mediaDevices?.getUserMedia)throw new Error('Camera requires HTTPS/localhost and a supported browser. Select a file instead.');
      const capture=await navigator.mediaDevices.getUserMedia({video:{facingMode:{ideal:'environment'},width:{ideal:1920},height:{ideal:1080}},audio:false});
      if(!mounted.current||version!==request.current){capture.getTracks().forEach(track=>track.stop());return;}
      stream.current=capture;setReady(true);
    }catch(e){if(mounted.current&&version===request.current)setError((e as Error).name==='NotAllowedError'?'Camera permission was denied. Allow it in browser settings or select a file.':(e as Error).message);}
  };
  const takePhoto=()=>{if(!video.current?.videoWidth)return;const version=request.current;const canvas=document.createElement('canvas');canvas.width=video.current.videoWidth;canvas.height=video.current.videoHeight;canvas.getContext('2d')!.drawImage(video.current,0,0);canvas.toBlob(blob=>{if(blob&&mounted.current&&version===request.current){onFiles([new File([blob],`invoice-photo-${Date.now()}.jpg`,{type:'image/jpeg'})],true);stop();}},'image/jpeg',.94);};
  useImperativeHandle(ref,()=>({openFiles:()=>{if(!busy&&!cameraOpen)files.current?.click();}}),[busy,cameraOpen]);
  const pick=(event:React.ChangeEvent<HTMLInputElement>)=>{const picked=Array.from(event.target.files||[]);event.target.value='';if(picked.length)onFiles(picked,true);};
  return <div className="upload-actions">
    <input ref={files} disabled={busy} multiple type="file" accept="image/jpeg,image/png,application/pdf" className="sr-only" aria-label="Select invoice pages or a PDF" onChange={pick}/>
    <button className="button secondary full" disabled={busy||cameraOpen} onClick={()=>files.current?.click()}><UploadCloud size={16}/>{hasFile?'Add invoice pages':'Choose from files'}</button>
    <button className="button secondary full" disabled={busy||cameraOpen} onClick={openCamera}><Camera size={16}/>Take a photo</button>
    <small>One PDF with selectable text, or up to 5 JPEG/PNG pages, 3 MB combined. Files opens a picker; Photo opens a live camera preview.</small>
    {cameraOpen&&<div className="camera-preview"><div><strong>Camera preview</strong><button className="icon-button" onClick={stop} aria-label="Close camera"><X size={18}/></button></div><video ref={video} autoPlay muted playsInline/>{error?<p role="alert">{error}</p>:!ready?<p role="status">Waiting for camera permission…</p>:<button className="button primary full" onClick={takePhoto}><Camera size={16}/>Capture page</button>}</div>}
  </div>;
});
InvoiceUploadPicker.displayName='InvoiceUploadPicker';
