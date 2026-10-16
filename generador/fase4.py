# FASE 4: bunker subterraneo, estatua de 2 munecos, salon de cofres gigante y ferrocarriles.
# Uso: python fase4.py  -> regenera TODO el datapack (gen6 + fases 1 a 4)
# En el juego: /function granjas:fase4   (construye al ESTE y SUR; el bunker queda 26 bloques abajo)
# Las vias se tienden al final, en el juego: un "constructor" lee donde estan los marcadores de las
# fases 1, 2, 3 y la megabase, y avanza bloque a bloque desde la estacion central hasta cada una.
import os; GEN=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(GEN,'fase3.py'),encoding='utf-8').read())

M4='@e[type=minecraft:marker,tag=granjas_f4,limit=1]'
SX,SZ=26,22          # centro de la plaza y la estatua
HX,HZ=50,0           # salon de cofres
BX,BY,BZ=8,-26,4     # bunker (esquina), el piso queda 26 bloques bajo la superficie

# =====================================================================
#  ESTACION CENTRAL: torre de 4 andenes (uno por linea, cada uno 4 bloques mas alto)
# =====================================================================
LINEAS=[ # (tag destino, nombre, cama de la via, baranda, farol)
 ('granjas_f1','LINEA ROJA - FASE 1 (hierro y aldeanos)','red_nether_bricks','nether_brick_fence','lantern','red'),
 ('granjas_f2','LINEA VERDE - FASE 2 (animales y cultivos)','mossy_stone_bricks','oak_fence','lantern','green'),
 ('granjas_f3','LINEA AZUL - FASE 3 (casas y portales)','polished_deepslate','dark_oak_fence','soul_lantern','aqua'),
 ('granjas_mega','LINEA DORADA - MEGABASE','smooth_sandstone','birch_fence','lantern','gold')]
NIV=[4+4*k for k in range(4)]   # nivel (y local) de la cama de cada linea en la estacion
def estacion():
    g=G(0,0); top=NIV[-1]+3
    g.fill((-1,0,-13),(7,top,-7),'stone_bricks'); g.fill((0,1,-12),(6,top-1,-8),'air')
    g.walls(-1,7,2,top-1,-13,-7,'glass')
    for x,z in [(-1,-13),(7,-13),(-1,-7),(7,-7)]: g.fill((x,1,z),(x,top,z),'stripped_oak_log')
    g.fill((-1,top,-13),(7,top,-7),'oak_planks')
    for k,b in enumerate(NIV):
        tag,name,bed,fence,lamp,color=LINEAS[k]
        g.fill((0,b,-12),(6,b,-8),bed)
        g.fill((-1,b+1,-10),(-1,b+2,-10),'air'); g.fill((7,b+1,-10),(7,b+2,-10),'air')     # salidas este/oeste
        g.fill((3,b+1,-13),(3,b+2,-13),'air'); g.fill((3,b+1,-7),(3,b+2,-7),'air')         # salidas norte/sur
        g.L.append(f'summon minecraft:text_display {g.p(3,b+3,-12)} {{billboard:"center",text:{{text:"{name}",color:"{color}",bold:1b}},background:1073741824}}')
        g.set((5,b+3,-12),'lantern[hanging=true]')
    g.fill((1,1,-12),(1,top-1,-12),'ladder[facing=south]')
    g.fill((2,1,-7),(4,2,-7),'air')                                                       # entrada (sur)
    g.label((3,4,-5),'ESTACION CENTRAL\\nsube por la escalera: 1 piso por linea','gold')
    return g.L

# =====================================================================
#  PLAZA Y ESTATUA DE 2 MUNECOS (se toman de la mano, miran al sur)
# =====================================================================
def muneco(g,fx,h0,fz,c):
    legs,shoes,shirt,skin,hair=c['legs'],c['shoes'],c['shirt'],c['skin'],c['hair']
    g.fill((fx,h0,fz),(fx+3,h0+5,fz+1),legs); g.fill((fx,h0,fz),(fx+3,h0,fz+1),shoes)
    g.fill((fx+1,h0+1,fz),(fx+2,h0+4,fz+1),c.get('gap',legs))
    g.fill((fx,h0+6,fz),(fx+3,h0+11,fz+1),shirt)
    for ax in (fx-2,fx+4):
        g.fill((ax,h0+6,fz),(ax+1,h0+11,fz+1),skin); g.fill((ax,h0+9,fz),(ax+1,h0+11,fz+1),shirt)
    g.fill((fx,h0+12,fz-1),(fx+3,h0+15,fz+2),skin)                     # cabeza 4x4x4
    g.fill((fx,h0+15,fz-1),(fx+3,h0+15,fz+2),hair); g.fill((fx,h0+12,fz-1),(fx+3,h0+15,fz-1),hair)
    g.fill((fx,h0+13,fz-1),(fx,h0+15,fz+1),hair); g.fill((fx+3,h0+13,fz-1),(fx+3,h0+15,fz+1),hair)
    if c.get('largo'): g.fill((fx,h0+9,fz-1),(fx+3,h0+12,fz-1),hair)  # pelo largo por la espalda
    g.set((fx,h0+13,fz+2),'white_concrete'); g.set((fx+1,h0+13,fz+2),c['ojos'])
    g.set((fx+2,h0+13,fz+2),c['ojos']); g.set((fx+3,h0+13,fz+2),'white_concrete')
    g.fill((fx+1,h0+12,fz+2),(fx+2,h0+12,fz+2),c['boca'])
