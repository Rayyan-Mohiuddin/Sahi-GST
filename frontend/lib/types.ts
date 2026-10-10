export type Fields = Record<string, string | null>;
export type ParseFeedback = {extracted_count:number; field_count:number; review_fields:{field:string;reason:string;message:string;evidence:string|null}[]};
export type Finding = {id:string; rule_id:string; field:string; status:string; title:string; message:string; observed?:string; expected?:string};
export type Result = {findings:Finding[]; counts:Record<string,number>; not_checked:string[]; rule_version:string; status:string};
export type Review = {id:string; fields:Fields; result:Result; source:string; status:string; created_at:string; draft:string; original_id:string|null};
export type Session = {authenticated:boolean; username:string|null; cloud_extraction:boolean; database:string};
