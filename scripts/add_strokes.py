import re, json, sys, unicodedata
idioms_path, irg_path, rs_path, out_path = sys.argv[1:5]
total = {}
rs = {}
for line in open(irg_path, encoding='utf8'):
    if line.startswith('#') or '\t' not in line: continue
    cp, field, val = line.rstrip('\n').split('\t', 2)
    ch = chr(int(cp[2:], 16))
    if field == 'kTotalStrokes':
        total[ch] = int(val.split()[0])
for line in open(rs_path, encoding='utf8'):
    if line.startswith('#') or '\t' not in line: continue
    cp, field, val = line.rstrip('\n').split('\t', 2)
    ch = chr(int(cp[2:], 16))
    if field in ('kRSKangXi', 'kRSUnicode') and ch not in rs:
        rs[ch] = val.split()[0]
def radical_char(v):
    m = re.match(r"(\d+)'?\.", v)
    if not m: return None
    n = int(m.group(1))
    return unicodedata.normalize('NFKC', chr(0x2F00 + n - 1))
data = json.load(open(idioms_path, encoding='utf8'))
miss = set()
for it in data:
    chars = []
    for ch in it['word']:
        s = total.get(ch)
        r = radical_char(rs[ch]) if ch in rs else None
        if s is None: miss.add(ch)
        chars.append({'c': ch, 's': s, 'r': r})
    it['chars'] = chars
json.dump(data, open(out_path, 'w', encoding='utf8'), ensure_ascii=False)
print('idioms', len(data), 'missing strokes:', len(miss), sorted(miss)[:20])
