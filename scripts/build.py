# 把 data/idioms.json、data/strokes.json 嵌入 src/template.html，產生單一檔 index.html（離線可開）
# 只保留每個字都有筆畫資料的成語
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
idioms = json.loads((root / 'data' / 'idioms.json').read_text(encoding='utf8'))
strokes = json.loads((root / 'data' / 'strokes.json').read_text(encoding='utf8'))
kept = [it for it in idioms if all(c['c'] in strokes for c in it['chars'])]
used = {c['c'] for it in kept for c in it['chars']}
strokes_used = {k: v for k, v in strokes.items() if k in used}
tpl = (root / 'src' / 'template.html').read_text(encoding='utf8')
def js(x):
    return json.dumps(x, ensure_ascii=False).replace('</', '<\\/')
out = tpl.replace('/*__DATA__*/[]', js(kept), 1).replace('/*__STROKES__*/{}', js(strokes_used), 1)
(root / 'index.html').write_text(out, encoding='utf8')
print('built', len(kept), 'idioms (dropped', len(idioms) - len(kept), 'without stroke data) →', root / 'index.html')
