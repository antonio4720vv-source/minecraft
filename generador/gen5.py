import os; GEN=os.path.dirname(os.path.abspath(__file__))  # carpeta generador/
exec(open(os.path.join(GEN,'gen4.py'),encoding='utf-8').read())
import math

# ===================== GRANJA DE ANIMALES =====================
f=Fn('Construyendo GRANJA DE ANIMALES...')
f.fill((-1,0,-1),(21,6,22),'air'); f.fill((-1,0,-1),(21,0,22),'grass_block')
f.fill((10,0,-1),(10,0,22),'dirt_path'); f.fill((-1,0,10),(21,0,10),'dirt_path')
pens=[((0,0),(9,9),(9,4),'east','cow','VACAS'),((11,0),(20,9),(11,4),'west','sheep','OVEJAS'),
      ((0,11),(9,20),(9,15),'east','pig','CERDOS'),((11,11),(20,20),(11,15),'west','chicken','GALLINAS')]
for (x0,z0),(x1,z1),(gx,gz),gf,mob,name in pens:
    f.fill((x0,1,z0),(x1,1,z0),'oak_fence'); f.fill((x0,1,z1),(x1,1,z1),'oak_fence')
    f.fill((x0,1,z0),(x0,1,z1),'oak_fence'); f.fill((x1,1,z0),(x1,1,z1),'oak_fence')
    f.set((gx,1,gz),f'oak_fence_gate[facing={gf}]')
    for cx,cz in [(x0,z0),(x1,z0),(x0,z1),(x1,z1)]: f.set((cx,2,cz),'lantern')
    f.set((x0+1,1,z0+1),'hay_block'); f.set((x1-1,1,z1-1),'water_cauldron[level=3]')
    mx,mz=(x0+x1)//2,(z0+z1)//2
    for i in range(6 if mob=='chicken' else 4):
        f.summon(mob,(mx-1+i%3,1,mz-1+i//3),'{PersistenceRequired:1b}')
    f.label((mx,4,mz),name)
f.set((10,1,22),'barrel[facing=up]{Items:[{Slot:0b,id:"minecraft:wheat",count:64},{Slot:1b,id:"minecraft:wheat",count:64},{Slot:2b,id:"minecraft:carrot",count:64},{Slot:3b,id:"minecraft:wheat_seeds",count:64},{Slot:4b,id:"minecraft:shears",count:1}]}')
f.label((10,3,22),'COMIDA PARA ANIMALES\\ntrigo, zanahoria, semillas')
f.msg('Granja de animales lista: vacas, ovejas, cerdos y gallinas. En el barril de la entrada hay trigo, zanahorias y semillas para que se reproduzcan.')
f.save('animales')

# ===================== CASA GRANDE (2 pisos) =====================
f=Fn('Construyendo CASA GRANDE...')
f.fill((-1,0,-1),(17,16,13),'air'); f.fill((-1,0,-1),(17,0,13),'grass_block')
f.fill((0,0,0),(16,0,12),'stone_bricks'); f.fill((1,0,1),(15,0,11),'dark_oak_planks')
f.fill((0,1,0),(16,8,12),'spruce_planks'); f.fill((1,1,1),(15,8,11),'air')
for x,z in [(0,0),(16,0),(0,12),(16,12),(8,0)]: f.fill((x,1,z),(x,8,z),'stripped_dark_oak_log')
f.fill((0,5,0),(16,5,12),'stripped_dark_oak_log[axis=x]'); f.fill((1,5,1),(15,5,11),'dark_oak_planks')
f.fill((0,9,0),(16,9,12),'spruce_planks')
for k in range(7):
    y=9+k
    if k<6:
        f.fill((-1,y,k-1),(17,y,k-1),'dark_oak_stairs[facing=south]'); f.fill((-1,y,13-k),(17,y,13-k),'dark_oak_stairs[facing=north]')
        if k>0: f.fill((0,y,k),(0,y,12-k),'spruce_planks'); f.fill((16,y,k),(16,y,12-k),'spruce_planks')
    else:
        f.fill((-1,y,5),(17,y,7),'dark_oak_slab[type=bottom]')
for x in (2,3,5,6,10,11,13,14):
    for y0 in (2,6):
        f.fill((x,y0,0),(x,y0+1,0),'glass_pane[east=true,west=true]'); f.fill((x,y0,12),(x,y0+1,12),'glass_pane[east=true,west=true]')
for z in (3,4,8,9):
    for y0 in (2,6):
        f.fill((0,y0,z),(0,y0+1,z),'glass_pane[north=true,south=true]'); f.fill((16,y0,z),(16,y0+1,z),'glass_pane[north=true,south=true]')
f.fill((7,1,12),(9,3,12),'air')
f.set((7,1,12),'iron_door[half=lower,facing=north,hinge=left]'); f.set((7,2,12),'iron_door[half=upper,facing=north,hinge=left]')
f.set((9,1,12),'iron_door[half=lower,facing=north,hinge=right]'); f.set((9,2,12),'iron_door[half=upper,facing=north,hinge=right]')
f.set((8,1,12),'spruce_planks'); f.set((8,2,12),'spruce_planks'); f.set((8,3,12),'spruce_planks')
f.set((8,2,13),'stone_button[face=wall,facing=south]'); f.set((8,2,11),'stone_button[face=wall,facing=north]')
f.fill((6,0,13),(10,0,15),'stone_bricks'); f.set((6,1,13),'lantern'); f.set((10,1,13),'lantern')
# escalera interna
for i in range(4): f.set((11+i,1+i,10),'oak_stairs[facing=east]'); f.set((11+i,1+i,11),'oak_stairs[facing=east]')
f.fill((11,5,10),(15,5,11),'air'); f.fill((11,6,9),(15,6,9),'oak_fence')
# piso 1: sala, cocina y encantamientos
f.fill((2,1,2),(6,1,6),'bookshelf'); f.fill((3,1,3),(5,1,5),'air'); f.set((4,1,6),'air'); f.set((4,1,4),'enchanting_table')
f.set((15,1,1),'crafting_table'); f.set((14,1,1),'furnace[facing=south]'); f.set((13,1,1),'smoker[facing=south]'); f.set((12,1,1),'blast_furnace[facing=south]')
f.set((11,1,1),'brewing_stand'); f.set((10,1,1),'anvil[facing=east]'); f.set((9,1,1),'cauldron')
f.fill((6,1,8),(10,1,10),'red_carpet'); f.set((1,1,10),'ender_chest[facing=east]')
for p in [(4,4,4),(12,4,4),(8,4,9)]: f.set(p,'lantern[hanging=true]')
# piso 2: dormitorio
f.bed((2,6,3),(2,6,2),'red','north'); f.bed((4,6,3),(4,6,2),'blue','north'); f.bed((6,6,3),(6,6,2),'green','north'); f.bed((8,6,3),(8,6,2),'yellow','north')
f.fill((1,6,5),(1,7,9),'barrel[facing=east]'); f.fill((15,6,1),(15,7,6),'barrel[facing=west]')
f.fill((3,6,6),(9,6,9),'light_blue_carpet')
for p in [(4,8,5),(12,8,4),(8,8,9)]: f.set(p,'lantern[hanging=true]')
f.label((8,5,14),'CASA')
f.msg('Casa grande lista: 2 pisos, 4 camas, 15 barriles, cocina, mesa de encantar con 15 estanterias, pociones, yunque y cofre de ender.')
f.save('casa_grande')

# ===================== MONTANA + CASA ENCIMA =====================
f=Fn('Construyendo MONTANA con la casa grande encima (unos 60x60 bloques)...')
R0,SL,HT=26,0.8,16
for xa,xb in [(-30,0),(1,30)]:
    for za,zb in [(-32,0),(1,30)]:
        for ya,yb in [(1,12),(13,24)]: f.fill((xa,ya,za),(xb,yb,zb),'air')
for h in range(1,HT+1):
    r=R0-h*SL
    for dz in range(-int(r),int(r)+1):
        w=int(math.sqrt(max(r*r-dz*dz,0)))
        f.fill((-w,h,dz),(w,h,dz),'grass_block' if h<HT else 'grass_block')
# arboles en la ladera
for ang in [30,70,110,150,210,250,290,330]:
    d=19; x=round(d*math.sin(math.radians(ang))); z=round(d*math.cos(math.radians(ang)))
    if z<-14 and abs(x)<5: continue
    h=min(HT,int((R0-math.hypot(x,z))/SL))
    f.L.append(f'place feature minecraft:spruce {C(x,h+1,z)}')
# escalera de subida (lado norte)
for i in range(1,HT+1):
    z=-30+i
    if i>1: f.fill((-2,1,z),(2,i-1,z),'stone_bricks')
    f.fill((-2,i,z),(2,i+5,z),'air')
    f.fill((-1,i,z),(1,i,z),'stone_brick_stairs[facing=south]')
    f.set((-2,i,z),'stone_bricks'); f.set((2,i,z),'stone_bricks')
    f.set((-2,i+1,z),'stone_brick_wall'); f.set((2,i+1,z),'stone_brick_wall')
    if i%4==0: f.set((-2,i+2,z),'lantern'); f.set((2,i+2,z),'lantern')
f.L.append(f'execute positioned ~-8 ~{HT} ~-6 run function granjas:_casa_grande')
f.label((0,3,-31),'SUBIDA A LA CASA')
f.msg('Montana lista: sube por la escalera del lado norte. La casa grande esta en la cima.')
f.save('montana')

# ===================== PORTAL DEL END DECORADO =====================
f=Fn('Construyendo PORTAL DEL END decorado...')
f.fill((-8,0,-8),(8,12,8),'air')
f.fill((-8,0,-8),(8,0,8),'end_stone_bricks'); f.fill((-6,0,-6),(6,0,6),'purpur_block'); f.fill((-4,0,-4),(4,0,4),'obsidian')
for x,z in [(-3,-3),(3,-3),(-3,3),(3,3)]: f.set((x,0,z),'crying_obsidian')
for i in range(-1,2):
    f.set((i,1,-2),'end_portal_frame[eye=true,facing=south]'); f.set((i,1,2),'end_portal_frame[eye=true,facing=north]')
    f.set((-2,1,i),'end_portal_frame[eye=true,facing=east]'); f.set((2,1,i),'end_portal_frame[eye=true,facing=west]')
f.fill((-1,1,-1),(1,1,1),'end_portal')
for x,z in [(-6,-6),(6,-6),(-6,6),(6,6)]:
    f.fill((x,1,z),(x,5,z),'purpur_pillar'); f.set((x,6,z),'purpur_block'); f.set((x,7,z),'end_rod[facing=up]')
for x,z in [(-6,0),(6,0),(0,-6),(0,6)]:
    f.fill((x,1,z),(x,2,z),'end_stone_brick_wall'); f.set((x,3,z),'soul_lantern')
for x,z,fac in [(-4,-4,'south'),(4,-4,'south'),(-4,4,'north'),(4,4,'north')]:
    f.set((x,1,z),'obsidian'); f.set((x,2,z),f'dragon_head[rotation={ {"south":0,"north":8}[fac] }]')
f.fill((-8,1,-8),(8,1,-8),'end_stone_brick_wall'); f.fill((-8,1,8),(-1,1,8),'end_stone_brick_wall'); f.fill((1,1,8),(8,1,8),'end_stone_brick_wall')
f.fill((-8,1,-8),(-8,1,8),'end_stone_brick_wall'); f.fill((8,1,-8),(8,1,8),'end_stone_brick_wall')
f.label((0,5,0),'PORTAL AL END','light_purple')
f.msg('Portal del End listo. Cuidado: al pisar el centro viajas al End. Lleva buena armadura, comida y bloques.')
f.save('portal_end')
open(f'{F}/portal_end.mcfunction','w').write('execute align xyz positioned ~0.5 ~ ~12.5 run function granjas:_portal_end\n')

# ===================== CUARTO DE COFRES =====================
f=Fn('Construyendo CUARTO DE COFRES organizado...')
f.fill((-1,0,-1),(22,7,13),'air'); f.fill((-1,0,-1),(22,0,13),'grass_block')
f.fill((0,0,0),(20,0,12),'polished_andesite')
f.fill((0,1,0),(20,5,12),'spruce_planks'); f.fill((1,1,1),(19,4,11),'air')
for x,z in [(0,0),(20,0),(0,12),(20,12)]: f.fill((x,1,z),(x,5,z),'stripped_spruce_log')
grupos=[(1,3),(5,7),(9,11),(13,15),(17,19)]
norte=['PIEDRA Y TIERRA','MADERA','MINERALES','REDSTONE','COMIDA']
sur=['DROPS DE MOBS','GRANJAS','HERRAMIENTAS Y ARMAS','POCIONES Y LIBROS','VARIOS']
for (a,b),n,s in zip(grupos,norte,sur):
    f.fill((a,1,1),(b,3,1),'barrel[facing=south]'); f.fill((a,1,11),(b,3,11),'barrel[facing=north]')
    f.label(((a+b)//2,4,2),n,'yellow'); f.label(((a+b)//2,4,10),s,'yellow')
for x in (4,8,12,16):
    for z in (1,11): f.fill((x,1,z),(x,3,z),'stripped_spruce_log')
for x in range(3,19,4):
    for z in (4,8): f.set((x,5,z),'glowstone')
f.set((10,1,6),'ender_chest[facing=east]'); f.set((8,1,6),'crafting_table'); f.set((12,1,6),'barrel[facing=up]')
f.fill((5,1,5),(15,1,7),'gray_carpet','replace air')
f.set((20,1,6),'iron_door[half=lower,facing=west,hinge=left]'); f.set((20,2,6),'iron_door[half=upper,facing=west,hinge=left]')
f.set((21,2,7),'stone_button[face=wall,facing=east]'); f.set((19,2,7),'stone_button[face=wall,facing=west]')
f.label((21,4,6),'CUARTO DE COFRES')
f.msg('Cuarto de cofres listo: 90 barriles en 10 secciones con su nombre (piedra, madera, minerales, redstone, comida, mobs, granjas, herramientas, pociones y varios).')
f.save('cofres')

# ===================== TORRE PARA ELITROS CON ASCENSOR =====================
H=60
f=Fn('Construyendo TORRE DE ELITROS con ascensor de burbujas (60 bloques)...')
f.fill((-4,0,-12),(22,30,12),'air'); f.fill((-4,31,-12),(22,H+4,12),'air'); f.fill((-4,0,-12),(22,0,12),'grass_block')
f.fill((0,0,0),(8,H,8),'stone_bricks','hollow')
for y in range(4,H,6):
    for a,b in [((3,y,0),(5,y+2,0)),((3,y,8),(5,y+2,8)),((0,y,3),(0,y+2,5)),((8,y,3),(8,y+2,5))]: f.fill(a,b,'glass')
f.fill((3,0,3),(5,H,5),'glass')
f.set((4,0,4),'soul_sand'); f.fill((4,1,4),(4,H,4),'bubble_column[drag=false]')
f.fill((4,1,1),(4,2,2),'air'); f.fill((4,1,0),(4,2,0),'air')
f.set((4,1,3),'oak_door[half=lower,facing=south,hinge=left]'); f.set((4,2,3),'oak_door[half=upper,facing=south,hinge=left]')
f.set((4,1,0),'iron_door[half=lower,facing=north,hinge=left]'); f.set((4,2,0),'iron_door[half=upper,facing=north,hinge=left]')
f.set((5,2,-1),'stone_button[face=wall,facing=north]'); f.set((5,2,1),'stone_button[face=wall,facing=south]')
for y in range(6,H,8): f.set((2,y,2),'lantern[hanging=true]') if False else None
f.fill((1,1,1),(7,H-1,7),'air','replace stone_bricks')
f.fill((3,1,3),(5,H,5),'glass'); f.fill((4,1,4),(4,H,4),'bubble_column[drag=false]'); f.set((4,1,3),'oak_door[half=lower,facing=south,hinge=left]'); f.set((4,2,3),'oak_door[half=upper,facing=south,hinge=left]')
# plataforma de salto arriba
f.fill((-3,H+1,-3),(11,H+1,11),'polished_deepslate'); f.set((4,H+1,4),'air')
f.fill((-3,H+2,-3),(11,H+2,-3),'glass_pane[east=true,west=true]'); f.fill((-3,H+2,11),(11,H+2,11),'glass_pane[east=true,west=true]')
f.fill((-3,H+2,-3),(-3,H+2,11),'glass_pane[north=true,south=true]'); f.fill((11,H+2,-3),(11,H+2,11),'glass_pane[north=true,south=true]')
f.fill((3,H+2,-3),(5,H+2,-3),'air')
f.fill((3,H+1,-10),(5,H+1,-4),'polished_deepslate')                      # trampolin hacia el norte
for x,z in [(3,-10),(5,-10),(-3,-3),(11,-3),(-3,11),(11,11)]: f.set((x,H+2,z),'end_rod[facing=up]')
for x,z in [(0,0),(8,0),(0,8),(8,8)]: f.set((x,H+2,z),'lantern')
f.set((4,H+2,8),'barrel[facing=up]{Items:[{Slot:0b,id:"minecraft:firework_rocket",count:64,components:{"minecraft:fireworks":{flight_duration:2}}}]}')
# piscina de aterrizaje
f.fill((11,-3,-2),(21,0,10),'stone_bricks'); f.fill((12,-2,-1),(20,0,9),'water')
f.label((4,4,-1),'TORRE DE ELITROS\\nentra a la columna: te sube sola')
f.label((4,H+4,-6),'SALTA DESDE EL TRAMPOLIN','aqua')
f.msg('Torre lista: entra por la puerta, metete en la columna de agua y sube sola hasta arriba. En la cima hay un barril con cohetes. Si caes, hay una piscina al este.')
f.save('torre_elitros')

# ===================== MEGABASE =====================
MHUB='@e[type=minecraft:marker,tag=granjas_mega,limit=1]'
RX0,RX1,RZ0,RZ1=-100,100,-150,80
cols=[('hierro',-94,-4,19,-3,19,26),('mobs',-67,-2,19,-2,19,25),('experiencia',-42,-3,11,-2,12,18),('aldeanos',-24,-1,18,-1,11,16),
      ('comercio',5,-4,31,-3,5,12),('cana',43,-3,13,-4,3,11),('comida',62,-3,13,-3,4,11),('hornos',81,-3,9,-3,3,10)]
def farm_calls(lst):
    out=[]
    for n,X,lx0,lx1,lz0,lz1,step in lst:
        ox=X-lx0
        for k in range(5):
            oz=-20-lz1-k*step
            out.append(f'execute positioned ~{ox} ~ ~{oz} run function granjas:_{n}')
    return out
W('megabase',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_mega0'])
W('_mega0',[
 'kill @e[type=minecraft:marker,tag=granjas_mega]',
 'summon minecraft:marker ~ ~ ~ {Tags:["granjas_mega"]}',
 f'forceload add ~{RX0} ~{RZ0} ~{RX1} ~{RZ1}',
 'tellraw @a {"text":"MEGABASE: preparando el terreno (200 x 230 bloques). Esto tarda como 40 segundos, el servidor se puede trabar un poco. NO te muevas.","color":"gold"}',
 'schedule function granjas:_mega1 6s replace'])
def flat_stage(ya,yb,extra=[]):
    L=[]
    for xa,xb in chunks(RX0,RX1,30):
        for za,zb in chunks(RZ0,RZ1,30):
            L.append(f'fill {C(xa,ya,za)} {C(xb,yb,zb)} air')
            for e in extra: L.append(e.format(a=C(xa,0,za),b=C(xb,0,zb),c=C(xa,-3,za),d=C(xb,-1,zb)))
    return L
def stage(name,body,nxt=None,msg=None,delay='4s'):
    L=[]
    if msg: L.append(f'tellraw @a {{"text":"{msg}","color":"yellow"}}')
    L+=body
    W(f'_{name}b',L)
    W(f'_{name}',[f'execute at {MHUB} run function granjas:_{name}b']+([f'schedule function granjas:_{nxt} {delay} replace'] if nxt else []))
stage('mega1',[f'execute positioned {C(RX0,-6,RZ0)} run kill @e[type=!minecraft:player,tag=!granjas_mega,tag=!granjas_hub,dx={RX1-RX0},dy=70,dz={RZ1-RZ0}]']+flat_stage(1,18),'mega2','Aplanando (1/3)...')
stage('mega2',flat_stage(19,36),'mega3','Aplanando (2/3)...')
stage('mega3',flat_stage(37,48)+[l for l in flat_stage(0,0,['fill {a} {b} grass_block','fill {c} {d} dirt']) if not l.endswith(' air')]+['kill @e[type=minecraft:item,distance=..250]'],'mega4','Aplanando (3/3)...')
caminos=[f'fill {C(-2,0,RZ0)} {C(2,0,RZ1)} stone_bricks', f'fill {C(RX0,0,-2)} {C(RX1,0,2)} stone_bricks',
         f'fill {C(-12,0,-12)} {C(12,0,12)} polished_andesite']
for z in range(RZ0,RZ1+1,10): caminos.append(f'setblock {C(-3,1,z)} lantern'); caminos.append(f'setblock {C(3,1,z)} lantern')
for x in range(RX0,RX1+1,10): caminos.append(f'setblock {C(x,1,-3)} lantern'); caminos.append(f'setblock {C(x,1,3)} lantern')
stage('mega4',['tp @a[distance=..10] ~ ~1 ~-15']+caminos+['function granjas:_portal_end'],'mega5','Construyendo caminos y portal del End...')
stage('mega5',farm_calls(cols[:2]),'mega6','Construyendo 5 granjas de hierro y 5 de mobs...')
stage('mega6',farm_calls(cols[2:4]),'mega7','Construyendo 5 granjas de experiencia y 5 criaderos...')
stage('mega7',farm_calls(cols[4:6]),'mega8','Construyendo 5 salas de comercio y 5 granjas de cana...')
stage('mega8',farm_calls(cols[6:]),'mega9','Construyendo 5 granjas de comida y 5 de hornos...')
stage('mega9',['execute positioned ~-60 ~ ~48 run function granjas:_montana',
               'execute positioned ~-28 ~ ~20 run function granjas:_animales',
               'execute positioned ~8 ~ ~20 run function granjas:_cofres',
               'execute positioned ~50 ~ ~30 run function granjas:_torre_elitros',
               f'summon minecraft:text_display {C(0,4,-12)} {{billboard:"center",text:{{text:"MEGABASE\\nNorte: 40 granjas\\nSur: montana con casa, animales, cofres y torre de elitros",color:"gold",bold:1b}}}}',
               'tellraw @a {"text":"MEGABASE TERMINADA! Norte: las 40 granjas. Sur: montana con la casa (oeste), animales, cuarto de cofres y torre de elitros (este). Portal del End en el centro.","color":"green"}'],
      None,'Construyendo montana con casa, animales, cofres y torre...')

H=['scoreboard objectives add granjas dummy',
 'execute unless score #on granjas matches 0..1 run scoreboard players set #on granjas 0',
 'schedule function granjas:producir 60s replace',
 'tellraw @a {"text":"[Granjas v6] /function granjas:megabase  = construye TODO. Lista de comandos: /function granjas:lista","color":"gold"}']
W('ayuda',H)
W('lista',['tellraw @s {"text":"--- TODO JUNTO ---\\n/function granjas:megabase\\n--- PLAZA PEQUENA ---\\n/function granjas:aplanar  y luego  granjas:construir\\n--- SUELTAS (donde estes parado) ---\\nhierro, experiencia, aldeanos, comercio, cana, comida, sandia, hornos, mobs, animales, casa, casa_grande, montana, portal_end, cofres, torre_elitros\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, arreglar","color":"aqua"}'])
json.dump({"pack":{"description":"Granjas v6: megabase","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)

z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
# ---- validacion ----
import re
ok_cmds={'fill','setblock','summon','tellraw','execute','function','kill','forceload','schedule','data','loot','scoreboard','tp','place'}
bad=0; total=0
for fn in os.listdir(F):
    for i,line in enumerate(open(f'{F}/{fn}'),1):
        line=line.rstrip('\n'); total+=1
        if not line: continue
        if line.split()[0] not in ok_cmds: print('LINEA RARA',fn,i,line[:80]); bad=1
        if line.count('{')!=line.count('}') or line.count('[')!=line.count(']'): print('LLAVES',fn,i,line[:100]); bad=1
        m=re.match(r'fill ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*)',line)
        if m:
            v=[int(t) if t else 0 for t in m.groups()]
            vol=(abs(v[3]-v[0])+1)*(abs(v[4]-v[1])+1)*(abs(v[5]-v[2])+1)
            if vol>32768: print('GRANDE',fn,vol,line[:60]); bad=1
print('OK' if not bad else 'HAY ERRORES', total,'lineas')
