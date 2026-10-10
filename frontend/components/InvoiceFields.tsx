type Hint={field:string;message:string;evidence:string|null};
export function InvoiceFields({groups,fields,busy,hints,extracted,onEdit}:{groups:{name:string;fields:string[][]}[];fields:Record<string,string|null>;busy:boolean;hints:Hint[];extracted:boolean;onEdit:(key:string,value:string)=>void}){
 const all=groups.flatMap(g=>g.fields).filter(([key])=>!key.endsWith('gstin'));
 const needs=(key:string)=>hints.some(h=>h.field===key)||!fields[key];
 const render=(entries:string[][])=><div className="fields-grid">{entries.map(([key,label])=><label key={key} className={needs(key)?'field-needs-review':''}>{label}<input disabled={busy} value={fields[key]||''} onChange={e=>onEdit(key,e.target.value)} placeholder="Confirm from original" type={key==='invoice_date'?'date':'text'} inputMode={['taxable_value','tax_rate','cgst','sgst','igst','round_off','total'].includes(key)?'decimal':undefined}/>{hints.filter(h=>h.field===key).map(h=><span className="field-hint" key={h.field}>{h.message}{h.evidence&&<small>Read text: {h.evidence}</small>}</span>)}</label>)}</div>;
 if(!extracted)return <fieldset><legend>Invoice fields</legend>{render(all)}</fieldset>;
 const uncertain=all.filter(([key])=>needs(key)),other=all.filter(([key])=>!needs(key));
 return <><fieldset><legend>{uncertain.length?`${uncertain.length} details need a closer look`:'No additional uncertainty flagged'}</legend>{render(uncertain)}</fieldset>{other.length>0&&<details className="extracted-fields"><summary>Review {other.length} other extracted fields</summary><p>No uncertainty was flagged for these values. This is not a confidence guarantee; compare them with the original before confirming.</p>{render(other)}</details>}</>;
}
