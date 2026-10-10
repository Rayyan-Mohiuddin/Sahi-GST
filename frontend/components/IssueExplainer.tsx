'use client';
import {useEffect,useRef,useState} from 'react';
import {Sparkles,Volume2} from 'lucide-react';
import type {Review,Session} from '../lib/types';
type Explanation={id:string;text:string;source:string};
export function IssueExplainer({review,session}:{review:Review;session:Session|null}){
  const [language,setLanguage]=useState('en'),[items,setItems]=useState<Explanation[]>([]),[source,setSource]=useState('rule'),[busy,setBusy]=useState(false),[error,setError]=useState('');
  const active=useRef<AbortController|null>(null);
  const load=async(useAI:boolean)=>{
    active.current?.abort();const controller=new AbortController();active.current=controller;setBusy(true);setError('');
    try{const token=document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1]||'';
      const response=await fetch(`/api/reviews/${review.id}/explanations/`,{method:'POST',signal:controller.signal,headers:{'Content-Type':'application/json','X-CSRFToken':token},body:JSON.stringify({language,use_ai:useAI})});
      const data=await response.json();if(!response.ok)throw new Error(data.error||'Explanation unavailable.');setItems(data.explanations);setSource(data.source);
    }catch(e){if(!controller.signal.aborted)setError((e as Error).message);}finally{if(!controller.signal.aborted)setBusy(false);}
  };
  useEffect(()=>{void load(false);return()=>{active.current?.abort();window.speechSynthesis?.cancel();};},[review.id,language]);
  const speak=(text:string)=>{if(!window.speechSynthesis){setError('Speech is not supported by this browser.');return;}const locale={en:'en',hi:'hi',te:'te'}[language]!;const voice=window.speechSynthesis.getVoices().find(v=>v.localService&&v.lang.toLowerCase().startsWith(locale));if(!voice){setError('No local voice for this language is available on this device. The text is still readable.');return;}window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(text);utterance.voice=voice;utterance.lang=voice.lang;window.speechSynthesis.speak(utterance);};
  if(!review.result.findings.some(f=>['issue','review'].includes(f.status)))return null;
  return <section className="language-panel"><div><strong>Understand the finding</strong><select aria-label="Explanation language" value={language} disabled={busy} onChange={e=>setLanguage(e.target.value)}><option value="en">English</option><option value="hi">हिन्दी</option><option value="te">తెలుగు</option></select></div><small>{source==='gemini'?'AI wording based on the saved checks':'Rule-based wording'} · amounts and verdicts remain in the evidence above</small>{items.map(item=><article key={item.id}><strong>{review.result.findings.find(f=>f.id===item.id)?.title}</strong><p lang={language}>{item.text}</p><button className="text-button" onClick={()=>speak(item.text)}><Volume2 size={15}/>Read aloud</button></article>)}{session?.cloud_extraction&&session.authenticated&&<><small>AI wording sends these findings to Google. Verify it against the saved evidence.</small><button className="button secondary full" disabled={busy} onClick={()=>load(true)}><Sparkles size={16}/>{busy?'Preparing explanation…':'Explain with AI'}</button></>}{busy&&<p role="status">Preparing explanation…</p>}{error&&<p role="alert">{error} Rule evidence remains available.</p>}</section>;
}
