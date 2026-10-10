"""Render labelled synthetic invoice images for real OCR regression runs."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
target = root / 'tests' / 'ocr_images'
target.mkdir(parents=True, exist_ok=True)
layout_fixtures = json.loads((root / 'backend/invoices/fixtures/parser_layouts.json').read_text())[:3]
fonts = [Path('C:/Windows/Fonts/arial.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
font_path = next((x for x in fonts if x.exists()), None)
font = ImageFont.truetype(str(font_path), 38) if font_path else ImageFont.load_default(size=38)
header_font = ImageFont.truetype(str(font_path), 44) if font_path else ImageFont.load_default(size=44)
manifest = []
for index, fixture in enumerate(layout_fixtures, 1):
    lines = fixture['text'].splitlines()
    image = Image.new('RGB', (1650, max(650, 310 + len(lines)*64)), 'white')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, image.width, 160), fill='#155d48')
    draw.text((70, 35), 'SAHI GST - SYNTHETIC INVOICE', font=header_font, fill='white')
    draw.text((70, 103), 'TEST DOCUMENT - NOT A REAL TAX INVOICE', font=font, fill='white')
    for row, line in enumerate(lines):
        draw.text((70, 215 + row*64), line, font=font, fill='#152e2a')
    filename = f'layout-{index}.png'
    image.save(target / filename, optimize=True)
    manifest.append({'name':fixture['name'], 'image':filename, 'expected':fixture['expected'], 'ground_truth_text':fixture['text'], 'synthetic':True})
(target / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print(f'Generated {len(manifest)} synthetic images in {target}')
