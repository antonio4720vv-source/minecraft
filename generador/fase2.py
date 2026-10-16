# FASE 2: establo de 10 granjas de animales + invernadero de 10 cultivos
#         + 10 granjas de bambu y 10 de sandia/calabaza en un pabellon ordenado.
# Uso: python fase2.py  -> regenera TODO el datapack (gen6 + fase 1 + fase 2) en build/granjas_datapack.zip
# En el juego: /function granjas:fase2   (construye al ESTE y SUR de donde estas parado)
import os; GEN=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(GEN,'fase1.py'),encoding='utf-8').read())

M2='@e[type=minecraft:marker,tag=granjas_f2,limit=1]'
AX,AZ=4,4        # establo de animales
CX,CZ=4,24       # invernadero de cultivos
PX,PZ=72,6       # pabellon de bambu (filas 1-2) y sandia/calabaza (filas 3-4)

# =====================================================================
#  ESTABLO: 2 pisos x 5 corrales = 10 granjas de animales
#  Corral 9x9 de pasto con valla y portera hacia el pasillo (lado sur).
#  En el pasillo, junto a cada portera, un barril con la comida para criarlos.
# =====================================================================
ANIMALES=[  # (entidad, nombre, cantidad, nbt extra, comida en el barril)
 ('cow','VACAS',4,'',[('wheat',64),('bucket',4)]),
 ('sheep','OVEJAS',4,'',[('wheat',64),('shears',1)]),
 ('pig','CERDOS',4,'',[('carrot',64)]),
 ('chicken','GALLINAS',6,'',[('wheat_seeds',64)]),
 ('rabbit','CONEJOS',4,'',[('carrot',64),('dandelion',32)]),
 ('goat','CABRAS',3,'',[('wheat',64),('bucket',2)]),
 ('mooshroom','CHAMPINACAS',3,'',[('wheat',64),('bowl',16)]),
 ('llama','LLAMAS',3,',Tame:1b',[('hay_block',32),('lead',4)]),
 ('armadillo','ARMADILLOS',3,'',[('spider_eye',32),('brush',1)]),
 ('bee','ABEJAS',4,'',[('glass_bottle',32),('shears',1)]),
]
FB=[0,6]; TOPA=12; LA=50      # pisos del establo y largo
def establo():
    g=G(AX,AZ)
    g.fill((-1,0,-1),(LA,0,13),'stone_bricks')
    for b in FB:
        if b: g.fill((-1,b,-1),(LA,b,13),'stone_bricks')
        g.fill((0,b+1,0),(LA-1,b+5,12),'air')
        g.walls(-1,LA,b+1,b+5,-1,13,'glass')
        for x in range(-1,LA+1,10):
            for z in (-1,13): g.fill((x,b+1,z),(x,b+5,z),'stripped_spruce_log')
        g.fill((0,b,10),(LA-1,b,12),'spruce_planks')                               # pasillo
        for x in range(4,LA,8): g.set((x,b+4,11),'light[level=15]')
    g.fill((-1,TOPA,-1),(LA,TOPA,13),'spruce_planks')
    for x in range(-1,LA+1,5):
        for z in (-1,13): g.set((x,TOPA+1,z),'lantern')
    g.fill((LA,1,11),(LA,2,11),'air')                                               # entrada (lado este)
    g.set((LA+1,1,10),'lantern'); g.set((LA+1,1,12),'lantern')
    g.fill((0,1,12),(0,TOPA-1,12),'ladder[facing=east]')                          # escalera entre pisos
    g.label((LA+2,4,11),'ESTABLO\\n10 granjas de animales\\nescalera adentro (oeste)')
    return g.L
