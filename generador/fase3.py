# FASE 3: zona residencial, portales y movilidad
#  - Montana natural (forma irregular, rocas, arboles, flores, arroyo) con la casa grande arriba (2 personas)
#  - Casa en el arbol (2 personas)  - Portal del End y portal del Nether decorados
#  - Caballeriza  - Torre de elitros
# Uso: python fase3.py  -> regenera TODO el datapack (gen6 + fases 1, 2 y 3)
# En el juego: /function granjas:fase3   (construye al ESTE y SUR de donde estas parado)
import os; GEN=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(GEN,'fase2.py'),encoding='utf-8').read())
import math, random

M3='@e[type=minecraft:marker,tag=granjas_f3,limit=1]'
MONT=(35,40); ARBOL=(85,24); CABA=(75,42); TORRE=(112,22); PEND=(113,52); PNETH=(138,52)

# =====================================================================
#  MONTANA NATURAL. Se calcula un mapa de alturas en Python para poner las rocas,
#  los arboles y las flores exactamente sobre la superficie.
#  Cima plana de radio 13 a la altura 16 donde va la casa grande.
# =====================================================================
HT,R0,RTOP=16,29,13
rnd=random.Random(26)
def radio(h,ang):
    base=RTOP+(R0-RTOP)*((HT-h)/HT)**1.3
    if h>=HT-2: return base
    return base*(1+0.10*math.sin(3*ang+h*0.4)+0.06*math.sin(5*ang+1.3))
def mapa_alturas():
    H={}
    for x in range(-R0-4,R0+5):
        for z in range(-R0-4,R0+5):
            d=math.hypot(x,z); a=math.atan2(z,x); h=0
            for k in range(1,HT+1):
                if d<=radio(k,a): h=k
            H[(x,z)]=h
    return H
HM=mapa_alturas()
def montana():
    L=['tellraw @s {"text":"Construyendo MONTANA natural...","color":"yellow"}']
    def fill(a,b,blk,mode=''): L.append(f'fill {C(*a)} {C(*b)} {blk}{(" "+mode) if mode else ""}')
    # capas: se rellena cada fila de cada capa (relleno solido; la piel de arriba queda de pasto)
    for h in range(1,HT+1):
        blk='stone' if h<HT-1 else 'dirt'
        for z in range(-R0-4,R0+5):
            xs=[x for x in range(-R0-4,R0+5) if HM[(x,z)]>=h]
            if not xs: continue
            # tramos continuos
            ini=xs[0]; prev=xs[0]
            for x in xs[1:]+[None]:
                if x is None or x!=prev+1:
                    fill((ini,h,z),(prev,h,z),blk); ini=x
                if x is not None: prev=x
    # piel: pasto arriba de cada columna, con manchas de tierra gruesa, musgo y piedra
    for (x,z),h in HM.items():
        if h==0: continue
        r=rnd.random()
        top='grass_block' if r<0.80 else ('coarse_dirt' if r<0.87 else ('moss_block' if r<0.94 else 'andesite'))
        if h>=HT: top='grass_block'
        L.append(f'setblock {C(x,h,z)} {top}')
    # rocas grandes en la ladera
    for _ in range(14):
        a=rnd.uniform(0,2*math.pi); d=rnd.uniform(15,26); x=round(d*math.cos(a)); z=round(d*math.sin(a))
        h=HM.get((x,z),0)
        if h<2 or (abs(x)<4 and z<0): continue
        b=rnd.choice(['mossy_cobblestone','andesite','stone','cobblestone'])
        fill((x,h,z),(x+1,h+1,z+1),b); L.append(f'setblock {C(x,h+2,z)} {b} keep')
    # arroyo: una fuente de agua que baja por la ladera este
    for i in range(0,10):
        x=14+i; z=4+(i%3==0); h=HM.get((x,z),0)
        if h>0: L.append(f'setblock {C(x,h,z)} water')
    # arboles y flores
    for _ in range(26):
        a=rnd.uniform(0,2*math.pi); d=rnd.uniform(14,R0+3); x=round(d*math.cos(a)); z=round(d*math.sin(a))
        if abs(x)<5 and z<0: continue                       # no tapar la subida
        h=HM.get((x,z),0)
        L.append(f'place feature minecraft:{rnd.choice(["spruce","spruce","birch","fancy_oak","oak"])} {C(x,h+1,z)}')
    for _ in range(70):
        a=rnd.uniform(0,2*math.pi); d=rnd.uniform(3,R0+3); x=round(d*math.cos(a)); z=round(d*math.sin(a))
        if (abs(x)<9 and abs(z)<8) or (abs(x)<4 and z<0): continue
        h=HM.get((x,z),0)
        f=rnd.choice(['short_grass','short_grass','fern','poppy','dandelion','cornflower','oxeye_daisy','azure_bluet','lily_of_the_valley','sweet_berry_bush[age=2]'])
        L.append(f'setblock {C(x,h+1,z)} {f} keep')
    # subida: escalera de piedra musgosa tallada en la ladera norte
    zt=-RTOP
    for i in range(1,HT+1):
        z=zt-(HT-i)-1
        fill((-2,i,z),(2,i+5,z),'air')
        fill((-1,i,z),(1,i,z),'mossy_stone_brick_stairs[facing=south]')
        if i>1: fill((-1,1,z),(1,i-1,z),'stone')
        L.append(f'setblock {C(-2,i,z)} mossy_cobblestone'); L.append(f'setblock {C(2,i,z)} mossy_cobblestone')
        L.append(f'setblock {C(-2,i+1,z)} mossy_cobblestone_wall'); L.append(f'setblock {C(2,i+1,z)} mossy_cobblestone_wall')
        if i%4==0: L.append(f'setblock {C(-2,i+2,z)} lantern'); L.append(f'setblock {C(2,i+2,z)} lantern')
    L.append(f'summon minecraft:text_display {C(0,3,zt-HT-2)} {{billboard:"center",text:{{text:"SUBIDA A LA CASA",color:"gold",bold:1b}},background:1073741824}}')
    return L
