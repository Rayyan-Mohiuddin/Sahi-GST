import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
const runtime='C:/Users/pro7p/.cache/codex-runtimes/codex-primary-runtime/dependencies';
process.env.RUNTIME_NODE_MODULES=`${runtime}/node/node_modules`;
const skill='C:/Users/pro7p/.codex/plugins/cache/openai-primary-runtime/presentations/26.1007.11041/skills/presentations';
const {PresentationFile,FileBlob}=await import(pathToFileURL(`${runtime}/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs`));
const workspaceDir=process.cwd(), stage=path.join(workspaceDir,'.local/deck-espada'),out=path.join(workspaceDir,'output/presentation-espada');
await fs.mkdir(stage,{recursive:true});await fs.mkdir(out,{recursive:true});
const p=await PresentationFile.importPptx(await FileBlob.load('output/presentation/Sahi-GST-jury-pitch.pptx'));
const snap=await p.inspect({kind:'slide,textbox,image',maxChars:100000});
const records=snap.records;
const original=p.slides.items.slice();
const C={ink:'#172C40',paper:'#F7F3EB',muted:'#596775',accent:'#BB641A'};
function text(s,content,x,y,w,h,size=28,color=C.ink,bold=false,font='Aptos'){
 const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=content;t.text.style={fontFamily:font,fontSize:size,color,bold};return t;
}
function replace(index,match,value){const r=records.find(r=>r.kind==='textbox'&&r.slideIndex===index&&r.text===match);if(!r)throw new Error(`Missing source text ${match}`);p.resolve(r.id).text=value;}
function clear(index){p.delete(records.filter(r=>r.slideIndex===index&&['textbox','image'].includes(r.kind)).map(r=>r.id));}
// Remove hidden duplicate cover title; keep original artwork and visible title.
p.delete(records.find(r=>r.kind==='textbox'&&r.slideIndex===0&&r.text==='Your invoice looks fine.\nYour totals might disagree.').id);
clear(2);let s=original[2];
text(s,'We took the problem to a real store',64,64,1140,85,46,C.ink,true);
s.images.add({blob:new Uint8Array(await fs.readFile(process.env.INTERVIEW_PHOTO||'D:/Downloads/ratnadeep.jpeg')),contentType:'image/jpeg',fit:'contain',position:{left:64,top:184,width:530,height:416},alt:'User-supplied photo from Salman’s visit to Ratnadeep supermarket in Hanamkonda'});
text(s,'Ratnadeep supermarket\nHanamkonda',650,188,535,85,30,C.ink,true);
text(s,'Salman spoke with employee\nSai Karthik about invoice issues.',650,300,535,80,27);
text(s,'He reported a similar problem,\nexpressed interest in Sahi GST,\nand invited a follow-up.',650,410,535,120,29,C.ink,true);
text(s,'Early customer signal • one conversation',650,574,540,35,21,C.muted);
s.speakerNotes.text='Source: Salman’s account supplied in this chat and his photograph. Paraphrase, not a verbatim quote. Conversation date not supplied. No phone number included. One employee’s feedback is not corporate endorsement, adoption, CA review or a paid pilot. Obtain permission before publishing this named photo outside the requested jury deck. Follow up to ask for a redacted example, current process, frequency, time spent and a supervised trial.';
replace(5,'Working prototype ≠ validated tax advice','Evidence-led invoice checks');
replace(5,'Still to establish','Next validation milestones');
replace(5,'Single-rate domestic B2B goods only. No compliance or ITC certification.','Supported scope: single-rate domestic B2B goods invoices.');
replace(6,'Proposed pilot. No interviews or endorsements claimed.','One store conversation completed. Structured pilot is next.');
original[6].speakerNotes.text+='\nUpdate: Salman reports one conversation with Sai Karthik, a Ratnadeep employee in Hanamkonda. The 2-CA/3-bookkeeper/20-case pilot remains proposed; no CA sign-off or business partnership claimed.';
// Add a real example of the existing language templates, before the AI/rules slide.
const language=p.slides.add();language.background.fill=C.paper;
text(language,'Understand the finding in your language',64,64,1150,90,44,C.ink,true);
text(language,'Example: printed invoice total does not match the confirmed amounts',64,168,1150,60,24,C.muted);
text(language,'ENGLISH',64,252,170,40,21,C.ink,true);
text(language,'The printed total differs from the confirmed amounts.\nCheck the original and ask the supplier to clarify the difference.',260,243,940,88,27);
text(language,'HINDI',64,364,170,40,21,C.ink,true);
text(language,'बिल का कुल योग पुष्टि की गई रकम से मेल नहीं खाता।\nमूल बिल जाँचें और अंतर के बारे में सप्लायर से पूछें।',260,351,940,92,28,C.ink,false,'Nirmala UI');
text(language,'TELUGU',64,480,170,40,21,C.ink,true);
text(language,'బిల్లులోని మొత్తం, నిర్ధారించిన మొత్తాలతో సరిపోలడం లేదు.\nఅసలు బిల్లును చూసి, తేడా గురించి సరఫరాదారుని అడగండి.',260,469,940,100,28,C.ink,false,'Nirmala UI');
text(language,'Text examples from the app • read-aloud depends on installed device voices',64,604,1150,35,20,C.muted);
language.speakerNotes.text='Exact M04 text from backend/invoices/languages.py. Frontend IssueExplainer is rendered on Findings and selects en/hi/te; endpoint /api/reviews/{id}/explanations/. These are rule-template examples, not new live-demo verification or native-speaker approval. Preview access currently blocks browser acceptance. Browser speech requires an installed local voice. Native-speaker review and two-phone testing remain pending.';
// Team before final call to action.
const team=p.slides.add();team.background.fill=C.paper;
text(team,'Meet Espada',64,64,1140,90,52,C.ink,true);
text(team,'Team ID: TRI26278',64,180,1100,55,28,C.muted);
text(team,'Salman Imran Syed',64,292,1140,70,43,C.ink,true);
text(team,'Rayyan Mohiuddin',64,382,1140,70,43,C.ink,true);
text(team,'Kakatiya Institute of Technology and Science, Warangal',64,506,1140,65,30);
text(team,'Third-year students',64,589,1100,45,26,C.muted);
team.speakerNotes.text='Names, college, year, team name and ID supplied by the user. Do not assign contributions that have not been recorded in TEAM_CONTRIBUTIONS.md.';
// A crisp final scan slide, using the supplied QR unchanged with white quiet space.
clear(9);s=original[9];s.background.fill=C.ink;
text(s,'See Sahi GST in action',64,64,1140,90,52,C.paper,true);
text(s,'Scan. Check. Ask for the fix.',64,218,660,110,43,C.paper,true);
text(s,'Try the synthetic invoice.\nInspect the mismatch.\nRead the correction request.',64,358,650,145,30,'#D7E1EA');
text(s,'sahi-gst-d511.vercel.app',64,561,660,55,28,C.paper,true);
s.images.add({blob:new Uint8Array(await fs.readFile(process.env.WEBSITE_QR||'D:/Downloads/Sahi GST qr.png')),contentType:'image/png',fit:'contain',position:{left:840,top:206,width:360,height:360},alt:'User-supplied QR code intended to open the Sahi GST live website'});
text(s,'Scan to open the live product',815,584,405,45,23,C.paper);
s.speakerNotes.text='Use the original user-supplied QR without cropping or regeneration. Intended site supplied by user context: https://sahi-gst-d511.vercel.app/ . Verify QR destination by scanning on a phone before presenting; automatic decoding was not available in the local runtime. Demo the labelled synthetic invoice and original source; do not imply financial loss or verified tax eligibility. Opening pitch: “One wrong digit can turn a routine invoice into a correction chase. Sahi GST reads the invoice, asks you to confirm uncertain details, checks the numbers, and helps you request the exact fix. We spoke with a supermarket employee in Hanamkonda who reported a similar problem and invited a follow-up. Scan the code and try the synthetic example.”';
// One consistent, visible identity on every slide, including the cover.
p.slides.reorder([...original.slice(0,4),language,...original.slice(4,9),team,original[9]].map(s=>`sl/${s.id}`));
const updated=await p.inspect({kind:'textbox',maxChars:100000});
p.delete(updated.records.filter(r=>r.kind==='textbox'&&r.text.startsWith('SAHI GST  /')).map(r=>r.id));
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];const dark=[original[3],original[7],original[9]].includes(slide);
 text(slide,`ESPADA  |  TEAM ID: TRI26278  |  SAHI GST`,64,668,1030,28,18,dark?'#D7E1EA':C.ink);
 text(slide,String(i+1).padStart(2,'0'),1160,668,60,28,18,dark||i===0?'#D7E1EA':C.ink);
 const png=await p.export({slide,format:'png',scale:1});await fs.writeFile(path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidatePath=path.join(stage,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidatePath);
const {finalizePresentation}=await import(pathToFileURL(`${skill}/container_tools/artifact_tool_utils.mjs`));
const result=await finalizePresentation({workspaceDir,candidatePath,finalPath:path.join(out,'Sahi-GST-Espada-jury-pitch.pptx'),pythonExecutable:`${runtime}/python/python.exe`,integrityValidatorPath:`${skill}/container_tools/inspect_presentation_package_integrity.py`,layoutValidatorPath:`${skill}/container_tools/inspect_presentation_layout_geometry.py`,layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'reference',families:['Aptos'],referencePath:path.join(workspaceDir,'output/presentation/Sahi-GST-jury-pitch.pptx'),referenceSha256:createHash('sha256').update(await fs.readFile('output/presentation/Sahi-GST-jury-pitch.pptx')).digest('hex'),scriptFonts:{cs:'Nirmala UI'}},verifyArtifactToolImport:true,receiptPath:path.join(stage,'validation.json')});
console.log(JSON.stringify(result));

