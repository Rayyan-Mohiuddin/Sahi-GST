import type {Finding} from './types';
export type ExplanationLanguage='en'|'hi'|'te';
// Mirrors backend/invoices/languages.py; parity tested against that source.
export const RULE_MESSAGES:Record<ExplanationLanguage,Record<string,string>>={
  "en": {
    "M04": "The printed total differs from the confirmed amounts. Check the original and ask the supplier to clarify the difference.",
    "M02": "The printed rate and tax amount need checking. Confirm the invoice uses one rate before requesting a correction.",
    "I01": "Check every GSTIN character against the original. A format check does not verify active registration.",
    "default": "Check this finding against the original invoice. Confirm the detail and ask the supplier to clarify anything missing or inconsistent."
  },
  "hi": {
    "M04": "बिल का कुल योग पुष्टि की गई रकम से मेल नहीं खाता। मूल बिल जाँचें और अंतर के बारे में सप्लायर से पूछें।",
    "M02": "बिल पर लिखी दर और टैक्स की रकम जाँचें। सुधार माँगने से पहले पुष्टि करें कि बिल में एक ही दर है।",
    "I01": "GSTIN का हर अक्षर मूल बिल से मिलाएँ। सही प्रारूप से सक्रिय पंजीकरण की पुष्टि नहीं होती।",
    "default": "इस जानकारी को मूल बिल से मिलाएँ। कोई जानकारी गायब या अलग हो तो सप्लायर से स्पष्ट करें।"
  },
  "te": {
    "M04": "బిల్లులోని మొత్తం, నిర్ధారించిన మొత్తాలతో సరిపోలడం లేదు. అసలు బిల్లును చూసి, తేడా గురించి సరఫరాదారుని అడగండి.",
    "M02": "బిల్లులోని పన్ను రేటు, పన్ను మొత్తాన్ని తనిఖీ చేయండి. సవరణ అడిగే ముందు బిల్లులో ఒకే రేటు ఉందో నిర్ధారించండి.",
    "I01": "GSTIN లోని ప్రతి అక్షరాన్ని అసలు బిల్లుతో పోల్చండి. సరైన ఆకృతి ఉన్నంత మాత్రాన నమోదు క్రియాశీలంగా ఉందని నిర్ధారణ కాదు.",
    "default": "ఈ వివరాన్ని అసలు బిల్లుతో పోల్చండి. వివరాలు లేకపోయినా లేదా తేడా ఉన్నా సరఫరాదారుని వివరణ అడగండి."
  }
};
export function ruleExplanations(findings:Finding[],language:ExplanationLanguage){
 return findings.filter(f=>f.status==='issue'||f.status==='review').map(f=>({id:f.id,text:RULE_MESSAGES[language][f.rule_id]||RULE_MESSAGES[language].default,source:'rule'}));
}