W('_montana_n',montana())
W('_montana_casa',['execute positioned ~-8 ~16 ~-6 run function granjas:_casa_grande',
 # la casa grande limpia un poco de cima: se rellena el pasto alrededor
 'tellraw @s {"text":"Montana con casa lista: sube por la escalera del lado norte.","color":"green"}'])
W('montana_natural',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_montana_n','execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_montana_casa'])

# =====================================================================
#  PORTAL DEL NETHER decorado (marco de obsidiana 5x6, portal activo)
# =====================================================================
g=G(0,0)
g.L.append('tellraw @s {"text":"Construyendo PORTAL DEL NETHER decorado...","color":"yellow"}')
g.fill((-8,0,-8),(8,12,8),'air')
g.fill((-8,0,-8),(8,0,8),'blackstone'); g.fill((-6,0,-6),(6,0,6),'polished_blackstone_bricks')
g.fill((-4,0,-3),(4,0,3),'polished_blackstone'); g.fill((-3,0,-1),(3,0,1),'crying_obsidian')
for x,z in [(-7,-7),(7,-7),(-7,7),(7,7),(-5,7),(5,-7)]:
    g.set((x,0,z),'crimson_nylium' if x<0 else 'warped_nylium')
for x,z in [(-7,-6),(-6,-7),(6,7),(7,6)]: g.set((x,0,z),'crimson_nylium' if x<0 else 'warped_nylium')
# marco y portal (eje x, se cruza caminando hacia el norte/sur)
g.fill((-2,1,0),(2,6,0),'obsidian'); g.fill((-1,2,0),(1,5,0),'nether_portal[axis=x]')
for x in (-3,3):
    g.fill((x,1,0),(x,5,0),'polished_blackstone_wall'); g.set((x,6,0),'gilded_blackstone')
g.fill((-3,7,0),(3,7,0),'polished_blackstone_brick_slab[type=bottom]'); g.set((0,7,0),'chiseled_polished_blackstone')
g.set((0,8,0),'soul_campfire[lit=true]')
for x in (-2,2): g.set((x,1,-1),'crying_obsidian'); g.set((x,1,1),'crying_obsidian')
# 4 pilares de basalto con faroles de almas colgando de cadenas
for x,z in [(-6,-6),(6,-6),(-6,6),(6,6)]:
    g.fill((x,1,z),(x,6,z),'polished_basalt'); g.set((x,7,z),'chiseled_nether_bricks')
    g.set((x,8,z),'soul_lantern')
for x,z in [(-6,0),(6,0)]:
    g.fill((x,1,z),(x,3,z),'red_nether_bricks'); g.set((x,4,z),'shroomlight')
# vegetacion del nether en las esquinas
for x,z,p in [(-7,-5,'crimson_fungus'),(-5,-7,'crimson_roots'),(-7,7,'crimson_roots'),(7,-5,'warped_fungus'),(5,-7,'warped_roots'),(7,7,'warped_roots'),(-5,7,'weeping_vines'),(5,7,'twisting_vines')]:
    if p in ('weeping_vines','twisting_vines'): continue
    g.set((x,1,z),p)
g.set((-7,1,-7),'crimson_fungus'); g.set((7,1,-7),'warped_fungus')
# borde de valla de nether
for a,b in [((-8,1,-8),(8,1,-8)),((-8,1,8),(-2,1,8)),((2,1,8),(8,1,8)),((-8,1,-8),(-8,1,8)),((8,1,-8),(8,1,8))]: g.fill(a,b,'nether_brick_fence')
g.fill((-1,1,8),(1,1,8),'air'); g.fill((-1,0,7),(1,0,9),'polished_blackstone_bricks')
g.label((0,10,0),'PORTAL AL NETHER','red')
g.L.append('tellraw @s {"text":"Portal del Nether listo. Lleva armadura de oro para que los piglins no te ataquen.","color":"green"}')
W('_portal_nether',g.L)
W('portal_nether',['execute align xyz positioned ~0.5 ~ ~12.5 run function granjas:_portal_nether'])

# =====================================================================
#  ETAPAS
# =====================================================================
DX0,DX1,DZ0,DZ1=-2,150,-4,74
def limpiar3(ya,yb): return [f'fill {C(xa,ya,DZ0)} {C(xb,yb,DZ1)} air' for xa,xb in chunks(DX0,DX1,28)]
def etapa3(n,body,nxt=None,msg=None,delay='3s'):
    L=([f'tellraw @a {{"text":"[Fase 3] {msg}","color":"yellow"}}'] if msg else [])+body
    W(f'_f3_{n}b',L)
    W(f'_f3_{n}',[f'execute at {M3} run function granjas:_f3_{n}b']+([f'schedule function granjas:_f3_{nxt} {delay} replace'] if nxt else []))
def at(p,fn): return f'execute positioned ~{p[0]} ~ ~{p[1]} run function granjas:{fn}'
W('fase3',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_f3_nueva'])
W('_f3_nueva',['kill @e[type=minecraft:marker,tag=granjas_f3]','summon minecraft:marker ~ ~ ~ {Tags:["granjas_f3"]}','function granjas:_f3_0'])
W('rehacer_fase3',[f'execute unless entity {M3} run tellraw @s {{"text":"No encuentro la Fase 3. Usa /function granjas:fase3 donde la quieras.","color":"red"}}',
                   f'execute at {M3} run function granjas:_f3_0'])
W('_f3_0',[f'execute at {M3} run forceload add ~{DX0} ~{DZ0} ~{DX1} ~{DZ1}',
 'tellraw @a {"text":"[Fase 3] Preparando terreno de 150 x 78 bloques al ESTE y SUR. Tarda unos 40 segundos. No te alejes.","color":"gold"}',
 'schedule function granjas:_f3_1 5s replace'])
# camino principal (norte) con ramales a cada lugar
camino=[f'fill {C(DX0,0,0)} {C(DX1,0,2)} dirt_path']+[f'setblock {C(x,1,-1)} lantern' for x in range(0,DX1,10)]
for x,z in [(MONT[0],MONT[1]-RTOP-HT-2),(ARBOL[0]-12,ARBOL[1]),(CABA[0]+26,CABA[1]+6),(TORRE[0]+4,TORRE[1]-13),(PEND[0],PEND[1]-9),(PNETH[0],PNETH[1]-9)]:
    if (x,z)==(ARBOL[0]-12,ARBOL[1]):
        camino.append(f'fill {C(x,0,3)} {C(x+1,0,z)} dirt_path'); camino.append(f'fill {C(x,0,z)} {C(x+9,0,z+1)} dirt_path')
    else: camino.append(f'fill {C(x-1,0,3)} {C(x+1,0,z)} dirt_path')
for px,pz in (PEND,PNETH): camino.append(f'fill {C(px-1,1,pz-8)} {C(px+1,1,pz-8)} air')       # entrada por el norte
camino.append(f'fill {C(CABA[0]+26,0,3)} {C(CABA[0]+27,0,CABA[1]+6)} dirt_path')
etapa3(1,[f'execute positioned {C(DX0,-6,DZ0)} run kill @e[type=!minecraft:player,tag=!granjas_f3,tag=!granjas_f2,tag=!granjas_f1,tag=!granjas_mega,tag=!granjas_hub,dx={DX1-DX0},dy=90,dz={DZ1-DZ0}]']
      +limpiar3(1,10)+limpiar3(11,20)+limpiar3(21,30)+limpiar3(31,40),'2','Limpiando terreno (1/2)...')
etapa3(2,limpiar3(41,50)+limpiar3(51,60)+limpiar3(61,70)+limpiar3(71,80)+[f'fill {C(xa,0,DZ0)} {C(xb,0,DZ1)} grass_block' for xa,xb in chunks(DX0,DX1,28)]
      +[f'fill {C(xa,-3,DZ0)} {C(xb,-1,DZ1)} dirt' for xa,xb in chunks(DX0,DX1,28)]+['kill @e[type=minecraft:item,distance=..200]'],'3','Limpiando terreno (2/2)...')
etapa3(3,[at(MONT,'_montana_n')],'4','Montana natural...','4s')
etapa3(4,[at(MONT,'_montana_casa'),at(ARBOL,'_arbol')],'5','Casa grande en la cima y casa en el arbol...')
etapa3(5,[at(CABA,'_caballeriza'),at(TORRE,'_torre_elitros')],'6','Caballeriza y torre de elitros...')
etapa3(6,[at(PEND,'_portal_end'),at(PNETH,'_portal_nether')]+camino+[f'setblock {C(x,1,z)} light[level=15] keep' for x in range(DX0+3,DX1,8) for z in range(DZ0+3,DZ1,8)]
      +['kill @e[type=minecraft:item,distance=..200]',
 'tellraw @a {"text":"[Fase 3] LISTA! Sigue el camino de tierra del norte: montana con la casa (oeste), casa en el arbol, caballeriza, torre de elitros y los portales del End y del Nether (este).","color":"green"}'],
 None,'Portales del End y del Nether y caminos...')

W('lista',['tellraw @s {"text":"--- FASES ---\\n/function granjas:fase1   (torre de hierro + criaderos y comercio)\\n/function granjas:fase2   (establo, invernadero, bambu, sandia y calabaza)\\n/function granjas:fase3   (montana con casa, casa del arbol, portales, caballeriza, torre de elitros)\\n/function granjas:rehacer_fase1 | rehacer_fase2 | rehacer_fase3\\n--- SUELTAS (donde estes) ---\\nmontana_natural, arbol, portal_end, portal_nether, caballeriza, torre_elitros, casa_grande, hierro, aldeanos, comercio, bambu, sandia, calabaza, cofres, fuente\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, hierro_vision","color":"aqua"}'])
z=os.path.join(GEN,'build','granjas_datapack.zip')
json.dump({"pack":{"description":"Granjas v10: fases 1, 2 y 3","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)

if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
bad=0
for fn in os.listdir(F):
    for i,line in enumerate(open(f'{F}/{fn}'),1):
        line=line.rstrip('\n')
        if not line: continue
        if line.count('{')!=line.count('}') or line.count('[')!=line.count(']'): print('LLAVES',fn,i,line[:100]); bad=1
        m=re.match(r'fill ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*)',line)
        if m:
            v=[int(t) if t else 0 for t in m.groups()]
            vol=(abs(v[3]-v[0])+1)*(abs(v[4]-v[1])+1)*(abs(v[5]-v[2])+1)
            if vol>32768: print('GRANDE',fn,vol,line[:60]); bad=1
print('FASE 3:', 'OK' if not bad else 'HAY ERRORES', '->', z)
