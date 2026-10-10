'use client';
import {useCallback,useEffect,useRef,useState} from 'react';
import {attachWorkspaceHistory,type WorkspaceView} from '../lib/workspace-history';
export function useWorkspaceNavigation(){
  const [view,setView]=useState<WorkspaceView>({nav:'overview',modal:false});
  const controller=useRef<ReturnType<typeof attachWorkspaceHistory>|null>(null);
  useEffect(()=>{const active=attachWorkspaceHistory(window,setView);controller.current=active;return()=>{active.dispose();controller.current=null;};},[]);
  const setNav=useCallback((nav:string)=>controller.current?.setNav(nav),[]);
  const setModal=useCallback((open:boolean)=>controller.current?.setModal(open),[]);
  return {...view,setNav,setModal};
}
