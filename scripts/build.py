# 把 data/idioms.json 嵌入 src/template.html，產生單一檔 index.html（離線可開）
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / 'data' / 'idioms.json').read_text(encoding='utf8'))
tpl = (root / 'src' / 'template.html').read_text(encoding='utf8')
payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
out = tpl.replace('/*__DATA__*/[]', payload, 1)
(root / 'index.html').write_text(out, encoding='utf8')
print('built', len(data), 'idioms →', root / 'index.html')
