export type WorkspaceView = {nav:string; modal:boolean};
const pages = new Set(['overview','invoices','followups','reports','settings','guide']);
type Port = Pick<Window,'history'|'location'|'addEventListener'|'removeEventListener'>;

/** Each opened review gets one history entry, so Back closes it before leaving. */
export function attachWorkspaceHistory(port:Port, onChange:(view:WorkspaceView)=>void) {
  const initialPage = new URL(port.location.href).searchParams.get('view') || 'overview';
  let view:WorkspaceView={nav:pages.has(initialPage)?initialPage:'overview',modal:false};
  const write=(next:WorkspaceView,replace=false)=>{
    const url=new URL(port.location.href);
    if(next.nav==='overview')url.searchParams.delete('view');else url.searchParams.set('view',next.nav);
    const state={...port.history.state,sahiGST:next};
    if(replace)port.history.replaceState(state,'',url.href);else port.history.pushState(state,'',url.href);
    view=next;onChange({...view});
  };
  write(view,true);
  const pop=()=>{
    const saved=port.history.state?.sahiGST;
    const nav=saved?.nav || new URL(port.location.href).searchParams.get('view') || 'overview';
    view={nav:pages.has(nav)?nav:'overview',modal:saved?.modal===true};
    onChange({...view});
  };
  port.addEventListener('popstate',pop);
  return {
    setNav:(nav:string)=>{if(pages.has(nav)&&(view.nav!==nav||view.modal))write({nav,modal:false});},
    setModal:(open:boolean)=>{
      if(open===view.modal)return;
      if(open)write({...view,modal:true});
      else port.history.back();
    },
    dispose:()=>port.removeEventListener('popstate',pop),
  };
}
