import os; GEN=os.path.dirname(os.path.abspath(__file__))  # carpeta generador/
exec(open(os.path.join(GEN,'gen3.py'),encoding='utf-8').read().split("# ================= TODAS / NUEVAS")[0])

def W(name, lines):
    open(f'{F}/{name}.mcfunction','w').write('\n'.join(lines)+'\n')


# ---------- CASA DE MADERA PARA 2 ----------
f=Fn('Construyendo CASA de madera...')
f.fill((-1,0,-1),(13,12,12),'air'); f.fill((-1,0,-1),(13,0,12),'grass_block')
f.fill((0,0,0),(12,0,10),'cobblestone'); f.fill((1,0,1),(11,0,9),'oak_planks')
f.fill((1,1,1),(11,4,9),'oak_planks','hollow')
for x,z in [(1,1),(11,1),(1,9),(11,9)]: f.fill((x,1,z),(x,4,z),'oak_log')
f.fill((0,4,0),(12,4,10),'spruce_planks'); f.fill((1,4,1),(11,4,9),'oak_planks')
for k in range(5):
    y=5+k
    f.fill((0,y,k),(12,y,k),'spruce_stairs[facing=south]'); f.fill((0,y,10-k),(12,y,10-k),'spruce_stairs[facing=north]')
    if k+1<=9-k: f.fill((1,y,k+1),(1,y,9-k),'oak_planks'); f.fill((11,y,k+1),(11,y,9-k),'oak_planks')
f.fill((0,10,5),(12,10,5),'spruce_slab[type=bottom]')
for x in (3,4,8,9):
    f.fill((x,2,1),(x,3,1),'glass_pane[east=true,west=true]'); f.fill((x,2,9),(x,3,9),'glass_pane[east=true,west=true]')
for z in (4,6):
    f.fill((1,2,z),(1,3,z),'glass_pane[north=true,south=true]'); f.fill((11,2,z),(11,3,z),'glass_pane[north=true,south=true]')
f.set((6,1,9),'iron_door[half=lower,facing=north,hinge=left]'); f.set((6,2,9),'iron_door[half=upper,facing=north,hinge=left]')
f.set((7,2,10),'stone_button[face=wall,facing=south]'); f.set((7,2,8),'stone_button[face=wall,facing=north]')
f.fill((5,0,10),(7,0,12),'cobblestone'); f.set((4,1,10),'lantern'); f.set((8,1,10),'lantern')
f.bed((2,1,3),(2,1,2),'red','north'); f.bed((4,1,3),(4,1,2),'blue','north')
f.set((3,1,2),'oak_planks'); f.set((3,2,2),'lantern')
f.fill((10,1,2),(10,2,4),'barrel[facing=west]')
f.set((10,1,5),'crafting_table'); f.set((10,1,6),'furnace[facing=west]'); f.set((10,1,7),'smoker[facing=west]')
f.set((10,1,8),'anvil[facing=north]')
f.set((2,1,8),'enchanting_table'); f.fill((2,1,6),(2,2,6),'bookshelf'); f.fill((3,1,8),(4,2,8),'bookshelf') if False else None
f.set((2,1,7),'bookshelf'); f.set((3,1,8),'bookshelf')
f.fill((5,1,4),(7,1,6),'red_carpet')
f.set((5,3,5),'lantern[hanging=true]'); f.set((8,3,5),'lantern[hanging=true]'); f.set((3,3,7),'lantern[hanging=true]')
f.set((7,1,2),'oak_fence'); f.set((7,2,2),'flower_pot')
f.label((6,4,11),'CASA')
f.msg('Casa lista: 2 camas, 6 barriles, mesa de crafteo, horno, ahumador, yunque y mesa de encantar. Puerta de hierro con boton (los zombis no la rompen).')
f.save('casa')

# posiciones de cada granja alrededor de la plaza (x, z)
POS={'hierro':(-48,-30),'experiencia':(-20,-26),'aldeanos':(-2,-24),'mobs':(24,-34),
     'comercio':(-48,12),'cana':(-10,13),'comida':(10,12),'hornos':(30,12),'casa':(48,-14)}
X0,X1,Z0,Z1=-58,64,-40,22
HUB='@e[type=minecraft:marker,tag=granjas_hub,limit=1]'

