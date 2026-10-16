import json,re,os,sys
GEN=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(sys.argv[1] if len(sys.argv)>1 else os.path.join(GEN,'data.json')))
B=D['blocks']; I=set(D['items']); E=set(D['entities'])
def chk_block(tok,where):
    m=re.match(r'^(?:minecraft:)?([a-z0-9_]+)(\[[^\]]*\])?(\{.*\})?$',tok)
    if not m: return f'bloque raro {tok[:40]}'
    name,props=m.group(1),m.group(2)
    if name not in B: return f'bloque no existe: {name}'
    if props:
        st={s['n']:s for s in B[name]}
        for kv in props[1:-1].split(','):
            k,v=kv.split('=')
            if k not in st: return f'{name}: propiedad {k} no existe ({list(st)})'
            s=st[k]
            if s['t']=='enum' and v not in s['v']: return f'{name}: {k}={v} invalido ({s["v"]})'
            if s['t']=='bool' and v not in ('true','false'): return f'{name}: {k}={v}'
    return None
errs=0
F=os.path.join(GEN,'build','granjas','data','granjas','function')
for fn in sorted(os.listdir(F)):
    for i,line in enumerate(open(f'{F}/{fn}'),1):
        line=line.strip()
        if not line: continue
        t=line.split(' ')
        e=None
        if t[0]=='fill': e=chk_block(t[7],fn)
        elif t[0]=='setblock': e=chk_block(t[4],fn)
        m=re.search(r'summon (?:minecraft:)?([a-z_]+)',line)
        if m and m.group(1) not in E: e=f'entidad no existe {m.group(1)}'
        for it in re.findall(r'id:"minecraft:([a-z0-9_]+)"',line):
            if it not in I and it not in E: e=f'item no existe {it}'
        for fe in re.findall(r'replace ([a-z_]+)$',line):
            if fe not in B: e=f'bloque filtro no existe {fe}'
        if e: print(fn,i,e); errs+=1
print('ERRORES:',errs)
