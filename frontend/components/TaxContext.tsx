export function TaxContext({context}:{context?:{amount:string|null;label:string;eligibility_checked:boolean}}){
  if(!context)return null;
  return <section className="tax-context"><span>{context.label}</span><strong>{context.amount===null?'Confirm tax amounts':new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR'}).format(Number(context.amount))}</strong><p>This is the GST amount shown on the invoice. ITC availability requires a separate eligibility check; this figure is not calculated loss or savings.</p></section>;
}
