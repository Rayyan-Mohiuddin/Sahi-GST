export function pageLimitError(files:Pick<File,'size'|'type'>[]):string|null{
  if(!files.length||files.length>5)return 'Choose 1–5 pages of the same invoice.';
  if(files.some(f=>!['image/png','image/jpeg'].includes(f.type)))return 'Each page must be JPEG/PNG.';
  if(files.reduce((sum,f)=>sum+f.size,0)>3*1024*1024)return 'Invoice pages must be under 3 MB combined for this deployment.';
  return null;
}
