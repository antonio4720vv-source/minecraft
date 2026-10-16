import os; GEN=os.path.dirname(os.path.abspath(__file__))  # carpeta generador/
import os, json, shutil, zipfile
B=os.path.join(GEN,'build','granjas')
shutil.rmtree(B, ignore_errors=True)
F=f'{B}/data/granjas/function'; os.makedirs(F); os.makedirs(f'{B}/data/minecraft/tags/function')
json.dump({"pack":{"description":"Granjas v2: hierro, experiencia, criadero y comercio","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)
json.dump({"values":["granjas:ayuda"]},open(f'{B}/data/minecraft/tags/function/load.json','w'))

def C(x,y,z): return f'~{x} ~{y-1} ~{z}'.replace('~0','~')
class Fn:
    def __init__(s,title): s.L=[f'tellraw @s {{"text":"{title}","color":"yellow"}}']
    def fill(s,a,b,blk,mode=''): s.L.append(f'fill {C(*a)} {C(*b)} {blk}{(" "+mode) if mode else ""}')
    def set(s,p,blk): s.L.append(f'setblock {C(*p)} {blk}')
    def summon(s,e,p,nbt=''): s.L.append(f'summon minecraft:{e} {C(*p)} {nbt}'.rstrip())
    def label(s,p,text,color='gold'):
        s.L.append(f'summon minecraft:text_display {C(*p)} {{billboard:"center",text:{{text:"{text}",color:"{color}",bold:1b}},background:1073741824}}')
    def msg(s,t): s.L.append(f'tellraw @s {{"text":"{t}","color":"green"}}')
    def bed(s,foot,head,color,fac):
        s.set(foot,f'{color}_bed[facing={fac},part=foot]'); s.set(head,f'{color}_bed[facing={fac},part=head]')
    def door_east(s,x,y,z):
        # puerta en pared que corre en Z; se entra caminando hacia el este; (x,y+1,z+1) debe ser pared
        s.set((x,y,z),'iron_door[half=lower,facing=east,hinge=left]'); s.set((x,y+1,z),'iron_door[half=upper,facing=east,hinge=left]')
        s.set((x-1,y+1,z+1),'stone_button[face=wall,facing=west]'); s.set((x+1,y+1,z+1),'stone_button[face=wall,facing=east]')
    def save(s,name):
        open(f'{F}/_{name}.mcfunction','w').write('\n'.join(s.L)+'\n')
        open(f'{F}/{name}.mcfunction','w').write(f'execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_{name}\n')

# ================= HIERRO (elevada, barriles a nivel del suelo) =================
f=Fn('Construyendo granja de HIERRO v2...')
f.fill((-4,0,-3),(19,16,19),'air')
f.fill((-1,0,-1),(18,4,18),'stone_bricks')                  # base solida (no aparecen mobs debajo)
f.fill((-1,5,-1),(18,5,18),'smooth_stone')                  # plataforma de golems
f.fill((-1,6,-1),(18,7,18),'glass','hollow'); f.fill((0,6,0),(17,7,17),'air')
# Agua (probado en Paper 26.2): con fuentes en los 4 bordes, la regla de fuentes infinitas convertia TODA la
# plataforma en agua quieta y los golems se quedaban parados. Ahora: fuentes solo en los bordes oeste y este
# (empujan hacia el canal central x=8..9) y en las 2 puntas del canal (empujan hacia el foso del medio).
f.fill((8,5,0),(9,5,17),'air')                                                   # canal central (1 bloque de hondo)
f.fill((0,6,0),(0,6,17),'water'); f.fill((17,6,0),(17,6,17),'water')
f.fill((8,5,0),(9,5,0),'water'); f.fill((8,5,17),(9,5,17),'water')
f.fill((8,4,8),(9,4,9),'soul_campfire[lit=true]')   # foso: el golem cae ENCIMA de la fogata
# sala de recoleccion a nivel del suelo
f.fill((5,1,5),(12,3,12),'air'); f.fill((0,1,8),(4,2,9),'air')
f.fill((8,3,8),(9,2,9),'hopper[facing=down]'); f.fill((8,1,8),(9,1,9),'barrel[facing=up]')
for p in [(6,0,6),(11,0,11),(6,0,11),(11,0,6),(2,0,8)]: f.set(p,'glowstone')
f.door_east(-1,1,8)
f.label((-2,4,8),'GRANJA DE HIERRO\\nlos barriles estan adentro')
# capsula de aldeanos y zombi
f.fill((5,10,5),(12,10,12),'smooth_stone'); f.fill((5,11,5),(12,12,12),'glass'); f.fill((6,11,6),(11,12,11),'air')
f.fill((5,13,5),(12,13,12),'glass')
# Probado en Paper 26.2: el aldeano solo entra en panico si el zombi esta a menos de 8 bloques
# y lo ve. Antes las camas estaban en el lado opuesto (z=6) y el zombi a z=15: nunca aparecian golems.
# Ahora: camas pegadas al lado del zombi, zombi en una celda de 1 bloque junto a la capsula,
# y una rendija de 1 bloque de alto a la altura de los ojos (nadie cabe por ahi).
for x in (6,8,10): f.bed((x,11,10),(x,11,11),'red','south')
f.fill((6,10,13),(11,10,14),'smooth_stone'); f.fill((6,11,13),(11,12,14),'glass'); f.fill((7,11,13),(10,12,13),'air')
f.fill((6,13,13),(11,13,14),'glass')                          # techo de vidrio: ahi no pueden aparecer golems
f.fill((7,12,12),(10,12,12),'air')                            # rendija para que los aldeanos vean al zombi
f.summon('zombie',(8,11,13),'{PersistenceRequired:1b,CustomName:"Asustador",equipment:{head:{id:"minecraft:carved_pumpkin",count:1}},drop_chances:{head:0.0f}}')
for x in (7,9,10): f.summon('villager',(x,11,9),'{PersistenceRequired:1b,CustomName:"Trabajador del hierro"}')
f.msg('Granja de hierro lista. Entra por la puerta de hierro (boton al lado): los 4 barriles del centro se llenan solos. Empieza despues de la primera noche.')
f.save('hierro')
# arreglo para granjas ya construidas: el jugador se para DENTRO de la puerta de hierro
f=Fn('Arreglando la granja de hierro...')
f.L.append('kill @e[type=iron_golem,distance=..40]')
f.fill((8,5,8),(9,5,9),'air'); f.fill((8,4,8),(9,4,9),'soul_campfire[lit=true]')
f.msg('Arreglada: ahora los golems caen a un foso con fogatas y mueren. Si no estabas parado DENTRO de la puerta de hierro, no funciono: vuelve a intentarlo.')
f.L=[l.replace('~','~',1) for l in f.L]
open(f'{F}/_hierro_arreglar.mcfunction','w').write('\n'.join(f.L)+'\n')
open(f'{F}/hierro_arreglar.mcfunction','w').write('execute align xyz positioned ~1.5 ~ ~-7.5 run function granjas:_hierro_arreglar\n')

# ================= EXPERIENCIA (zona de matar a nivel del suelo) =================
f=Fn('Construyendo granja de EXPERIENCIA v2...')
f.fill((-3,0,-2),(11,20,12),'air'); f.fill((-3,0,-2),(11,0,12),'cobblestone')
f.fill((-1,13,-1),(9,18,9),'cobblestone','hollow')         # cuarto del spawner (arriba, oscuro)
f.fill((0,14,0),(8,14,0),'water')
f.set((4,15,4),'spawner{SpawnData:{entity:{id:"minecraft:zombie"}}}')
f.fill((-2,1,9),(10,3,12),'cobblestone')                   # pasillo del jugador
f.fill((-1,1,7),(9,12,9),'cobblestone')                    # torre de caida
f.fill((0,2,8),(8,13,8),'air')                             # caida de 12 bloques
for x in range(9): f.set((x,14,8),'oak_wall_sign[facing=north]')
f.fill((0,1,8),(8,1,8),'hopper[facing=south]'); f.fill((0,1,9),(8,1,9),'barrel[facing=up]')
f.fill((0,2,9),(8,2,9),'cobblestone_slab[type=bottom]')    # rendija para pegarles
f.fill((-1,1,10),(9,2,11),'air')
for x in (0,4,8): f.set((x,3,11),'glowstone')
for p in [(1,19,1),(4,19,4),(7,19,7),(1,19,7),(7,19,1)]: f.set(p,'torch')
for p in [(-2,1,0),(10,1,0),(4,1,-2),(-2,1,5),(10,1,5)]: f.set(p,'torch')
f.door_east(-2,1,10)
f.label((-3,4,10),'GRANJA DE EXPERIENCIA\\nparate en la mitad del pasillo')
f.msg('Granja de experiencia lista. Entra por la puerta, parate en la MITAD del pasillo mirando a la rendija y pegales a los zombis. El botin cae en los barriles del piso.')
f.save('experiencia')

# ================= CRIADERO (4 adultos, 22 camas, corral de bebes) =================
f=Fn('Construyendo CRIADERO de aldeanos v2...')
f.fill((-1,0,-1),(17,5,11),'air'); f.fill((-1,0,-1),(17,0,11),'grass_block')
f.fill((-1,1,-1),(11,3,11),'glass','hollow'); f.fill((-1,4,-1),(11,4,11),'glass')
for p in [(2,0,4),(8,0,4),(2,0,6),(8,0,6),(5,0,5)]: f.set(p,'glowstone')
for x in range(0,11):
    f.bed((x,1,0),(x,1,1),'white','south'); f.bed((x,1,10),(x,1,9),'white','north')
f.set((11,1,5),'air')                                        # hueco de 1 bloque: solo pasan los bebes
f.fill((11,0,2),(17,4,8),'glass','hollow'); f.fill((12,0,3),(16,0,7),'grass_block')
f.fill((12,1,3),(16,3,7),'air'); f.set((11,1,5),'air'); f.set((11,2,5),'glass')
f.set((14,0,5),'glowstone')
f.fill((17,1,4),(17,3,6),'stone_bricks')
f.set((17,1,5),'iron_door[half=lower,facing=west,hinge=left]'); f.set((17,2,5),'iron_door[half=upper,facing=west,hinge=left]')
f.set((18,2,6),'stone_button[face=wall,facing=east]'); f.set((16,2,6),'stone_button[face=wall,facing=west]')
inv='['+','.join(['{id:"minecraft:bread",count:64}']*8)+']'
for i,(x,z) in enumerate([(3,4),(5,4),(3,6),(5,6)]):
    f.summon('villager',(x,1,z),'{PersistenceRequired:1b,CustomName:"Padre '+str(i+1)+'",Inventory:'+inv+'}')
f.label((18,4,5),'CRIADERO\\nlos bebes salen a este corral')
f.label((5,6,5),'CRIADERO DE ALDEANOS')
f.msg('Criadero listo: 4 adultos con pan y 22 camas. Los bebes pasan solos por el hueco al corral de la derecha; sacalos por la puerta de hierro y llevalos a la sala de comercio.')
f.save('aldeanos')

# ================= SALA DE COMERCIO =================
prof=[('armorer','blast_furnace','Armero'),('butcher','smoker','Carnicero'),('cartographer','cartography_table','Cartografo'),
('cleric','brewing_stand','Clerigo'),('farmer','composter','Granjero'),('fisherman','barrel','Pescador'),('fletcher','fletching_table','Flechero'),
('leatherworker','cauldron','Peletero'),('librarian','lectern','Bibliotecario 1'),('librarian','lectern','Bibliotecario 2'),('librarian','lectern','Bibliotecario 3'),
('mason','stonecutter','Albanil'),('shepherd','loom','Pastor'),('toolsmith','smithing_table','Herrero de herramientas'),('weaponsmith','grindstone','Herrero de armas')]
W=2*len(prof)
f=Fn('Construyendo SALA DE COMERCIO v2...')
f.fill((-4,0,-3),(W+1,6,5),'air'); f.fill((-4,0,-3),(W+1,0,5),'stone_bricks')
f.fill((-2,0,-3),(W,4,4),'stone_bricks'); f.fill((-1,1,2),(W-1,2,3),'air')
for i,(p,ws,name) in enumerate(prof):
    X=2*i
    f.fill((X,1,0),(X,2,0),'air'); f.set((X,2,1),'air'); f.set((X,1,-1),ws); f.set((X,3,2),'glowstone')
    f.summon('villager',(X,1,0),'{PersistenceRequired:1b,Xp:1,CustomName:"'+name+'",CustomNameVisible:1b,VillagerData:{profession:"minecraft:'+p+'",level:1,type:"minecraft:plains"}}')
f.door_east(-2,1,2)
f.label((-3,4,2),'SALA DE COMERCIO\\n15 aldeanos con profesion')
f.msg('Sala de comercio lista: 15 aldeanos (3 bibliotecarios para libros encantados). Cada uno muestra su nombre encima.')
f.save('comercio')

# ================= TODAS EN FILA =================
L=['tellraw @s {"text":"Construyendo las 4 granjas en fila hacia el ESTE (unos 110 bloques). Espera unos segundos...","color":"yellow"}',
 f'fill {C(-4,1,-6)} {C(108,4,-4)} air', f'fill {C(-4,0,-6)} {C(108,0,-4)} stone_bricks']
for x in range(-4,109,8): L.append(f'setblock {C(x,1,-6)} lantern')
L+=['function granjas:_hierro','execute positioned ~30 ~ ~ run function granjas:_experiencia',
    'execute positioned ~52 ~ ~ run function granjas:_aldeanos','execute positioned ~76 ~ ~ run function granjas:_comercio',
    f'summon minecraft:text_display {C(-5,3,-5)} {{billboard:"center",text:{{text:"Hierro -> Experiencia -> Criadero -> Comercio",color:"aqua",bold:1b}}}}',
    'tellraw @s {"text":"Listo: sigue el camino de piedra con faroles hacia el este.","color":"green"}']
open(f'{F}/_todas.mcfunction','w').write('\n'.join(L)+'\n')
open(f'{F}/todas.mcfunction','w').write('execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_todas\n')

H=['tellraw @a {"text":"[Granjas v2] Parate en un terreno PLANO y despejado (borra lo que haya) y usa:","color":"gold"}',
 'tellraw @a {"text":"/function granjas:todas  (las 4 juntas en fila)\\n/function granjas:hierro\\n/function granjas:experiencia\\n/function granjas:aldeanos\\n/function granjas:comercio","color":"aqua"}']
open(f'{F}/ayuda.mcfunction','w').write('\n'.join(H)+'\n')

z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
# chequeo de limite de fill (32768)
import re
for fn in os.listdir(F):
    for line in open(f'{F}/{fn}'):
        m=re.match(r'fill ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*)',line)
        if m:
            v=[int(t) if t else 0 for t in m.groups()]
            vol=(abs(v[3]-v[0])+1)*(abs(v[4]-v[1])+1)*(abs(v[5]-v[2])+1)
            if vol>32768: print('DEMASIADO GRANDE',fn,vol)
print('ok')
