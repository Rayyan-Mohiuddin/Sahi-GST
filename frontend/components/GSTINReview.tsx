'use client';
import {ShieldCheck} from 'lucide-react';
type Hint={field:string;message:string;evidence:string|null};
export function GSTINReview({fields,confirmed,busy,hints,onEdit,onConfirm}:{fields:Record<string,string|null>;confirmed:Record<string,boolean>;busy:boolean;hints:Hint[];onEdit:(key:string,value:string)=>void;onConfirm:(key:string,checked:boolean)=>void}){
  return <fieldset className="gstin-review"><legend><ShieldCheck size={16}/>Confirm GSTINs character by character</legend><p>OCR can confuse Z/2, O/0 and I/1. Even a correctly shaped GSTIN may be misread. Check the original before confirming.</p><div className="fields-grid">{[['supplier_gstin','Supplier GSTIN'],['buyer_gstin','Buyer GSTIN']].map(([key,label])=><div key={key} className={hints.some(h=>h.field===key)?'field-needs-review':''}>
    <label htmlFor={`gstin-${key}`}>{label}<input id={`gstin-${key}`} className="gstin-input" disabled={busy} value={fields[key]||''} onChange={e=>onEdit(key,e.target.value)} spellCheck={false} autoCapitalize="characters" autoCorrect="off" placeholder="Read from the original" aria-describedby={`gstin-hint-${key}`}/></label>
    <span id={`gstin-hint-${key}`} className="field-hint">{hints.find(h=>h.field===key)?.message||'Matching the format does not verify registration or exact spelling.'}</span>

  </div>)}</div></fieldset>;
}
