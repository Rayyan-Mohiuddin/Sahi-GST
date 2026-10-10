'use client';
import {useEffect,useState} from 'react';
import {ArrowRight,CheckCheck,ShieldCheck} from 'lucide-react';

export function LandingPage({authenticated,onCheck,onSample,onNavigate}:{authenticated:boolean;onCheck:()=>void;onSample:()=>void;onNavigate:(view:string)=>void}){
  const [difference,setDifference]=useState(1000);
  useEffect(()=>{
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    let frame=0;const start=performance.now();
    const tick=(now:number)=>{const progress=Math.min((now-start)/600,1);setDifference(Math.round(1000*(1-(1-progress)**3)));if(progress<1)frame=requestAnimationFrame(tick);};
    frame=requestAnimationFrame(tick);return()=>cancelAnimationFrame(frame);
  },[]);
  return <div className="landing">
    <header className="landing-header"><a className="landing-brand" href="/" aria-label="Sahi GST home"><CheckCheck aria-hidden="true"/>Sahi GST</a><a className="workspace-chip" href="/?view=invoices" onClick={event=>{event.preventDefault();onNavigate('invoices');}}>{authenticated?'Your workspace':'Guest workspace'}<ArrowRight size={14} aria-hidden="true"/></a></header>
    <main id="landing-main">
      <section className="landing-hero" aria-labelledby="landing-title">
        <div className="landing-copy"><h1 id="landing-title">One wrong digit can delay your business.</h1><p>Check a supported GST goods invoice before you send it. Understand findings in English, Hindi or Telugu, and ask for the fix.</p><div className="landing-actions"><button className="button primary" onClick={onCheck}>Check an invoice <ArrowRight size={18} aria-hidden="true"/></button><button className="button secondary" onClick={onSample}>Try the sample</button></div></div>
        <figure className="invoice-example" aria-label="Synthetic invoice DEMO/1042. Taxable value Rs 10,000, GST at 18 percent Rs 1,800, printed total Rs 12,800. Expected total Rs 11,800: Rs 1,000 difference.">
          <figcaption>Synthetic example</figcaption><div className="example-paper"><div className="example-heading"><span>DECCAN OFFICE SUPPLIES</span><strong>DEMO/1042</strong></div><dl><div><dt>Taxable value</dt><dd>Rs 10,000</dd></div><div><dt>GST <small>18%</small></dt><dd>Rs 1,800</dd></div><div className="example-mismatch"><dt>Printed total <small>Doesn’t add up</small></dt><dd>Rs 12,800</dd></div><div className="example-expected"><dt>Expected total</dt><dd>Rs 11,800</dd></div></dl></div><div className="example-difference" aria-label="Rs 1,000 difference found"><strong aria-hidden="true">Rs {new Intl.NumberFormat('en-IN').format(difference)}</strong><span>difference found</span></div>
        </figure>
        <p className="landing-trust"><ShieldCheck size={16} aria-hidden="true"/>A review aid, not a compliance certificate.</p><p className="landing-scope">Works for: single-rate domestic B2B goods invoices.</p>
      </section>
      <section className="landing-steps" aria-label="How it works">{['Bring your invoice','See what needs attention','Ask for the right correction'].map((text,index)=><div key={text}><span aria-hidden="true">0{index+1}</span><h2>{text}</h2></div>)}</section>
    </main>
    <footer className="landing-footer"><span>Sahi GST</span><nav aria-label="Information"><a href="/?view=settings" onClick={event=>{event.preventDefault();onNavigate('settings');}}>Workspace and privacy</a><a href="/?view=guide" onClick={event=>{event.preventDefault();onNavigate('guide');}}>How it works</a></nav></footer>
  </div>;
}
