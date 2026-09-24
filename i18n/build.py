"""Injecte les traductions (i18n/*.json) dans index.html, entre /*I18N*/ et /*/I18N*/."""
import json, re, pathlib
root = pathlib.Path(__file__).resolve().parent
order = ['fr', 'en', 'zh', 'hi', 'es', 'ar', 'bn', 'pt', 'ru', 'ja']
ref = json.loads((root / 'fr.json').read_text(encoding='utf-8'))
def check(c, d):
    assert set(d) == set(ref), (c, set(ref) ^ set(d))
    assert set(d['s']) == set(ref['s']), (c, set(ref['s']) ^ set(d['s']))
    assert len(d['caps']) == len(ref['caps']) and len(d['chapters']) == 11, c
    ws = set(w for g in d['words']['groups'] for w in g)
    assert all(w in ws for st in d['words']['steps'] for w, _ in st) and d['words']['start'] in ws, c
    assert len(d['words']['steps']) == 8 and len(d['words']['pick']) == 8, c
data = {}
for c in order:
    f = root / f'{c}.json'
    if not f.exists(): continue
    try: d = json.loads(f.read_text(encoding='utf-8')); check(c, d); data[c] = d
    except Exception as e: print('ignorée :', c, e)
blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
html = root.parent / 'index.html'
s = html.read_text(encoding='utf-8')
s, n = re.subn(r'/\*I18N\*/.*?/\*/I18N\*/', lambda m: '/*I18N*/const I18N = ' + blob + ';/*/I18N*/', s, flags=re.S)
assert n == 1
html.write_text(s, encoding='utf-8')
print('langues :', ', '.join(data))
