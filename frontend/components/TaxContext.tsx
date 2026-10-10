'use client';
import {useEffect,useState} from 'react';
export function TaxContext({context}:{context?:{amount:string|null;label:string;eligibility_checked:boolean}}){
 const amount=context?.amount===null?null:Number(context?.amount);
 const [display,setDisplay]=useState(amount);
 useEffect(()=>{if(amount===null||!Number.isFinite(amount)){setDisplay(null);return;}if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){setDisplay(amount);return;}let frame=0;const start=performance.now();const tick=(now:number)=>{const progress=Math.min((now-start)/550,1);setDisplay(amount*(1-Math.pow(1-progress,3)));if(progress<1)frame=requestAnimationFrame(tick);};frame=requestAnimationFrame(tick);return()=>cancelAnimationFrame(frame);},[amount]);
 if(!context)return null;
 const format=(value:number)=>new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:2}).format(value);
 return <section className="tax-context"><span>{context.label}</span><strong aria-label={amount===null?'Confirm tax amounts':format(amount)}><span aria-hidden="true">{display===null?'Confirm tax amounts':format(display)}</span></strong><p>Invoice GST, shown once. Credit eligibility is not checked; this is not a loss or savings estimate.</p></section>;
}
