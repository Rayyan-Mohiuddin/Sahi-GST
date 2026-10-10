/** Render textless PDFs only after the server has confirmed no embedded text. */
export async function renderPdfForOcr(file:File):Promise<File[]> {
  const pdfjs=await import('pdfjs-dist');
  pdfjs.GlobalWorkerOptions.workerSrc=new URL('pdfjs-dist/build/pdf.worker.min.mjs',import.meta.url).toString();
  const pdfDocument=await pdfjs.getDocument({data:await file.arrayBuffer()}).promise;
  if(pdfDocument.numPages>5)throw new Error('Upload at most 5 pages of one invoice.');
  const pages:File[]=[];
  for(let number=1;number<=pdfDocument.numPages;number++){
    const page=await pdfDocument.getPage(number);const viewport=page.getViewport({scale:2});const canvas=globalThis.document.createElement('canvas');canvas.width=Math.ceil(viewport.width);canvas.height=Math.ceil(viewport.height);
    await page.render({canvas,canvasContext:canvas.getContext('2d')!,viewport}).promise;
    const blob=await new Promise<Blob>((resolve,reject)=>canvas.toBlob((value:Blob|null)=>value?resolve(value):reject(new Error('Could not render this PDF page.')),'image/png'));
    pages.push(new File([blob],`${file.name.replace(/\.pdf$/i,'')}-page-${number}.png`,{type:'image/png'}));
  }
  return pages;
}
