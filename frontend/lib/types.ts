export type Fields = Record<string, string | null>;
export type ParseFeedback = {extracted_count:number; field_count:number; review_fields:{field:string;reason:string;message:string;evidence:string|null;confidence?:number;region?:{x:number;y:number;width:number;height:number}}[];field_confidence?:Record<string,number|null>;corrections?:{field:string;rule:string;original:string;normalized:string}[];raw_ocr_text?:string;image_quality?:{score:number;warnings:string[]}};
export type Finding = {id:string; rule_id:string; field:string; status:string; title:string; message:string; observed?:string; expected?:string};
export type Result = {findings:Finding[]; counts:Record<string,number>; not_checked:string[]; rule_version:string; status:string;tax_context?:{amount:string|null;label:string;eligibility_checked:boolean}};
export type Review = {id:string; fields:Fields; result:Result; source:string; status:string; created_at:string; draft:string; original_id:string|null;image_urls?:string[];image_url:string|null;report_url:string};
export type Session = {authenticated:boolean; username:string|null; cloud_extraction:boolean; database:string};
