'use client';
import './workspace-menu.css';
import {useEffect,useRef,useState} from 'react';
import {ChevronDown,FolderOpen,Settings2,LogIn} from 'lucide-react';
import type {Session} from '../lib/types';
export function WorkspaceMenu({session,onNavigate}:{session:Session|null;onNavigate:(page:string)=>void}){
  const [open,setOpen]=useState(false),root=useRef<HTMLDivElement>(null);
  useEffect(()=>{if(!open)return;const close=(e:PointerEvent)=>{if(!root.current?.contains(e.target as Node))setOpen(false);};const key=(e:KeyboardEvent)=>{if(e.key==='Escape')setOpen(false);};document.addEventListener('pointerdown',close);document.addEventListener('keydown',key);return()=>{document.removeEventListener('pointerdown',close);document.removeEventListener('keydown',key);};},[open]);
  const navigate=(page:string)=>{onNavigate(page);setOpen(false);};
  return <div className="workspace-menu" ref={root}><button className="workspace" aria-expanded={open} aria-controls="workspace-options" onClick={()=>setOpen(!open)}><span className="workspace-icon">SG</span><span><strong>{session?.username?session.username:'Account & settings'}</strong><small>{session?.authenticated?'Personal account':'Guest workspace · 24 hours'}</small></span><ChevronDown size={14}/></button>{open&&<div className="workspace-options" id="workspace-options"><small>One private workspace per account</small><button onClick={()=>navigate('invoices')}><FolderOpen size={16}/>Open invoice inbox</button><button onClick={()=>navigate('settings')}><Settings2 size={16}/>Workspace & privacy</button><a href={session?.authenticated?'/accounts/logout/':'/accounts/login/'}><LogIn size={16}/>{session?.authenticated?'Sign out':'Sign in / switch account'}</a></div>}</div>;
}