def plaza():
    g=G(0,0)
    for dz in range(-17,18):
        w=int(math.sqrt(max(17*17-dz*dz,0)))
        g.fill((SX-w,0,SZ+dz),(SX+w,0,SZ+dz),'grass_block')
        w2=int(math.sqrt(max(15*15-dz*dz,0)))
        if w2: g.fill((SX-w2,0,SZ+dz),(SX+w2,0,SZ+dz),'polished_andesite')
    for dz in range(-11,12):
        w=int(math.sqrt(max(11*11-dz*dz,0))); g.fill((SX-w,0,SZ+dz),(SX+w,0,SZ+dz),'smooth_stone')
    for a in range(0,360,15):
        x=SX+round(16*math.cos(math.radians(a))); z=SZ+round(16*math.sin(math.radians(a)))
        g.set((x,1,z),['azalea','flowering_azalea','allium','oxeye_daisy'][a//15%4])
    for a in range(0,360,45):
        x=SX+round(13*math.cos(math.radians(a))); z=SZ+round(13*math.sin(math.radians(a)))
        g.fill((x,1,z),(x,2,z),'dark_oak_fence'); g.set((x,3,z),'lantern')
    # pedestal
    g.fill((SX-10,1,SZ-3),(SX+9,2,SZ+4),'smooth_quartz'); g.fill((SX-10,3,SZ-3),(SX+9,3,SZ+4),'quartz_bricks')
    for x in range(SX-10,SX+10): g.set((x,1,SZ+5),'quartz_stairs[facing=north]')
    g.fill((SX-11,1,SZ-3),(SX-11,1,SZ+4),'quartz_stairs[facing=east]'); g.fill((SX+10,1,SZ-3),(SX+10,1,SZ+4),'quartz_stairs[facing=west]')
    chico=dict(legs='blue_concrete',shoes='gray_concrete',shirt='cyan_concrete',skin='smooth_sandstone',hair='brown_concrete',ojos='blue_concrete',boca='brown_terracotta')
    chica=dict(legs='white_concrete',shoes='white_concrete',shirt='pink_concrete',skin='smooth_sandstone',hair='yellow_concrete',ojos='green_concrete',boca='red_terracotta',largo=1,gap='pink_concrete')
    muneco(g,SX-6,4,SZ,chico); muneco(g,SX+2,4,SZ,chica)
    g.L.append(f'summon minecraft:text_display {g.p(SX,3,SZ+6)} {{billboard:"center",text:{{text:"LOS FUNDADORES",color:"gold",bold:1b}},background:1073741824}}')
    return g.L

# =====================================================================
#  SALON DE COFRES GIGANTE: 24 secciones x 36 barriles = 864 barriles (23 328 espacios)
# =====================================================================
CATS=[('PIEDRA','stone'),('ROCAS','granite'),('DEEPSLATE','cobbled_deepslate'),('TIERRA','dirt'),('ARENA Y GRAVA','sand'),('MADERA','oak_planks'),
 ('TRONCOS','oak_log'),('VIDRIO','glass'),('LANA Y TINTES','white_wool'),('CONCRETO','white_concrete'),('MINERALES','diamond'),('LINGOTES','iron_ingot'),
 ('REDSTONE','redstone'),('MECANISMOS','piston'),('COMIDA','bread'),('CULTIVOS','wheat'),('DROPS DE MOBS','bone'),('RAROS DE MOBS','ender_pearl'),
 ('HERRAMIENTAS','diamond_pickaxe'),('ARMAS','diamond_sword'),('ARMADURAS','diamond_chestplate'),('POCIONES','brewing_stand'),('LIBROS','enchanted_book'),('NETHER Y END','netherrack')]
def salon():
    g=G(HX,HZ); L,Z=41,29
    g.fill((-1,0,-1),(L+1,0,Z+1),'polished_andesite'); g.fill((0,0,0),(L,0,Z),'dark_oak_planks')
    g.walls(-1,L+1,1,7,-1,Z+1,'spruce_planks'); g.fill((-1,8,-1),(L+1,8,Z+1),'dark_oak_planks')
    for x in range(-1,L+2,6):
        for z in (-1,Z+1): g.fill((x,1,z),(x,7,z),'stripped_spruce_log')
    for x in range(1,L,6):
        for z in (-1,Z+1): g.fill((x,3,z),(x+2,5,z),'glass')
    g.fill((-1,1,20),(-1,3,21),'air')                                                     # entrada (oeste)
    i=0
    for r in range(4):
        z0=4+6*r
        for side,(zz,fac,fr,ff) in enumerate([(z0,'north',z0-1,2),(z0+1,'south',z0+2,3)]):
            for c in range(3):
                x0=3+12*c; name,icon=CATS[i]; i+=1
                g.fill((x0,1,zz),(x0+11,3,zz),f'barrel[facing={fac}]')
                g.fill((x0,4,zz),(x0+11,4,zz),'spruce_planks')
                g.summon('item_frame',(x0+5,4,fr),'{Facing:'+str(ff)+'b,Fixed:1b,Item:{id:"minecraft:'+icon+'",count:1}}')
                g.L.append(f'summon minecraft:text_display {g.p(x0+6,5,fr)} {{billboard:"center",text:{{text:"{name}",color:"yellow",bold:1b}},background:1073741824}}')
        g.fill((2,1,z0),(2,4,z0+1),'stripped_spruce_log'); g.fill((39,1,z0),(39,4,z0+1),'stripped_spruce_log')
    for x in range(4,L,6):
        for z in (2,8,14,20,26): g.set((x,7,z),'lantern[hanging=true]')
    for k,b in enumerate(['crafting_table','ender_chest[facing=west]','anvil[facing=north]','stonecutter[facing=west]','smithing_table','cartography_table']):
        g.set((L,1,3+k*4),b)
    g.label((-2,5,20),'SALON DE COFRES\\n864 barriles en 24 secciones','gold')
    return g.L

# =====================================================================
#  BUNKER: 40x30 a 26 bloques de profundidad. Dormitorio (2), encantamientos y pociones,
#  almacen, granja interna (1 de cada una) y 8 aldeanos de tradeo.
# =====================================================================
class GB(G):
    def p(s,x,y,z): return C(x+s.ox,y+BY,z+s.oz)
def bunker_a():
    g=GB(BX,BZ)
    g.fill((-1,-1,-1),(40,8,30),'deepslate_tiles'); g.fill((0,1,0),(39,7,29),'air')
    g.fill((0,0,0),(39,0,29),'polished_deepslate')
    for x in range(2,39,6):
        for z in range(2,29,6): g.set((x,8,z),'sea_lantern')
    for x in range(0,40,4): g.set((x,4,10),'deepslate_bricks')
    g.fill((0,1,10),(39,7,10),'deepslate_bricks'); g.fill((10,1,0),(10,7,9),'deepslate_bricks'); g.fill((20,1,0),(20,7,29),'deepslate_bricks')
    for x in (4,14,28): g.fill((x,1,10),(x+1,2,10),'air')
    g.fill((10,1,4),(10,2,5),'air'); g.fill((20,1,4),(20,2,5),'air'); g.fill((20,1,19),(20,2,20),'air')
    g.fill((28,1,30),(30,3,30),'air')                                                      # puerta a la escalera
    # A) dormitorio para 2
    g.set((2,1,2),'red_bed[facing=north,part=foot]'); g.set((2,1,1),'red_bed[facing=north,part=head]')
    g.set((4,1,2),'blue_bed[facing=north,part=foot]'); g.set((4,1,1),'blue_bed[facing=north,part=head]')
    g.set((3,1,1),'barrel[facing=up]'); g.set((3,2,1),'lantern')
    g.fill((8,1,1),(8,2,4),'barrel[facing=west]'); g.fill((1,1,5),(5,1,7),'red_carpet')
    for x,b in [(1,'crafting_table'),(2,'furnace[facing=north]'),(3,'smoker[facing=north]'),(4,'blast_furnace[facing=north]'),(6,'ender_chest[facing=north]')]: g.set((x,1,9),b)
    # B) encantamientos y pociones
    g.set((15,1,4),'enchanting_table')
    g.fill((13,1,2),(17,2,2),'bookshelf'); g.fill((13,1,6),(17,2,6),'bookshelf'); g.fill((13,1,3),(13,2,5),'bookshelf'); g.fill((17,1,3),(17,2,5),'bookshelf')
    g.fill((15,1,6),(15,2,6),'air'); g.fill((14,1,3),(16,1,5),'purple_carpet'); g.set((15,1,4),'enchanting_table')
    for x,b in [(11,'brewing_stand'),(12,'brewing_stand'),(13,'water_cauldron[level=3]'),(16,'anvil[facing=east]'),(17,'smithing_table'),(18,'grindstone[face=floor,facing=north]')]: g.set((x,1,8),b)
    g.set((19,1,1),'barrel[facing=west]{Items:[{Slot:0b,id:"minecraft:blaze_powder",count:16},{Slot:1b,id:"minecraft:nether_wart",count:32},{Slot:2b,id:"minecraft:glass_bottle",count:16},{Slot:3b,id:"minecraft:lapis_lazuli",count:64}]}')
    # C) almacen
    g.fill((21,1,0),(39,3,0),'barrel[facing=south]'); g.fill((21,1,9),(39,3,9),'barrel[facing=north]')
    g.fill((24,1,4),(36,2,5),'barrel[facing=up]')
    # luces de la granja interna ANTES de plantar (los cultivos se rompen si estan a oscuras al ponerlos)
    for x in range(1,20,3):
        for z in range(12,23,3): g.set((x,3,z),'light[level=15]')
    g.label((5,4,5),'DORMITORIO','yellow'); g.label((15,5,4),'ENCANTAMIENTOS Y POCIONES','yellow'); g.label((30,5,4),'ALMACEN','yellow')
    return g.L
PROF_B=[('librarian','lectern','Bibliotecario 1'),('librarian','lectern','Bibliotecario 2'),('librarian','lectern','Bibliotecario 3'),
 ('armorer','blast_furnace','Armero'),('toolsmith','smithing_table','Herrero'),('weaponsmith','grindstone','Armas'),('cleric','brewing_stand','Clerigo'),('farmer','composter','Granjero')]
def bunker_b():
    g=GB(BX,BZ)
    # D) granja interna: 1 de cada una
    for (x0,z0),(crop,age) in zip([(1,12),(7,12),(13,12),(1,18)],[('wheat',7),('carrots',7),('potatoes',7),('beetroots',3)]):
        g.fill((x0,0,z0),(x0+4,0,z0+4),'farmland[moisture=7]'); g.set((x0+2,0,z0+2),'water')
        g.fill((x0,1,z0),(x0+4,1,z0+4),f'{crop}[age={age}]'); g.set((x0+2,1,z0+2),'air')
    g.fill((7,0,18),(11,0,18),'sand'); g.fill((7,0,19),(11,0,19),'water'); g.fill((7,0,20),(11,0,20),'sand')
    g.fill((7,1,18),(11,2,18),'sugar_cane'); g.fill((7,1,20),(11,2,20),'sugar_cane')
    g.fill((13,0,18),(17,0,20),'grass_block'); g.fill((13,1,19),(17,3,19),'bamboo')
    g.fill((13,1,18),(17,1,18),'sweet_berry_bush[age=3]'); g.fill((13,0,22),(17,0,22),'mycelium')
    g.set((13,1,22),'red_mushroom'); g.set((15,1,22),'brown_mushroom'); g.set((17,1,22),'red_mushroom')
    for x,z in [(9,16),(15,16),(9,21),(15,21),(3,24),(13,24)]: g.set((x,4,z),'light[level=15]')
    for i,(mob,n) in enumerate([('cow',2),('sheep',2),('pig',2),('chicken',3)]):
        x0=1+i*5
        g.fill((x0,0,24),(x0+3,0,28),'grass_block')
        g.walls(x0-1,x0+4,1,1,23,29,'oak_fence'); g.set((x0+1,1,23),'oak_fence_gate[facing=north]')
        for k in range(n): g.summon(mob,(x0+1+k%2,1,25+k//2),'{PersistenceRequired:1b}')
    g.set((19,1,12),'barrel[facing=west]{Items:[{Slot:0b,id:"minecraft:wheat",count:64},{Slot:1b,id:"minecraft:carrot",count:64},{Slot:2b,id:"minecraft:wheat_seeds",count:64},{Slot:3b,id:"minecraft:bone_meal",count:64}]}')
    g.set((19,1,16),'barrel[facing=west]'); g.summon('marker',(19,1,16),'{Tags:["go_hierro","f4"]}')
    g.label((19,3,16),'BOVEDA DE HIERRO\\n(produccion asegurada)','white')
    g.label((10,5,14),'GRANJA INTERNA','yellow')
    # E) tradeo: 8 aldeanos en el muro este
    g.fill((36,1,11),(39,3,28),'deepslate_bricks')
    for i,(p,ws,name) in enumerate(PROF_B):
        z=12+2*i
        g.fill((38,1,z),(38,2,z),'air'); g.set((37,2,z),'air'); g.set((39,1,z),ws); g.set((37,3,z),'glowstone')
        g.summon('villager',(38,1,z),'{PersistenceRequired:1b,Xp:1,CustomName:"'+name+'",CustomNameVisible:1b,VillagerData:{profession:"minecraft:'+p+'",level:1,type:"minecraft:plains"}}')
    g.fill((24,0,18),(32,0,24),'polished_blackstone_bricks')
    g.label((30,5,20),'SALA DE TRADEO','yellow')
    return g.L
def escalera_bunker():
    g=G(0,0); x0,z0=BX+28,BZ+31      # escalera de 3 de ancho, baja hacia el norte hasta la puerta del bunker
    for k in range(0,27):
        z=z0+26-k; y=-k
        g.fill((x0-1,y,z),(x0+3,y+5,z),'deepslate_bricks'); g.fill((x0,y+1,z),(x0+2,y+4,z),'air')
        g.fill((x0,y,z),(x0+2,y,z),'deepslate_brick_stairs[facing=south]')
        if k%3==0: g.set((x0+1,y+4,z),'light[level=15]')
    g.fill((x0,-26,z0),(x0+2,-26,z0),'polished_deepslate'); g.fill((x0,-25,z0),(x0+2,-23,z0),'air')
    zt=z0+27
    g.fill((x0-1,0,zt),(x0+3,0,zt+2),'polished_deepslate'); g.fill((x0-1,5,z0+22),(x0+3,5,zt+2),'deepslate_tile_slab[type=bottom]')
    for x in (x0-1,x0+3): g.fill((x,1,zt+2),(x,4,zt+2),'deepslate_brick_wall')
    g.set((x0-2,1,zt+2),'lantern'); g.set((x0+4,1,zt+2),'lantern')
    g.label((x0+1,4,zt+3),'BUNKER\\nbaja por la escalera','gold')
    return g.L

# =====================================================================
#  FERROCARRILES (se tienden en el juego, 24 bloques por tick)
#  Cada linea: sale de su anden en la estacion central, va en X y luego en Z hasta un punto
#  6 bloques al noroeste del marcador de la fase (fuera de sus edificios). Atraviesa cerros con
#  tunel (solo rompe bloques naturales), cruza valles con puente y pilares, y al final baja o
#  sube en rampa hasta la altura de la fase. Cada 8 bloques: riel propulsor sobre bloque de redstone.
#  Estaciones: tope, 2 rieles de freno, boton para arrancar y barril con 8 vagonetas.
# =====================================================================
NAT=['#minecraft:base_stone_overworld','#minecraft:dirt','#minecraft:leaves','#minecraft:logs','#minecraft:sand','#minecraft:terracotta','gravel','snow_block','clay','sandstone','red_sandstone','ice','packed_ice','calcite','short_grass','tall_grass','fern','large_fern','#minecraft:flowers','snow','vine','sugar_cane','bamboo','sweet_berry_bush','dead_bush','glow_lichen']
def limpia(y0,y1,dy=''):
    return [f'fill ~ ~{y0} ~ ~ ~{y1} ~ air replace {t}' for t in NAT]
S='scoreboard players'
R='rieles'
def sc(*a): return f'{S} '+' '.join(a)
W('_rl_start',['scoreboard objectives add rieles dummy',sc('set #8',R,'8'),sc('set #6',R,'6'),sc('set #-1',R,'-1'),sc('set #linea',R,'1'),
 'tellraw @a {"text":"[Ferrocarriles] Tendiendo las vias hacia cada fase. Puede trabarse un poco el servidor.","color":"gold"}',
 'schedule function granjas:_rl_sig 1t replace'])
W('_rl_sig',[f'execute if score #linea {R} matches {k+1} run function granjas:_rl_l{k+1}' for k in range(4)]+[f'execute if score #linea {R} matches 5.. run function granjas:_rl_fin'])
for k,(tag,name,bed,fence,lamp,color) in enumerate(LINEAS):
    W(f'_rl_l{k+1}',[f'data modify storage granjas:riel l set value {{tag:"{tag}",y:{NIV[k]-1},sep:{6+3*k},bed:"{bed}",fence:"{fence}",lamp:"{lamp}",name:"{name.split(" - ")[0]}"}}',
                     'function granjas:_rl_ini with storage granjas:riel l'])
W('_rl_ini',['$execute unless entity @e[type=minecraft:marker,tag=$(tag)] run function granjas:_rl_salta with storage granjas:riel l',
             '$execute if entity @e[type=minecraft:marker,tag=$(tag)] run function granjas:_rl_prep with storage granjas:riel l'])
W('_rl_salta',['$tellraw @a {"text":"[Ferrocarriles] No encuentro $(tag) (esa fase no esta construida o esta muy lejos y descargada): se salta.","color":"red"}',
               sc('add #linea',R,'1'),'schedule function granjas:_rl_sig 2t replace'])
def store(path,score,scale='1'): return f'execute store result storage granjas:riel {path} int {scale} run {S} get {score} {R}'
W('_rl_prep',[
 'kill @e[type=minecraft:marker,tag=riel_w]','kill @e[type=minecraft:marker,tag=riel_s]',
 f'$execute at {M4} run summon minecraft:marker ~3 ~$(y) ~-10 {{Tags:["riel_w"]}}',
 f'$execute at {M4} run summon minecraft:marker ~3 ~$(y) ~-10 {{Tags:["riel_s"]}}',
 f'execute store result score #wx {R} run data get entity @e[type=minecraft:marker,tag=riel_w,limit=1] Pos[0]',
 f'execute store result score #wy {R} run data get entity @e[type=minecraft:marker,tag=riel_w,limit=1] Pos[1]',
 f'execute store result score #wz {R} run data get entity @e[type=minecraft:marker,tag=riel_w,limit=1] Pos[2]',
 f'$execute store result score #tx {R} run data get entity @e[type=minecraft:marker,tag=$(tag),limit=1] Pos[0]',
 f'$execute store result score #ty {R} run data get entity @e[type=minecraft:marker,tag=$(tag),limit=1] Pos[1]',
 f'$execute store result score #tz {R} run data get entity @e[type=minecraft:marker,tag=$(tag),limit=1] Pos[2]',
 '$scoreboard players remove #tx rieles $(sep)',   # cada linea llega por su propia columna (no se cruzan las rampas)
sc('remove #tz',R,'6'),sc('remove #ty',R,'1'),
 sc('operation #remx',R,'=','#tx',R),sc('operation #remx',R,'-=','#wx',R),
 sc('operation #remz',R,'=','#tz',R),sc('operation #remz',R,'-=','#wz',R),
 sc('operation #dy',R,'=','#ty',R),sc('operation #dy',R,'-=','#wy',R),
 sc('set #sx',R,'1'),f'execute if score #remx {R} matches ..-1 run {S} set #sx {R} -1',f'execute if score #remx {R} matches ..-1 run {S} operation #remx {R} *= #-1 {R}',
 sc('set #sz',R,'1'),f'execute if score #remz {R} matches ..-1 run {S} set #sz {R} -1',f'execute if score #remz {R} matches ..-1 run {S} operation #remz {R} *= #-1 {R}',
 sc('operation #ady',R,'=','#dy',R),f'execute if score #ady {R} matches ..-1 run {S} operation #ady {R} *= #-1 {R}',
 'data modify storage granjas:riel p set from storage granjas:riel l',
 sc('set #i',R,'0'),sc('set #corner',R,'0'),sc('set #hecho',R,'0'),
 f'execute if score #remx {R} matches 1.. run function granjas:_rl_ejex',
 f'execute if score #remx {R} matches 0 run function granjas:_rl_ejez',
 # datos de la estacion de salida (relativos al primer riel S)
 sc('operation #fdx',R,'=','#edx',R),sc('operation #fdz',R,'=','#edz',R),sc('operation #fox',R,'=','#eox',R),sc('operation #foz',R,'=','#eoz',R),
 'execute as @e[type=minecraft:marker,tag=riel_w,limit=1] at @s run forceload add ~ ~',
 'schedule function granjas:_rl_tick 1t replace'])
def eje(axis):
    L=[]
    if axis=='x':
        L+=[sc('set #seg',R,'0'),sc('operation #rem',R,'=','#remx',R),sc('set #ult',R,'0'),f'execute if score #remz {R} matches 0 run {S} set #ult {R} 1',
            sc('operation #edx',R,'=','#sx',R),sc('set #edz',R,'0'),sc('set #eox',R,'0'),sc('set #eoz',R,'1'),
            'data modify storage granjas:riel p merge value {shape:"east_west",pshape:"east_west"}',
            f'execute if score #sx {R} matches 1 run data modify storage granjas:riel p merge value {{up:"ascending_east",down:"ascending_west"}}',
            f'execute if score #sx {R} matches -1 run data modify storage granjas:riel p merge value {{up:"ascending_west",down:"ascending_east"}}']
    else:
        L+=[sc('set #seg',R,'1'),sc('operation #rem',R,'=','#remz',R),sc('set #ult',R,'1'),
            sc('set #edx',R,'0'),sc('operation #edz',R,'=','#sz',R),sc('set #eox',R,'1'),sc('set #eoz',R,'0'),
            'data modify storage granjas:riel p merge value {shape:"north_south",pshape:"north_south"}',
            f'execute if score #sz {R} matches 1 run data modify storage granjas:riel p merge value {{up:"ascending_south",down:"ascending_north"}}',
            f'execute if score #sz {R} matches -1 run data modify storage granjas:riel p merge value {{up:"ascending_north",down:"ascending_south"}}']
    L+=[store('p.dx','#edx'),store('p.dz','#edz'),store('p.ox','#eox'),store('p.oz','#eoz'),store('p.fbx','#edx','-32'),store('p.fbz','#edz','-32')]
    return L
W('_rl_ejex',eje('x')); W('_rl_ejez',eje('z'))
W('_rl_esquina',['function granjas:_rl_ejez',sc('set #corner',R,'1'),
 f'execute if score #sx {R} matches 1 if score #sz {R} matches 1 run data modify storage granjas:riel p.shape set value "south_west"',
 f'execute if score #sx {R} matches 1 if score #sz {R} matches -1 run data modify storage granjas:riel p.shape set value "north_west"',
 f'execute if score #sx {R} matches -1 if score #sz {R} matches 1 run data modify storage granjas:riel p.shape set value "south_east"',
 f'execute if score #sx {R} matches -1 if score #sz {R} matches -1 run data modify storage granjas:riel p.shape set value "north_east"'])
W('_rl_tick',[sc('set #pasos',R,'0'),
 'execute as @e[type=minecraft:marker,tag=riel_w,limit=1] at @s run function granjas:_rl_bucle',
 f'execute if score #hecho {R} matches 0 if entity @e[type=minecraft:marker,tag=riel_w] run schedule function granjas:_rl_tick 1t replace'])
W('_rl_bucle',['function granjas:_rpaso',sc('add #i',R,'1'),sc('remove #rem',R,'1'),sc('add #pasos',R,'1'),
 f'execute if score #corner {R} matches 1 if score #seg {R} matches 1 run function granjas:_rl_trasesq',
 f'execute if score #rem {R} matches ..0 run function granjas:_rl_finseg',
 f'execute if score #hecho {R} matches 0 if score #pasos {R} matches ..23 at @s run function granjas:_rl_bucle'])
W('_rl_trasesq',[sc('set #corner',R,'0'),'data modify storage granjas:riel p.shape set value "north_south"'])
W('_rl_finseg',[f'execute if score #seg {R} matches 1 at @s run function granjas:_rl_llegada',
 f'execute if score #seg {R} matches 0 if score #remz {R} matches 0 at @s run function granjas:_rl_llegada',
 f'execute if score #seg {R} matches 0 if score #remz {R} matches 1.. run function granjas:_rl_esquina'])
W('_rpaso',[sc('set #modo',R,'0'),sc('operation #lim',R,'=','#ady',R),sc('add #lim',R,'2'),
 sc('operation #m',R,'=','#i',R),sc('operation #m',R,'%=','#8',R),sc('operation #m6',R,'=','#i',R),sc('operation #m6',R,'%=','#6',R),
 f'execute if score #ult {R} matches 1 if score #corner {R} matches 0 unless score #dy {R} matches 0 if score #rem {R} <= #lim {R} run {S} set #modo {R} 1',
 f'execute if score #modo {R} matches 1 if score #dy {R} matches 1.. run function granjas:_rsube with storage granjas:riel p',
 f'execute if score #modo {R} matches 1 if score #dy {R} matches ..-1 run function granjas:_rbaja with storage granjas:riel p',
 f'execute if score #modo {R} matches 0 run function granjas:_rplano with storage granjas:riel p'])
def lados(y):
    return [f'$execute if block ~$(ox) ~{y} ~$(oz) #minecraft:replaceable unless block ~$(ox) ~{y} ~$(oz) light run setblock ~$(ox) ~{y} ~$(oz) $(fence)',
            f'$execute if block ~-$(ox) ~{y} ~-$(oz) #minecraft:replaceable unless block ~-$(ox) ~{y} ~-$(oz) light run setblock ~-$(ox) ~{y} ~-$(oz) $(fence)']
W('_rplano',[f'execute if score #m {R} matches 0 run forceload add ~ ~',
 f'$execute if score #m {R} matches 0 run forceload remove ~$(fbx) ~$(fbz)']+limpia(1,3)+[
 '$fill ~-$(ox) ~ ~-$(oz) ~$(ox) ~ ~$(oz) $(bed)',
 f'execute if score #m {R} matches 4 if score #corner {R} matches 0 run setblock ~ ~ ~ redstone_block',
 # ojo: un macro con un estado invalido (riel propulsor curvo) anula la funcion entera -> se usa pshape (siempre recto)
 f'$execute if score #m {R} matches 4 if score #corner {R} matches 0 run setblock ~ ~1 ~ powered_rail[shape=$(pshape),powered=true]',
 f'$execute unless score #m {R} matches 4 run setblock ~ ~1 ~ rail[shape=$(shape)]',
 f'$execute if score #m {R} matches 4 if score #corner {R} matches 1 run setblock ~ ~1 ~ rail[shape=$(shape)]',
 'execute if block ~ ~2 ~ air run setblock ~ ~2 ~ light[level=15]']+lados(1)+[
 f'$execute if score #m {R} matches 0 if block ~$(ox) ~1 ~$(oz) $(fence) run setblock ~$(ox) ~2 ~$(oz) $(lamp)',
 f'execute if score #m6 {R} matches 0 positioned ~ ~-1 ~ if block ~ ~ ~ #minecraft:replaceable unless block ~ ~ ~ light run function granjas:_rpilar with storage granjas:riel p',
 '$tp @s ~$(dx) ~ ~$(dz)'])
W('_rpilar',['$setblock ~ ~ ~ $(bed)',
 'execute positioned ~ ~-1 ~ if block ~ ~ ~ #minecraft:replaceable unless block ~ ~ ~ light run function granjas:_rpilar with storage granjas:riel p'])
W('_rsube',limpia(1,4)+['$fill ~-$(ox) ~ ~-$(oz) ~$(ox) ~ ~$(oz) $(bed)','$setblock ~ ~1 ~ rail[shape=$(up)]',
 'execute if block ~ ~3 ~ air run setblock ~ ~3 ~ light[level=15]']+lados(1)+[
 '$tp @s ~$(dx) ~1 ~$(dz)',sc('remove #dy',R,'1'),sc('remove #ady',R,'1')])
W('_rbaja',limpia(0,3)+['$fill ~-$(ox) ~-1 ~-$(oz) ~$(ox) ~-1 ~$(oz) $(bed)','$setblock ~ ~ ~ rail[shape=$(down)]',
 'execute if block ~ ~2 ~ air run setblock ~ ~2 ~ light[level=15]']+lados(0)+[
 '$tp @s ~$(dx) ~-1 ~$(dz)',sc('add #dy',R,'1'),sc('remove #ady',R,'1')])
# estaciones (fx,fz = tope; r1,r2 = rieles de freno; b = boton; a = barril)
def est_datos(ref):
    if ref=='fin':   # relativo al final E (despues del ultimo riel), direccion de llegada d=(edx,edz)
        c=[('fx','#edx','0'),('fz','#edz','0'),('r1x','#edx','-1'),('r1z','#edz','-1'),('r2x','#edx','-2'),('r2z','#edz','-2')]
        L=[store(p,s,k) for p,s,k in c]
        L+=[sc('operation #t',R,'=','#eox',R),sc('operation #t',R,'-=','#edx',R),store('e.bx','#t'),
            sc('operation #t',R,'=','#eoz',R),sc('operation #t',R,'-=','#edz',R),store('e.bz','#t'),
            sc('operation #t',R,'=','#eox',R),sc('operation #t',R,'*=','#-1',R),sc('operation #t',R,'-=','#edx',R),store('e.ax','#t'),
            sc('operation #t',R,'=','#eoz',R),sc('operation #t',R,'*=','#-1',R),sc('operation #t',R,'-=','#edz',R),store('e.az','#t')]
        L=[l.replace('storage granjas:riel fx','storage granjas:riel e.fx').replace('storage granjas:riel fz','storage granjas:riel e.fz')
            .replace('storage granjas:riel r1','storage granjas:riel e.r1').replace('storage granjas:riel r2','storage granjas:riel e.r2') for l in L]
    else:            # relativo al primer riel S, direccion de salida f=(fdx,fdz): tope en S-f
        L=[store('e.fx','#fdx','-1'),store('e.fz','#fdz','-1'),store('e.r1x','#fdx','0'),store('e.r1z','#fdz','0'),store('e.r2x','#fdx'),store('e.r2z','#fdz'),
           store('e.bx','#fox'),store('e.bz','#foz'),store('e.ax','#fox','-1'),store('e.az','#foz','-1')]
    return L
W('_rl_llegada',[sc('set #hecho',R,'1'),
 'data modify storage granjas:riel e set value {}',
 'data modify storage granjas:riel e.bed set from storage granjas:riel p.bed','data modify storage granjas:riel e.lamp set from storage granjas:riel p.lamp',
 'data modify storage granjas:riel e.name set from storage granjas:riel p.name',
 f'execute if score #seg {R} matches 0 run data modify storage granjas:riel e.shape set value "east_west"',
 f'execute if score #seg {R} matches 1 run data modify storage granjas:riel e.shape set value "north_south"']
 +est_datos('fin')+['function granjas:_rl_est with storage granjas:riel e',
 store('p.ady','#ady'),f'execute unless score #ady {R} matches 0 run function granjas:_rl_andamio with storage granjas:riel p',
 # estacion de salida en la estacion central
 sc('operation #t',R,'=','#fdx',R),f'execute if score #fdx {R} matches 0 run {S} set #t {R} 0',
 f'execute if score #fdx {R} matches 0 run data modify storage granjas:riel e.shape set value "north_south"',
 f'execute unless score #fdx {R} matches 0 run data modify storage granjas:riel e.shape set value "east_west"']
 +est_datos('ini')+['data modify storage granjas:riel e.name set value "ESTACION CENTRAL"',
 'execute as @e[type=minecraft:marker,tag=riel_s,limit=1] at @s run function granjas:_rl_est with storage granjas:riel e',
 'kill @e[type=minecraft:marker,tag=riel_w]','kill @e[type=minecraft:marker,tag=riel_s]',
 'tellraw @a [{"text":"[Ferrocarriles] Lista: ","color":"green"},{"storage":"granjas:riel","nbt":"p.name","color":"yellow"}]',
 sc('add #linea',R,'1'),'schedule function granjas:_rl_sig 2t replace'])
W('_rl_est',['$setblock ~$(fx) ~ ~$(fz) $(bed)','$setblock ~$(fx) ~1 ~$(fz) $(bed)','$setblock ~$(fx) ~2 ~$(fz) $(lamp)',
 '$setblock ~$(r1x) ~1 ~$(r1z) powered_rail[shape=$(shape)]','$setblock ~$(r2x) ~1 ~$(r2z) powered_rail[shape=$(shape)]',
 '$setblock ~$(bx) ~1 ~$(bz) $(bed)','$setblock ~$(bx) ~2 ~$(bz) stone_button[face=floor,facing=north]',
 '$setblock ~$(ax) ~1 ~$(az) barrel[facing=up]{Items:[{Slot:0b,id:"minecraft:minecart",count:8}]}',
 '$summon minecraft:text_display ~$(fx) ~3.5 ~$(fz) {billboard:"center",text:{text:"ESTACION - $(name)\\nboton = salir",color:"gold",bold:1b},background:1073741824}'])
# si la fase esta a otra altura y la rampa no alcanzo: columna de andamios al lado del tope
W('_rl_andamio',[sc('operation #c',R,'=','#ady',R),sc('add #c',R,'2'),
 f'$execute if score #dy {R} matches ..-1 positioned ~$(dx) ~-$(ady) ~$(dz) run function granjas:_rand',
 f'$execute if score #dy {R} matches 1.. positioned ~$(dx) ~1 ~$(dz) run function granjas:_rand'])
W('_rand',['setblock ~ ~ ~ scaffolding',sc('remove #c',R,'1'),
 f'execute if score #c {R} matches ..0 run fill ~ ~1 ~ ~ ~2 ~ air',
 f'execute if score #c {R} matches 1.. positioned ~ ~1 ~ run function granjas:_rand'])
W('_rl_fin',['tellraw @a {"text":"[Ferrocarriles] Todas las lineas estan listas. En cada estacion: pon una vagoneta, subete y presiona el boton.","color":"green"}',
 'execute at @e[type=minecraft:marker,tag=granjas_f1,limit=1] run forceload add ~-2 ~-4 ~70 ~26',
 'execute at @e[type=minecraft:marker,tag=granjas_f2,limit=1] run forceload add ~-2 ~-4 ~160 ~48',
 'execute at @e[type=minecraft:marker,tag=granjas_f3,limit=1] run forceload add ~-2 ~-4 ~150 ~74',
 f'execute at {M4} run forceload add ~-4 ~-16 ~94 ~66',
 'execute at @e[type=minecraft:marker,tag=granjas_mega,limit=1] run forceload add ~-115 ~-150 ~115 ~-18',
 'execute at @e[type=minecraft:marker,tag=granjas_mega,limit=1] run forceload add ~-115 ~-17 ~115 ~115'])
W('ferrocarriles',[f'execute unless entity {M4} run tellraw @s {{"text":"Primero construye la Fase 4 (/function granjas:fase4): ahi esta la estacion central.","color":"red"}}',
                   f'execute if entity {M4} run function granjas:_rl_start'])

# =====================================================================
#  ETAPAS
# =====================================================================
EX0,EX1,EZ0,EZ1=-4,94,-16,66
def limpiar4(ya,yb): return [f'fill {C(xa,ya,EZ0)} {C(xb,yb,EZ1)} air' for xa,xb in chunks(EX0,EX1,30)]
def etapa4(n,body,nxt=None,msg=None,delay='3s'):
    L=([f'tellraw @a {{"text":"[Fase 4] {msg}","color":"yellow"}}'] if msg else [])+body
    W(f'_f4_{n}b',L)
    W(f'_f4_{n}',[f'execute at {M4} run function granjas:_f4_{n}b']+([f'schedule function granjas:_f4_{nxt} {delay} replace'] if nxt else []))
W('fase4',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_f4_nueva'])
W('_f4_nueva',['kill @e[type=minecraft:marker,tag=granjas_f4]','summon minecraft:marker ~ ~ ~ {Tags:["granjas_f4"]}','function granjas:_f4_0'])
W('rehacer_fase4',[f'execute unless entity {M4} run tellraw @s {{"text":"No encuentro la Fase 4. Usa /function granjas:fase4 donde la quieras.","color":"red"}}',
                   f'execute at {M4} run function granjas:_f4_0'])
W('_f4_0',[f'execute at {M4} run forceload add ~{EX0} ~{EZ0} ~{EX1} ~{EZ1}',
 'tellraw @a {"text":"[Fase 4] Preparando terreno de 98 x 82 bloques al ESTE y SUR (y el bunker abajo). Tarda como 1 minuto y despues se tienden las vias.","color":"gold"}',
 'schedule function granjas:_f4_1 5s replace'])
etapa4(1,[f'execute positioned {C(EX0,-30,EZ0)} run kill @e[type=!minecraft:player,tag=!granjas_f4,tag=!granjas_f3,tag=!granjas_f2,tag=!granjas_f1,tag=!granjas_mega,tag=!granjas_hub,dx={EX1-EX0},dy=80,dz={EZ1-EZ0}]']
      +limpiar4(1,13)+limpiar4(14,26)+limpiar4(27,39)+[f'fill {C(xa,0,EZ0)} {C(xb,0,EZ1)} grass_block' for xa,xb in chunks(EX0,EX1,30)]
      +[f'fill {C(xa,-3,EZ0)} {C(xb,-1,EZ1)} dirt' for xa,xb in chunks(EX0,EX1,30)]+['kill @e[type=minecraft:item,distance=..150]'],'2','Limpiando terreno...')
caminos4=[f'fill {C(2,0,-6)} {C(4,0,SZ-17)} stone_bricks',f'fill {C(SX+15,0,HZ+20)} {C(HX-2,0,HZ+21)} stone_bricks',
          f'fill {C(BX+23,0,SZ+15)} {C(BX+25,0,BZ+61)} stone_bricks',f'fill {C(BX+23,0,BZ+59)} {C(BX+31,0,BZ+61)} stone_bricks',f'fill {C(3,0,SZ-1)} {C(SX-15,0,SZ+1)} stone_bricks',f'fill {C(3,0,SZ-17)} {C(3,0,SZ)} stone_bricks']
etapa4(2,estacion()+plaza()+caminos4,'3','Estacion central, plaza y estatua...')
etapa4(3,salon(),'4','Salon de cofres gigante...')
etapa4(4,bunker_a()+escalera_bunker(),'5','Bunker: dormitorio, encantamientos, almacen y escalera...')
etapa4(5,bunker_b()+[f'setblock {C(x,1,z)} light[level=15] keep' for x in range(EX0+3,EX1,8) for z in range(EZ0+3,EZ1,8)]
      +['kill @e[type=minecraft:item,distance=..150]','function granjas:respaldo_on',
 'tellraw @a {"text":"[Fase 4] LISTA! Estacion central (norte), estatua en la plaza, salon de cofres (este) y bunker (escalera al sur de la plaza).","color":"green"}',
 'function granjas:_rl_start'],None,'Bunker: granja interna y tradeo...')

W('lista',['tellraw @s {"text":"--- FASES ---\\n/function granjas:fase1   (torre de hierro + criaderos y comercio)\\n/function granjas:fase2   (establo, invernadero, bambu, sandia y calabaza)\\n/function granjas:fase3   (montana con casa, casa del arbol, portales, caballeriza, torre de elitros)\\n/function granjas:fase4   (bunker, estatua, salon de cofres y ferrocarriles)\\n/function granjas:ferrocarriles   (vuelve a tender las vias)\\n/function granjas:rehacer_fase1 ... rehacer_fase4\\n--- SUELTAS (donde estes) ---\\nmontana_natural, arbol, portal_end, portal_nether, caballeriza, torre_elitros, casa_grande, hierro, aldeanos, comercio, bambu, sandia, calabaza, cofres, fuente\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, hierro_vision","color":"aqua"}'])
z=os.path.join(GEN,'build','granjas_datapack.zip')
json.dump({"pack":{"description":"Granjas v11: fases 1 a 4 (megaproyecto completo)","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)
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
        if m and all(re.fullmatch(r'-?\d*',t) for t in m.groups()):
            v=[int(t) if t else 0 for t in m.groups()]
            vol=(abs(v[3]-v[0])+1)*(abs(v[4]-v[1])+1)*(abs(v[5]-v[2])+1)
            if vol>32768: print('GRANDE',fn,vol,line[:60]); bad=1
print('FASE 4:', 'OK' if not bad else 'HAY ERRORES', '->', z)