# ---------- APLANAR ----------
W('aplanar',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_aplanar'])
W('_aplanar',[
 'kill @e[type=minecraft:marker,tag=granjas_hub]',
 'summon minecraft:marker ~ ~ ~ {Tags:["granjas_hub"]}',
 f'forceload add ~{X0} ~{Z0} ~{X1} ~{Z1}',
 'tellraw @s {"text":"Aplanando un terreno de 110 x 60 bloques alrededor tuyo... (espera 5 segundos)","color":"yellow"}',
 'schedule function granjas:_aplanar2 5s replace'])
L=[]
def chunks(a,b,step=30):
    r=[];s=a
    while s<=b: r.append((s,min(s+step-1,b))); s+=step
    return r
for xa,xb in chunks(X0,X1):
    for za,zb in chunks(Z0,Z1):
        for ya,yb in [(1,18),(19,36),(37,45)]:
            L.append(f'fill {C(xa,ya,za)} {C(xb,yb,zb)} air')
        L.append(f'fill {C(xa,0,za)} {C(xb,0,zb)} grass_block')
        L.append(f'fill {C(xa,-3,za)} {C(xb,-1,zb)} dirt')
L.append('kill @e[type=minecraft:item,distance=..90]')
L.append('tellraw @a {"text":"Terreno aplanado. Ahora escribe: /function granjas:construir","color":"green"}')
W('_aplanar3',L)
W('_aplanar2',[f'execute at {HUB} run function granjas:_aplanar3'])

# ---------- CONSTRUIR TODO ----------
L=['tellraw @a {"text":"Construyendo las 8 granjas alrededor de la plaza...","color":"yellow"}',
   f'fill {C(X0,0,-3)} {C(X1-2,0,3)} stone_bricks', f'fill {C(-4,0,-6)} {C(4,0,6)} polished_andesite']
for x in range(X0,X1-1,8): L.append(f'setblock {C(x,1,-3)} lantern'); L.append(f'setblock {C(x,1,3)} lantern')
for n,(ox,oz) in POS.items(): L.append(f'execute positioned ~{ox} ~ ~{oz} run function granjas:_{n}')
L.append(f'summon minecraft:text_display {C(0,4,0)} {{billboard:"center",text:{{text:"PLAZA DE GRANJAS\\nNorte: hierro, experiencia, criadero, mobs\\nSur: comercio, cana, comida, hornos\\nEste: la CASA",color:"aqua",bold:1b}}}}')
L.append('function granjas:respaldo_on')
L.append('tellraw @a {"text":"Listo! Las 8 granjas estan alrededor de la plaza. El modo respaldo esta ACTIVADO.","color":"green"}')
W('_construir',L)
W('construir',[
 f'execute unless entity {HUB} run tellraw @s {{"text":"Primero usa /function granjas:aplanar","color":"red"}}',
 f'execute at {HUB} run function granjas:_construir'])

# ---------- MODO RESPALDO (produce cada minuto en los cofres) ----------
def P(n,x,y,z): ox,oz=POS[n]; return C(ox+x,y,oz+z)
L=[]
for _ in range(2): L.append(f'loot insert {P("hierro",8,1,8)} loot minecraft:entities/iron_golem')
L.append(f'loot insert {P("hierro",9,1,9)} loot minecraft:entities/iron_golem')
for _ in range(8): L.append(f'loot insert {P("cana",-1,1,0)} loot minecraft:blocks/sugar_cane')
for _ in range(2): L.append(f'loot insert {P("comida",-1,1,1)} loot minecraft:blocks/melon'); L.append(f'loot insert {P("comida",-1,1,1)} loot minecraft:blocks/pumpkin')
for m in ['creeper','creeper','skeleton','skeleton','zombie','spider']:
    L.append(f'loot insert {P("mobs",8,1,10)} loot minecraft:entities/{m}')
for m in ['zombie','zombie']: L.append(f'loot insert {P("experiencia",4,1,9)} loot minecraft:entities/{m}')
L.append('scoreboard players add #t granjas 1')
L.append(f'execute positioned {P("aldeanos",12,1,3)} store result score #b granjas if entity @e[type=minecraft:villager,dx=4,dy=3,dz=4]')
L.append(f'execute if score #t granjas matches 5.. if score #b granjas matches ..7 run summon minecraft:villager {P("aldeanos",14,1,5)} {{Age:-24000}}')
L.append('execute if score #t granjas matches 5.. run scoreboard players set #t granjas 0')
W('_producir',L)
W('producir',['schedule function granjas:producir 60s replace',
              f'execute if score #on granjas matches 1 at {HUB} run function granjas:_producir'])
W('respaldo_on',['scoreboard players set #on granjas 1','schedule function granjas:producir 60s replace',
 'tellraw @a {"text":"Modo respaldo ACTIVADO: cada minuto llegan hierro, cana, melones, calabazas y polvora a los cofres, y cada 5 minutos un bebe aldeano al corral.","color":"green"}'])
W('respaldo_off',['scoreboard players set #on granjas 0',
 'tellraw @a {"text":"Modo respaldo DESACTIVADO: ahora las granjas solo funcionan con sus mecanismos normales.","color":"yellow"}'])
W('quitar_carga',['forceload remove all','tellraw @s {"text":"Las granjas ya no se mantienen cargadas cuando te alejas.","color":"yellow"}'])

# ---------- AYUDA / LOAD ----------
W('ayuda',[
 'scoreboard objectives add granjas dummy',
 'execute unless score #on granjas matches 0..1 run scoreboard players set #on granjas 0',
 'schedule function granjas:producir 60s replace',
 'tellraw @a {"text":"[Granjas v5] Pasos: 1) /function granjas:aplanar   2) /function granjas:construir","color":"gold"}'])
json.dump({"pack":{"description":"Granjas v5: aplanar + 8 granjas en una plaza","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)

# limpiar comandos viejos de fila
for n in ['todas','_todas','nuevas','_nuevas']:
    p=f'{F}/{n}.mcfunction'
    if os.path.exists(p): os.remove(p)

z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
import re
bad=0
for fn in os.listdir(F):
    for line in open(f'{F}/{fn}'):
        m=re.match(r'fill ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*)',line)
        if m:
            v=[int(t) if t else 0 for t in m.groups()]
            vol=(abs(v[3]-v[0])+1)*(abs(v[4]-v[1])+1)*(abs(v[5]-v[2])+1)
            if vol>32768: print('DEMASIADO GRANDE',fn,vol); bad=1
print('ok' if not bad else 'ERR', sorted(x for x in os.listdir(F) if not x.startswith('_')))

# ---------- ARREGLAR (vagones + cofres -> barriles) ----------
L=[f'kill @e[type=minecraft:hopper_minecart,distance=..90]']
def to_barrel(n,x,y,z,fac):
    p=P(n,x,y,z)
    return [f'data remove storage granjas:tmp items',
            f'data modify storage granjas:tmp items set from block {p} Items',
            f'setblock {p} barrel[facing={fac}]',
            f'data modify block {p} Items set from storage granjas:tmp items']
L+=to_barrel('cana',-1,1,0,'west')+[f'setblock {P("cana",-1,2,0)} stone_bricks']
for x in range(12): L.append(f'summon minecraft:hopper_minecart {P("cana",x,2,0)}')
L+=to_barrel('comida',-1,1,1,'west')+[f'setblock {P("comida",-1,2,1)} stone_bricks',f'setblock {P("comida",-1,2,0)} stone_bricks']
for x in range(12):
    L.append(f'summon minecraft:hopper_minecart {P("comida",x,2,0)}'); L.append(f'summon minecraft:hopper_minecart {P("comida",x,2,1)}')
L+=to_barrel('hornos',-1,1,0,'west')+[f'setblock {P("hornos",-1,2,0)} stone_bricks']
L+=to_barrel('mobs',8,1,10,'south')+to_barrel('mobs',9,1,10,'south')
L.append('tellraw @a {"text":"Arreglado: vagones de vuelta en su lugar y los cofres cambiados por barriles (se abren aunque tengan un bloque encima). Las cosas que tenian se conservaron.","color":"green"}')
W('_arreglar',L)
W('arreglar',[f'execute unless entity {HUB} run tellraw @s {{"text":"No encuentro la plaza de granjas (usaste granjas:construir?)","color":"red"}}',
              f'execute at {HUB} run function granjas:_arreglar'])
W('reconstruir',[f'execute unless entity {HUB} run tellraw @s {{"text":"No encuentro la plaza de granjas. Usa /function granjas:aplanar donde quieras construir.","color":"red"}}',
 f'execute at {HUB} run function granjas:_reconstruir'])
W('_reconstruir',[
 'tellraw @a {"text":"Borrando todo lo construido en la plaza y reconstruyendo en 5 segundos...","color":"yellow"}',
 f'forceload add ~{X0} ~{Z0} ~{X1} ~{Z1}',
 f'execute positioned {C(X0,-6,Z0)} run kill @e[type=!minecraft:player,tag=!granjas_hub,dx={X1-X0},dy=60,dz={Z1-Z0}]',
 'schedule function granjas:_reconstruir2 5s replace'])
W('_reconstruir2',[f'execute at {HUB} run function granjas:_aplanar3',
 f'execute at {HUB} run function granjas:_construir',
 f'execute at {HUB} positioned {C(X0,-6,Z0)} run kill @e[type=minecraft:item,dx={X1-X0},dy=60,dz={Z1-Z0}]'])
z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
print('listo v5')

# ---------- SANDIA SOLA ----------
src=open(f'{F}/_comida.mcfunction').read().replace('pumpkin_stem','melon_stem').replace('MELONES y CALABAZAS','SANDIAS').replace('MELONES Y CALABAZAS','SANDIAS')
open(f'{F}/_sandia.mcfunction','w').write(src)
open(f'{F}/sandia.mcfunction','w').write('execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_sandia\n')
z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
print('sandia ok')