def corrales(piso):
    g=G(AX,AZ); b=FB[piso]
    for i in range(5):
        ent,name,n,extra,comida=ANIMALES[piso*5+i]; x0=10*i
        g.fill((x0,b,0),(x0+8,b,8),'grass_block')
        g.fill((x0+9,b+1,0),(x0+9,b+1,9),'oak_fence')                              # separacion
        g.fill((x0,b+1,9),(x0+8,b+1,9),'oak_fence'); g.set((x0+4,b+1,9),'oak_fence_gate[facing=south]')
        g.set((x0,b+1,0),'hay_block'); g.set((x0+8,b+1,0),'water_cauldron[level=3]')
        for p in [(x0+2,b+4,2),(x0+6,b+4,6),(x0+2,b+4,6),(x0+6,b+4,2)]: g.set(p,'light[level=15]')
        if ent=='bee':
            for x in (x0+2,x0+6): g.set((x,b+1,0),'beehive[facing=south,honey_level=5]')
            for x in range(x0+1,x0+8,2):
                for z in (3,5,7): g.set((x,b+1,z),'cornflower' if (x+z)%4 else 'poppy')
        if ent=='mooshroom': g.fill((x0,b,0),(x0+8,b,8),'mycelium')
        for k in range(n):
            g.summon(ent,(x0+2+k%3*2,b+1,3+k//3*2),'{PersistenceRequired:1b'+extra+'}')
        items=','.join(f'{{Slot:{s}b,id:"minecraft:{it}",count:{c}}}' for s,(it,c) in enumerate(comida))
        g.set((x0+5,b+1,10),f'barrel[facing=up]{{Items:[{items}]}}')
        g.label((x0+4,b+4,5),name,'yellow')
    return g.L

# =====================================================================
#  INVERNADERO: 10 parcelas de 9x9 (2 filas de 5), techo de vidrio y luces.
# =====================================================================
LC,ZC=54,21   # medidas del invernadero
def parcela(g,x0,z0,tipo):
    g.fill((x0,0,z0),(x0+8,0,z0+8),'dirt')
    if tipo in ('wheat','carrots','potatoes','beetroots'):
        edad=3 if tipo=='beetroots' else 7
        g.fill((x0,0,z0),(x0+8,0,z0+8),'farmland[moisture=7]'); g.set((x0+4,0,z0+4),'water')
        g.fill((x0,1,z0),(x0+8,1,z0+8),f'{tipo}[age={edad}]'); g.set((x0+4,1,z0+4),'lily_pad')
    elif tipo=='sweet_berry_bush':
        g.fill((x0,0,z0),(x0+8,0,z0+8),'grass_block')
        for z in range(z0,z0+9,2): g.fill((x0,1,z),(x0+8,1,z),'sweet_berry_bush[age=3]')
    elif tipo=='glow_berries':
        g.fill((x0,0,z0),(x0+8,0,z0+8),'moss_block')
        for x in range(x0,x0+9,2):
            for z in range(z0,z0+9,2):
                g.set((x,5,z),'jungle_planks'); g.set((x,4,z),'cave_vines_plant[berries=true]'); g.set((x,3,z),'cave_vines[berries=true,age=25]')
    elif tipo=='cocoa':
        g.fill((x0,0,z0),(x0+8,0,z0+8),'grass_block')
        for x in (x0+1,x0+4,x0+7):
            for z in (z0+1,z0+4,z0+7):
                g.fill((x,1,z),(x,3,z),'jungle_log')
                for y in (1,2,3):
                    g.set((x,y,z-1),'cocoa[age=2,facing=south]'); g.set((x,y,z+1),'cocoa[age=2,facing=north]')
    elif tipo=='sugar_cane':
        g.fill((x0,0,z0),(x0+8,0,z0+8),'sand')
        for z in (z0+1,z0+4,z0+7): g.fill((x0,0,z),(x0+8,0,z),'water')
        for z in (z0,z0+2,z0+3,z0+5,z0+6,z0+8): g.fill((x0,1,z),(x0+8,2,z),'sugar_cane')
    elif tipo in ('red_mushroom','brown_mushroom'):
        g.fill((x0,0,z0),(x0+8,0,z0+8),'mycelium')
        for x in range(x0,x0+9):
            for z in range(z0,z0+9):
                if (x+z)%2==0: g.set((x,1,z),tipo)
CULTIVOS=[('wheat','TRIGO','wheat_seeds'),('carrots','ZANAHORIAS','carrot'),('potatoes','PAPAS','potato'),
 ('beetroots','REMOLACHAS','beetroot_seeds'),('sweet_berry_bush','BAYAS DULCES','sweet_berries'),
 ('glow_berries','BAYAS LUMINOSAS','glow_berries'),('cocoa','CACAO','cocoa_beans'),('sugar_cane','CANA DE AZUCAR','sugar_cane'),
 ('red_mushroom','HONGOS ROJOS','red_mushroom'),('brown_mushroom','HONGOS MARRONES','brown_mushroom')]
def invernadero():
    g=G(CX,CZ)
    g.fill((-2,0,-2),(LC,0,ZC),'stone_bricks'); g.fill((-1,1,-1),(LC-1,6,ZC-1),'air')
    g.walls(-2,LC,1,5,-2,ZC,'glass'); g.fill((-2,6,-2),(LC,6,ZC),'glass')
    for x in range(-2,LC+1,8):
        for z in (-2,ZC): g.fill((x,1,z),(x,6,z),'stripped_birch_log')
    for i,(tipo,name,semilla) in enumerate(CULTIVOS):
        x0=(i%5)*11; z0=(i//5)*11
        parcela(g,x0,z0,tipo)
        g.set((x0-1,1,z0-1),f'barrel[facing=up]{{Items:[{{Slot:0b,id:"minecraft:{semilla}",count:64}},{{Slot:1b,id:"minecraft:bone_meal",count:64}}]}}')
        g.label((x0+4,4,z0+4),name,'yellow')
    for x in range(0,LC,5):
        for z in (-1,9,ZC-1):
            g.L.append(f'setblock {g.p(x,5,z)} light[level=15] keep')
    g.fill((-2,1,9),(-2,2,10),'air'); g.fill((LC,1,9),(LC,2,10),'air')               # puertas oeste y este
    g.label((-3,4,10),'INVERNADERO\\n10 cultivos - barril de semillas en cada esquina')
    return g.L

# =====================================================================
#  PABELLON: 4 filas x 5 granjas automaticas (probadas en 26.2: piston + observador
#  + vagonetas tolva). Filas 1-2: BAMBU. Fila 3: SANDIA. Fila 4: CALABAZA.
#  El barril de salida de cada granja esta en su lado oeste.
# =====================================================================
FN=f'{F}/_cana.mcfunction'
src=open(FN).read()
bam=src.replace('sugar_cane','bamboo').replace('CANA DE AZUCAR','BAMBU').replace('go_cana','go_bambu').replace('Construyendo granja de','Construyendo granja de')
bam=bam.replace('cuando la cana crece 3 bloques','cuando el bambu crece 3 bloques').replace('la cana','el bambu')
open(f'{F}/_bambu.mcfunction','w').write(bam)
open(f'{F}/bambu.mcfunction','w').write('execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_bambu\n')
src=open(f'{F}/_comida.mcfunction').read()
cal=src.replace('melon_stem','pumpkin_stem').replace('MELONES y CALABAZAS','CALABAZAS').replace('MELONES Y CALABAZAS','CALABAZAS').replace('go_comida','go_calabaza')
open(f'{F}/_calabaza.mcfunction','w').write(cal)
open(f'{F}/calabaza.mcfunction','w').write('execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_calabaza\n')
FILAS=[('bambu',0),('bambu',9),('sandia',18),('calabaza',27)]
def pabellon_piso():
    g=G(PX,PZ)
    g.fill((-5,0,-6),(84,0,32),'polished_andesite')
    g.label((-6,4,13),'PABELLON\\nfilas 1-2: BAMBU | 3: SANDIA | 4: CALABAZA\\nbarriles en el lado oeste de cada granja','aqua')
    return g.L
def pabellon(filas):
    L=[]
    for n,z in filas:
        for c in range(5): L.append(f'execute positioned ~{PX+c*17} ~ ~{PZ+z} run function granjas:_{n}')
    return L

# respaldo: el bambu y la calabaza tambien producen aunque falle la mecanica
with open(f'{F}/_producir.mcfunction','a') as fh:
    fh.write('execute as @e[type=minecraft:marker,tag=go_bambu] at @s run loot insert ~ ~ ~ loot minecraft:blocks/bamboo\n'*4)
    fh.write('execute as @e[type=minecraft:marker,tag=go_calabaza] at @s run loot insert ~ ~ ~ loot minecraft:blocks/pumpkin\n'*2)

# =====================================================================
#  ETAPAS
# =====================================================================
BX0,BX1,BZ0,BZ1=-2,160,-4,48
def limpiar2(ya,yb): return [f'fill {C(xa,ya,BZ0)} {C(xb,yb,BZ1)} air' for xa,xb in chunks(BX0,BX1,30)]
def etapa2(n,body,nxt=None,msg=None,delay='3s'):
    L=([f'tellraw @a {{"text":"[Fase 2] {msg}","color":"yellow"}}'] if msg else [])+body
    W(f'_f2_{n}b',L)
    W(f'_f2_{n}',[f'execute at {M2} run function granjas:_f2_{n}b']+([f'schedule function granjas:_f2_{nxt} {delay} replace'] if nxt else []))
W('fase2',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_f2_nueva'])
W('_f2_nueva',['kill @e[type=minecraft:marker,tag=granjas_f2]','summon minecraft:marker ~ ~ ~ {Tags:["granjas_f2"]}','function granjas:_f2_0'])
W('rehacer_fase2',[f'execute unless entity {M2} run tellraw @s {{"text":"No encuentro la Fase 2. Usa /function granjas:fase2 donde la quieras.","color":"red"}}',
                   f'execute at {M2} run function granjas:_f2_0'])
W('_f2_0',[f'execute at {M2} run forceload add ~{BX0} ~{BZ0} ~{BX1} ~{BZ1}',
 'tellraw @a {"text":"[Fase 2] Preparando terreno de 160 x 50 bloques al ESTE y SUR. Tarda unos 30 segundos. No te alejes.","color":"gold"}',
 'schedule function granjas:_f2_1 5s replace'])
etapa2(1,[f'execute positioned {C(BX0,-6,BZ0)} run kill @e[type=!minecraft:player,tag=!granjas_f2,tag=!granjas_f1,tag=!granjas_mega,tag=!granjas_hub,dx={BX1-BX0},dy=40,dz={BZ1-BZ0}]']
      +limpiar2(1,20)+limpiar2(21,40)+[f'fill {C(xa,0,BZ0)} {C(xb,0,BZ1)} grass_block' for xa,xb in chunks(BX0,BX1,30)]
      +[f'fill {C(xa,-3,BZ0)} {C(xb,-1,BZ1)} dirt' for xa,xb in chunks(BX0,BX1,30)]
      +[f'fill {C(BX0,0,0)} {C(BX1,0,2)} stone_bricks',f'fill {C(0,0,BZ0)} {C(2,0,BZ1)} stone_bricks',f'fill {C(0,0,20)} {C(PX-5,0,22)} stone_bricks']
      +['kill @e[type=minecraft:item,distance=..200]'],'2','Limpiando terreno...')
etapa2(2,establo()+corrales(0)+corrales(1),'3','Establo con 10 granjas de animales...')
etapa2(3,invernadero(),'4','Invernadero con 10 cultivos...')
etapa2(4,pabellon_piso()+pabellon(FILAS[:2]),'5','10 granjas de bambu...','4s')
etapa2(5,pabellon(FILAS[2:])+[f'setblock {C(PX+c*17-2,1,PZ+z)} light[level=15] keep' for c in range(6) for z in range(-4,33,4)]+['kill @e[type=minecraft:item,distance=..200]','function granjas:respaldo_on',
 'tellraw @a {"text":"[Fase 2] LISTA! Establo (10 animales, 2 pisos), invernadero (10 cultivos) y pabellon (10 bambu + 5 sandia + 5 calabaza, barriles al oeste de cada granja).","color":"green"}'],
 None,'10 granjas de sandia y calabaza...')

W('lista',['tellraw @s {"text":"--- FASES ---\\n/function granjas:fase1   (torre de hierro + criaderos y comercio)\\n/function granjas:fase2   (establo, invernadero, bambu, sandia y calabaza)\\n/function granjas:rehacer_fase1 | rehacer_fase2\\n--- SUELTAS (donde estes) ---\\nhierro, aldeanos, comercio, bambu, sandia, calabaza, cana, comida, hornos, mobs, animales, casa_grande, montana, portal_end, cofres, torre_elitros, caballeriza, arbol, fuente\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, hierro_vision","color":"aqua"}'])
json.dump({"pack":{"description":"Granjas v9: fase 1 + fase 2 (animales, cultivos, bambu, sandia y calabaza)","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)

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
print('FASE 2:', 'OK' if not bad else 'HAY ERRORES', '->', z)
