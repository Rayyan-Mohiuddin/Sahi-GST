'use client';
import {useState} from 'react';
import type {Review} from '../lib/types';

// Presentation-only fixtures: never persisted or mixed with the user's reviews.
const examples=[{invoice:'DEMO/1042',supplier:'Deccan Office Supplies',total:'12,800',status:'Issue found'},{invoice:'DEMO/1043',supplier:'Synthetic Packaging Co.',total:'23,600',status:'Checks passed'},{invoice:'DEMO/1044',supplier:'Example Stationery',total:'5,900',status:'Needs review'}];
export function WorkspaceSummary({reviews,onSample}:{reviews:Review[];onSample:()=>void}){
  const [demo,setDemo]=useState(false);
  const pending=reviews.filter(review=>review.status==='needs_review').length;
  const counts=demo?[3,2,1,2]:[reviews.length,pending,reviews.filter(review=>review.status==='checked').length,pending];
  return <section className="workspace-summary" aria-label="Workspace summary"><label className="demo-toggle"><input type="checkbox" checked={demo} onChange={event=>setDemo(event.target.checked)}/><span>Load demo data <small>Demo · synthetic reviews only</small></span></label>
    {(demo||reviews.length>0)&&<div className="stats-grid">{['Invoices reviewed','Need your attention','Supported checks passed','Correction drafts'].map((label,index)=><div className="stat-card" key={label}><span className="stat-label">{label}</span><strong>{new Intl.NumberFormat('en-IN').format(counts[index])}</strong></div>)}</div>}
    {demo&&<div className="panel demo-dashboard"><div className="panel-heading"><h2>Demo workspace</h2><span className="badge neutral">Synthetic · not saved</span></div><p>Illustrative statuses, not saved results. Use Try the sample on Home to run the actual checks.</p><div className="table-wrap"><table><thead><tr><th scope="col">Invoice / supplier</th><th scope="col">Total</th><th scope="col">Status</th></tr></thead><tbody>{examples.map(item=><tr key={item.invoice}><td><span className="row-title"><span><strong>{item.invoice}</strong><small>{item.supplier}</small></span></span></td><td className="amount">Rs {item.total}</td><td><span className={`badge ${item.status==='Checks passed'?'success':item.status==='Issue found'?'status-issue':'warning'}`}>{item.status}</span></td></tr>)}</tbody></table></div></div>}
  </section>;
}
