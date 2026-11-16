import zipfile, re, html, json, sys
src, out = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src)
ss = []
x = z.read('xl/sharedStrings.xml').decode('utf8')
for si in re.findall(r'<si>(.*?)</si>', x, re.S):
    ss.append(html.unescape(''.join(re.findall(r'<t[^>]*>(.*?)</t>', si, re.S))))
s = z.read('xl/worksheets/sheet1.xml').decode('utf8')
rows = re.findall(r'<row [^>]*>(.*?)</row>', s, re.S)
def cells(r):
    res = {}
    for attrs, body in re.findall(r'<c ([^>]*?)(?:/>|>(.*?)</c>)', r, re.S):
        ref = re.search(r'r="([A-Z]+)\d+"', attrs)
        v = re.search(r'<v>(.*?)</v>', body or '')
        t = re.search(r't="(\w+)"', attrs)
        val = v.group(1) if v else ''
        if t and t.group(1) == 's' and val != '':
            val = ss[int(val)]
        elif t and t.group(1) == 'inlineStr':
            val = html.unescape(''.join(re.findall(r'<t[^>]*>(.*?)</t>', body or '', re.S)))
        else:
            val = html.unescape(val)
        col = ref.group(1) if ref else None
        res[col] = val
    return res
def clean(t):
    t = t.replace('_x000D_', '').replace('\r', '').replace('　', ' ')
    t = re.sub(r'_x[0-9A-Fa-f]{4}_', '', t)
    return t.strip()
header = cells(rows[0])
cols = sorted(header.keys(), key=lambda c: (len(c), c))
hdr = {c: clean(header[c]) for c in cols}
data = []
for r in rows[1:]:
    c = cells(r)
    d = {hdr[k]: clean(v) for k, v in c.items() if k in hdr}
    data.append(d)
json.dump({'columns': list(hdr.values()), 'rows': data}, open(out, 'w'), ensure_ascii=False)
print('rows', len(data))
