import io
from zoneinfo import ZoneInfo
from html import escape
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from .rules import correction_draft, MONEY_FIELDS, number

def indian_amount(value):
    amount=number(value)
    if amount is None: return value
    whole,fraction=f"{abs(amount):.2f}".split(".")
    last=whole[-3:];prefix=whole[:-3];groups=[]
    while prefix:
        groups.insert(0,prefix[-2:]);prefix=prefix[:-2]
    grouped=",".join(groups+[last])
    return ("-" if amount<0 else "")+grouped+"."+fraction


# ReportLab's bundled font avoids missing rupee glyphs and adds no font download.
font_file = Path(__import__('reportlab').__file__).parent / 'fonts' / 'Vera.ttf'
if 'SahiReport' not in pdfmetrics.getRegisteredFontNames():
    pdfmetrics.registerFont(TTFont('SahiReport', str(font_file)))

def build_report(reviews):
    buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('SahiBody',fontName='SahiReport',fontSize=9,leading=14,textColor=colors.HexColor('#263b33')))
    styles.add(ParagraphStyle('SahiTitle',fontName='SahiReport',fontSize=23,leading=30,textColor=colors.HexColor('#155d48'),spaceAfter=10))
    styles.add(ParagraphStyle('SahiHeading',fontName='SahiReport',fontSize=12,leading=18,spaceBefore=15,spaceAfter=7,textColor=colors.HexColor('#155d48')))
    def safe(value):
        # The bundled font does not cover every Indian-language glyph; monetary labels use INR.
        return escape(str(value if value is not None else 'Not provided').replace('₹','INR ').replace('—','-').replace('–','-')).replace('\n','<br/>')
    def para(value,style='SahiBody'): return Paragraph(safe(value),styles[style])
    story=[para('Sahi GST | Invoice review report','SahiTitle'),para('Checks apply to confirmed fields. This report is not a GST compliance certificate or a corrected supplier invoice.'),Spacer(1,12)]
    for review in reviews:
        f=review.fields;r=review.result
        created=review.created_at.astimezone(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M IST')
        story += [para(f"Invoice {f.get('invoice_number') or '(number to confirm)'}",'SahiHeading'),para(f"Supplier: {f.get('supplier_name') or 'Not provided'} | Review: {str(review.id)}"),para(f"Created: {created} | Rule version: {r['rule_version']} | Source: {review.source}"),Spacer(1,8)]
        stamp=Table([[para('CHECK ID  '+str(review.id))]],colWidths=[510])
        stamp.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.2,colors.HexColor('#344d62')),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f3f6fa')),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
        story += [stamp,Spacer(1,8)]
        labels={'supplier_gstin' :'Supplier GSTIN','buyer_gstin':'Buyer GSTIN','cgst':'CGST','sgst':'SGST','igst':'IGST','tax_rate':'Printed GST rate (%)'}
        story.append(para('Monetary amounts are INR. The printed rate is a percentage.'))
        rows=[[para('Confirmed field'),para('Value')]]+[[para(labels.get(key,key.replace('_',' ').title())),para(indian_amount(value) if key in MONEY_FIELDS else value)] for key,value in f.items()]
        table=Table(rows,colWidths=[160,350],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf2ec')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#dce6df')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
        story += [table,para('Findings and evidence','SahiHeading')]
        for finding in r['findings']:
            if finding['status']=='pass': continue
            block=[para(f"{finding['status'].replace('_',' ').title()} | {finding['title']}"),para(finding['message'])]
            if finding.get('expected') is not None:
                block.append(para(f"Observed: {finding.get('observed')} | Arithmetic expected: {finding['expected']}"))
            story += [KeepTogether(block),Spacer(1,9)]
        story += [KeepTogether([para(f"{r['counts']['pass']} supported checks passed. Not checked:",'SahiHeading')]+[para('- '+item) for item in r['not_checked']])]
        story += [para('Next action / supplier request','SahiHeading'),para(correction_draft(f,r)),Spacer(1,20)]
    def footer(canvas,doc):
        canvas.saveState();canvas.setStrokeColor(colors.HexColor('#f1f3f5'));canvas.setLineWidth(.25)
        for y in range(52,800,22): canvas.line(38,y,A4[0]-38,y)
        canvas.setFont('SahiReport',8);canvas.setFillColor(colors.HexColor('#718277'))
        canvas.drawString(42,26,'Sahi GST - evidence for review, not legal certification')
        canvas.drawRightString(A4[0]-42,26,f'Page {doc.page}');canvas.restoreState()
    SimpleDocTemplate(buffer,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=45,title='Sahi GST invoice review',author='Sahi GST').build(story,onFirstPage=footer,onLaterPages=footer)
    return buffer.getvalue()
