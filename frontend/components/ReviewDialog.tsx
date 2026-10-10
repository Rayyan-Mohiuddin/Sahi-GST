'use client';
import {useEffect,useRef} from 'react';
import {X} from 'lucide-react';
export function ReviewDialog({open,busy,title,onClose,children}:{open:boolean;busy:boolean;title:string;onClose:()=>void;children:React.ReactNode}){
  const dialog=useRef<HTMLElement>(null),callbacks=useRef({busy,onClose});callbacks.current={busy,onClose};
  useEffect(()=>{
    if(!open)return;
    const previous=document.activeElement as HTMLElement|null,overflow=document.body.style.overflow;
    document.body.style.overflow='hidden';dialog.current?.querySelector<HTMLElement>('button:not(:disabled)')?.focus();
    const key=(event:KeyboardEvent)=>{
      if(event.key==='Escape'&&!callbacks.current.busy)callbacks.current.onClose();
      if(event.key!=='Tab')return;
      const nodes=Array.from(dialog.current?.querySelectorAll<HTMLElement>('button:not(:disabled),input:not(:disabled),textarea,a[href],summary')||[]).filter(n=>n.getClientRects().length>0);
      const first=nodes[0],last=nodes[nodes.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
    };
    window.addEventListener('keydown',key);
    return()=>{window.removeEventListener('keydown',key);document.body.style.overflow=overflow;previous?.focus();};
  },[open]);
  if(!open)return null;
  return <div className="modal-backdrop"><section ref={dialog} className="review-modal" role="dialog" aria-modal="true" aria-labelledby="review-title"><header className="modal-heading"><div><span className="eyebrow">INVOICE REVIEW</span><h2 id="review-title">{title}</h2></div><button className="icon-button" disabled={busy} onClick={onClose} aria-label="Close invoice review"><X size={23}/></button></header>{children}</section></div>;
}
