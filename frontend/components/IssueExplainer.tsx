'use client';
import {useEffect,useRef,useState} from 'react';
import {Sparkles,Volume2} from 'lucide-react';
import type {Review,Session} from '../lib/types';
import {ruleExplanations,type ExplanationLanguage} from '../lib/rule-explanations';
type Explanation={id:string;text:string;source:string};
export function IssueExplainer({review,session}:{review:Review;session:Session|null}){
  const [language,setLanguage]=useState<ExplanationLanguage>('en'),[ai,setAI]=useState<{review:string;language:ExplanationLanguage;items:Explanation[]}|null>(null),[busy,setBusy]=useState(false),[error,setError]=useState('');
  const currentAI=ai?.review===review.id&&ai.language===language?ai:null;
  const items=currentAI?.items||ruleExplanations(review.result.findings,language),source=currentAI?'gemini':'rule';
  const active=useRef<AbortController|null>(null);
  const load=async(useAI:boolean)=>{
    active.current?.abort();const controller=new AbortController();active.current=controller;setBusy(true);setError('');
    const timer=window.setTimeout(()=>{if(!controller.signal.aborted&&active.current===controller){controller.abort();setBusy(false);setAI(null);setError('AI wording timed out. Showing the rule explanation.');}},25000);
    try{const token=document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1]||'';
      const response=await fetch(`/api/reviews/${review.id}/explanations/`,{method:'POST',signal:controller.signal,headers:{'Content-Type':'application/json','X-CSRFToken':token},body:JSON.stringify({language,use_ai:useAI})});
      const data=await response.json();if(!response.ok)throw new Error(data.error||'Explanation unavailable.');
      if(!Array.isArray(data.explanations)||!data.explanations.length||data.explanations.some((item:Explanation)=>typeof item.text!=='string'||!item.text.trim()||!items.some(f=>f.id===item.id)))throw new Error('AI returned no usable explanation.');
      if(!controller.signal.aborted&&active.current===controller)setAI({review:review.id,language,items:data.explanations});
    }catch(e){if(!controller.signal.aborted&&active.current===controller){setAI(null);setError((e as Error).message);}}finally{window.clearTimeout(timer);if(!controller.signal.aborted&&active.current===controller)setBusy(false);}
  };
  useEffect(()=>{setAI(null);setBusy(false);setError('');return()=>{active.current?.abort();window.speechSynthesis?.cancel();};},[review.id,language]);
  const speak=(text:string)=>{if(!window.speechSynthesis){setError('Speech is not supported by this browser.');return;}const locale={en:'en',hi:'hi',te:'te'}[language]!;const voice=window.speechSynthesis.getVoices().find(v=>v.localService&&v.lang.toLowerCase().startsWith(locale));if(!voice){setError('No local voice for this language is available on this device. The text is still readable.');return;}window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(text);utterance.voice=voice;utterance.lang=voice.lang;window.speechSynthesis.speak(utterance);};
  if(!review.result.findings.some(f=>['issue','review'].includes(f.status)))return null;
  return <section className="language-panel"><div><strong>Explanations · English / Hindi / Telugu</strong><select aria-label="Explanation language" value={language} onChange={e=>setLanguage(e.target.value as ExplanationLanguage)}><option value="en">English</option><option value="hi">Hindi · हिन्दी</option><option value="te">Telugu · తెలుగు</option></select></div><small>{source==='gemini'?'AI wording based on the saved checks':'Rule-based wording'} · amounts and verdicts remain in the evidence above</small>{items.map(item=><article key={item.id}><strong>{review.result.findings.find(f=>f.id===item.id)?.title}</strong><p lang={language}>{item.text}</p><button className="text-button" onClick={()=>speak(item.text)}><Volume2 size={15}/>Read aloud</button></article>)}{session?.cloud_extraction&&session.authenticated&&<><small>AI wording sends these findings to Google. Verify it against the saved evidence.</small><button className="button secondary full" disabled={busy} onClick={()=>load(true)}><Sparkles size={16}/>{busy?'Preparing explanation…':'Explain with AI'}</button></>}{busy&&<p role="status">Preparing explanation…</p>}{error&&<p role="alert">{error} Rule evidence remains available.</p>}</section>;
}
