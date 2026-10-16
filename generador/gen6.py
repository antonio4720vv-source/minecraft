import os; GEN=os.path.dirname(os.path.abspath(__file__))  # carpeta generador/
exec(open(os.path.join(GEN,'gen5.py'),encoding='utf-8').read().split("# ===================== MEGABASE =====================")[0])
import math, random
random.seed(7)

# ---------- marcadores de produccion en cada granja ----------
def add_marker(fn, pos, tag):
    p=f'{F}/_{fn}.mcfunction'; L=open(p).read().rstrip('\n').split('\n')
    L.insert(len(L)-1, f'summon minecraft:marker {C(*pos)} {{Tags:["{tag}"]}}')
    open(p,'w').write('\n'.join(L)+'\n')
add_marker('hierro',(8,1,8),'go_hierro'); add_marker('cana',(-1,1,0),'go_cana'); add_marker('comida',(-1,1,1),'go_comida')
add_marker('mobs',(8,1,10),'go_mobs'); add_marker('experiencia',(4,1,9),'go_xpbarril'); add_marker('experiencia',(4,1,10),'go_xp')
add_marker('aldeanos',(14,1,5),'go_bebes')
src=open(f'{F}/_comida.mcfunction').read().replace('pumpkin_stem','melon_stem').replace('MELONES y CALABAZAS','SANDIAS').replace('MELONES Y CALABAZAS','SANDIAS').replace('go_comida','go_sandia')
open(f'{F}/_sandia.mcfunction','w').write(src)

L=[]
for _ in range(2): L.append('execute as @e[type=minecraft:marker,tag=go_hierro] at @s run loot insert ~ ~ ~ loot minecraft:entities/iron_golem')
for _ in range(5): L.append('execute as @e[type=minecraft:marker,tag=go_cana] at @s run loot insert ~ ~ ~ loot minecraft:blocks/sugar_cane')
L.append('execute as @e[type=minecraft:marker,tag=go_comida] at @s run loot insert ~ ~ ~ loot minecraft:blocks/melon')
L.append('execute as @e[type=minecraft:marker,tag=go_comida] at @s run loot insert ~ ~ ~ loot minecraft:blocks/pumpkin')
for _ in range(2): L.append('execute as @e[type=minecraft:marker,tag=go_sandia] at @s run loot insert ~ ~ ~ loot minecraft:blocks/melon')
for m in ['creeper','creeper','skeleton','zombie','spider']: L.append(f'execute as @e[type=minecraft:marker,tag=go_mobs] at @s run loot insert ~ ~ ~ loot minecraft:entities/{m}')
L.append('execute as @e[type=minecraft:marker,tag=go_xpbarril] at @s run loot insert ~ ~ ~ loot minecraft:entities/zombie')
L.append('execute as @e[type=minecraft:marker,tag=go_xp] at @s run xp add @a[distance=..6] 30 points')
L.append('scoreboard players add #t granjas 1')
L.append('execute as @e[type=minecraft:marker,tag=go_bebes] at @s store result score @s granjas if entity @e[type=minecraft:villager,distance=..4]')
L.append('execute if score #t granjas matches 10.. as @e[type=minecraft:marker,tag=go_bebes] at @s if score @s granjas matches ..5 run summon minecraft:villager ~ ~ ~ {Age:-24000}')
L.append('execute if score #t granjas matches 10.. run scoreboard players set #t granjas 0')
W('_producir',L)
W('producir',['schedule function granjas:producir 30s replace','execute if score #on granjas matches 1 run function granjas:_producir'])
W('respaldo_on',['scoreboard players set #on granjas 1','schedule function granjas:producir 30s replace',
 'tellraw @a {"text":"Produccion asegurada ACTIVADA: cada 30 segundos las granjas llenan sus barriles aunque el mecanismo falle.","color":"green"}'])

# ---------- casa grande para 2 ----------
p=f'{F}/_casa_grande.mcfunction'; s=open(p).read()
for col in ['green','yellow']: s='\n'.join(l for l in s.split('\n') if f'{col}_bed' not in l)+'\n'
s=s.replace('4 camas','cama doble para 2')
s=s.rstrip('\n')+'\n'
extra=[f'setblock {C(1,6,2)} spruce_trapdoor[half=top,open=false,facing=south]', f'setblock {C(1,7,2)} lantern',
       f'setblock {C(5,6,2)} spruce_trapdoor[half=top,open=false,facing=south]', f'setblock {C(5,7,2)} lantern',
       f'fill {C(9,6,1)} {C(13,6,1)} barrel[facing=south]', f'setblock {C(14,6,1)} crafting_table']
L=s.split('\n'); L[-1:-1]=extra; open(p,'w').write('\n'.join(L))

# ===================== CABALLERIZA =====================
f=Fn('Construyendo CABALLERIZA...')
f.fill((-1,0,-1),(25,12,23),'air'); f.fill((-1,0,-1),(25,0,23),'grass_block')
f.fill((0,0,0),(23,0,10),'spruce_planks')
f.fill((0,1,0),(23,5,10),'spruce_planks'); f.fill((1,1,1),(22,5,9),'air')
for x in range(0,24,4):
    for z in (0,10): f.fill((x,1,z),(x,5,z),'stripped_spruce_log')
for k in range(6):
    y=6+k
    f.fill((-1,y,k-1),(24,y,k-1),'spruce_stairs[facing=south]'); f.fill((-1,y,11-k),(24,y,11-k),'spruce_stairs[facing=north]')
    if k>0: f.fill((0,y,k),(0,y,10-k),'spruce_planks'); f.fill((23,y,k),(23,y,10-k),'spruce_planks')
f.fill((-1,11,4),(24,11,6),'spruce_slab[type=bottom]')
f.fill((0,6,1),(23,6,9),'spruce_planks')
for i in range(5):
    x0=1+i*4
    f.fill((x0,1,4),(x0+2,1,4),'oak_fence'); f.set((x0+1,1,4),'oak_fence_gate[facing=south]')
    if i<4: f.fill((x0+3,1,1),(x0+3,1,3),'oak_fence')
    f.set((x0,1,1),'hay_block'); f.set((x0+2,1,1),'water_cauldron[level=3]')
    f.summon('horse',(x0+1,1,2),'{Tame:1b,PersistenceRequired:1b,Variant:'+str(random.choice([0,1,2,3,4,5,6,256,513,770]))+',equipment:{saddle:{id:"minecraft:saddle",count:1}}}')
    f.set((x0+1,4,2),'lantern[hanging=true]')
f.fill((23,1,5),(23,3,8),'air'); f.fill((23,1,5),(23,1,8),'oak_fence_gate[facing=east]')
f.fill((1,1,9),(3,2,9),'barrel[facing=north]')
f.set((1,1,9),'barrel[facing=north]{Items:[{Slot:0b,id:"minecraft:hay_block",count:64},{Slot:1b,id:"minecraft:golden_carrot",count:64},{Slot:2b,id:"minecraft:lead",count:16},{Slot:3b,id:"minecraft:saddle",count:4}]}')
for x in (6,12,18): f.set((x,5,7),'lantern[hanging=true]')
# corral
f.fill((0,1,12),(23,1,12),'oak_fence'); f.fill((0,1,22),(23,1,22),'oak_fence'); f.fill((0,1,12),(0,1,22),'oak_fence'); f.fill((23,1,12),(23,1,22),'oak_fence')
f.set((12,1,12),'oak_fence_gate[facing=south]')
for x,z in [(0,12),(23,12),(0,22),(23,22),(12,22)]: f.set((x,2,z),'lantern')
for i in range(3): f.summon('horse',(5+i*6,1,17),'{Tame:1b,PersistenceRequired:1b,Variant:'+str(random.choice([1,2,257,514]))+'}')
f.summon('donkey',(10,1,19),'{Tame:1b,PersistenceRequired:1b}')
f.label((24,4,6),'CABALLERIZA\\n5 caballos ensillados','gold')
f.msg('Caballeriza lista: 5 caballos domados y ensillados, corral con 3 caballos y un burro, y un barril con heno, zanahorias doradas, riendas y sillas.')
f.save('caballeriza')

# ===================== CUARTO DE COFRES v2 =====================
cats=[('PIEDRAS',['stone','cobblestone','deepslate','cobbled_deepslate','granite','diorite','andesite','tuff','calcite']),
 ('TIERRA Y ARENA',['dirt','grass_block','sand','red_sand','gravel','clay_ball','terracotta','mud','moss_block']),
 ('MADERA',['oak_log','spruce_log','birch_log','jungle_log','acacia_log','dark_oak_log','mangrove_log','cherry_log','oak_planks']),
 ('MINERALES',['diamond','iron_ingot','gold_ingot','coal','copper_ingot','emerald','lapis_lazuli','quartz','netherite_ingot']),
 ('REDSTONE',['redstone','repeater','comparator','piston','sticky_piston','observer','hopper','dispenser','redstone_torch']),
 ('COMIDA',['bread','cooked_beef','golden_carrot','cooked_porkchop','cooked_chicken','carrot','potato','melon_slice','apple']),
 ('DROPS DE MOBS',['gunpowder','bone','string','rotten_flesh','arrow','spider_eye','ender_pearl','slime_ball','blaze_rod']),
 ('GRANJAS',['sugar_cane','wheat','pumpkin','melon','cactus','bamboo','kelp','egg','leather']),
 ('HERRAMIENTAS Y ARMAS',['diamond_pickaxe','diamond_sword','bow','diamond_axe','diamond_shovel','shield','fishing_rod','shears','crossbow']),
 ('ARMADURAS',['diamond_chestplate','diamond_helmet','diamond_leggings','diamond_boots','iron_chestplate','iron_helmet','iron_leggings','iron_boots','turtle_helmet']),
 ('POCIONES Y LIBROS',['potion','enchanted_book','experience_bottle','glass_bottle','nether_wart','blaze_powder','book','paper','brewing_stand']),
 ('NETHER Y END',['obsidian','netherrack','end_stone','nether_bricks','soul_sand','purpur_block','shulker_shell','chorus_fruit','glowstone_dust'])]
f=Fn('Construyendo CUARTO DE COFRES v2 (12 secciones con marcos)...')
f.fill((-1,0,-1),(27,8,18),'air'); f.fill((-1,0,-1),(27,0,18),'grass_block')
f.fill((0,0,0),(26,0,16),'polished_andesite'); f.fill((4,0,4),(22,0,12),'spruce_planks')
f.fill((0,1,0),(26,6,16),'spruce_planks'); f.fill((1,1,1),(25,5,15),'air')
for x,z in [(0,0),(26,0),(0,16),(26,16)]: f.fill((x,1,z),(x,6,z),'stripped_spruce_log')
def grupo(cells, face_dir, items, name):
    # cells: lista de 3 posiciones (x,z) de columnas; face_dir: hacia donde abren los barriles
    fac={'south':(0,1,3),'north':(0,-1,2),'east':(1,0,5),'west':(-1,0,4)}[face_dir]
    for c,(x,z) in enumerate(cells):
        f.fill((x,1,z),(x,3,z),f'barrel[facing={face_dir}]'); f.set((x,4,z),'spruce_planks')
        f.summon('item_frame',(x+fac[0],4,z+fac[1]),'{Facing:'+str(fac[2])+'b,Fixed:1b,Item:{id:"minecraft:'+items[c]+'",count:1}}')
    mx=sum(p[0] for p in cells)//3; mz=sum(p[1] for p in cells)//3
    f.label((mx+fac[0],5,mz+fac[1]),name,'yellow')
i=0
for gx in (2,6,10,16,20):      # pared sur (z=15), 5 grupos; la puerta va en el norte
    grupo([(gx,15),(gx+1,15),(gx+2,15)],'north',cats[i][1],cats[i][0]); i+=1
for gz in (2,6,10):            # pared oeste
    grupo([(1,gz),(1,gz+1),(1,gz+2)],'east',cats[i][1],cats[i][0]); i+=1
for gz in (2,6,10):            # pared este
    grupo([(25,gz),(25,gz+1),(25,gz+2)],'west',cats[i][1],cats[i][0]); i+=1
grupo([(14,15),(15,15),(13,15)],'north',cats[i][1],cats[i][0]) if False else None
f.set((13,1,15),'barrel[facing=north]'); f.set((14,1,15),'barrel[facing=north]')
for x in (13,14): f.set((x,2,15),'barrel[facing=north]'); f.set((x,3,15),'barrel[facing=north]')
f.label((13,5,14),cats[11][0] if False else 'EXTRA','yellow')
for x in range(4,24,5):
    for z in (4,8,12): f.set((x,6,z),'glowstone')
for x in (9,17): f.set((x,1,8),'crafting_table')
f.set((13,1,8),'ender_chest[facing=north]'); f.set((11,1,8),'anvil[facing=east]'); f.set((15,1,8),'stonecutter[facing=north]')
f.fill((12,1,1),(14,3,1),'air')
f.set((12,1,0),'iron_door[half=lower,facing=south,hinge=left]'); f.set((12,2,0),'iron_door[half=upper,facing=south,hinge=left]')
f.set((14,1,0),'iron_door[half=lower,facing=south,hinge=right]'); f.set((14,2,0),'iron_door[half=upper,facing=south,hinge=right]')
f.set((13,1,0),'spruce_planks'); f.set((13,2,0),'spruce_planks')
f.set((13,2,-1),'stone_button[face=wall,facing=north]'); f.set((13,2,1),'stone_button[face=wall,facing=south]')
for x in (3,4,8,9,17,18,22,23): f.fill((x,2,0),(x,3,0),'glass_pane[east=true,west=true]')
f.label((13,4,-1),'CUARTO DE COFRES')
f.msg('Cuarto de cofres listo: 12 secciones (cada barril tiene un marco con el objeto que va ahi), cofre de ender, yunque, cortapiedras y mesas de crafteo.')
f.save('cofres')
# la pared sur solo tiene 5 grupos; la seccion 12 (NETHER Y END) va en las columnas del medio
p=f'{F}/_cofres.mcfunction'; s=open(p).read()
s=s.replace('"text":"EXTRA"','"text":"NETHER Y END"')
open(p,'w').write(s)

# ===================== CASA EN EL ARBOL =====================
f=Fn('Construyendo CASA EN EL ARBOL con ascensor...')
f.fill((-10,0,-10),(10,20,10),'air'); f.fill((-10,21,-10),(10,34,10),'air'); f.fill((-10,0,-10),(10,0,10),'grass_block')
f.fill((-2,1,-2),(1,30,1),'dark_oak_log')
for x,z,dx,dz in [(-3,-3,-1,-1),(2,-3,1,-1),(-3,2,-1,1),(2,2,1,1)]:
    f.fill((x,0,z),(x,1,z),'dark_oak_wood'); f.set((x+dx,0,z+dz),'dark_oak_wood')
f.set((-1,0,-1),'soul_sand'); f.fill((-1,1,-1),(-1,18,-1),'bubble_column[drag=false]')
f.fill((-1,19,-1),(-1,20,-1),'air'); f.fill((-2,19,-1),(-2,20,-1),'air')
f.set((-2,1,-1),'oak_door[half=lower,facing=east,hinge=left]'); f.set((-2,2,-1),'oak_door[half=upper,facing=east,hinge=left]')
f.fill((0,1,0),(0,20,0),'ladder[facing=north]'); f.fill((1,1,0),(1,2,0),'air'); f.fill((1,19,0),(1,20,0),'air')
f.label((-4,4,-1),'ASCENSOR (sube)','aqua'); f.label((3,4,0),'ESCALERA','aqua')
# plataforma
for dz in range(-8,9):
    w=int(math.sqrt(max(64-dz*dz,0)))
    f.fill((-w,18,dz),(w,18,dz),'spruce_planks')
f.fill((-2,18,-2),(1,18,1),'dark_oak_log'); f.set((-1,18,-1),'bubble_column[drag=false]'); f.set((0,18,0),'ladder[facing=north]')
for dz in range(-8,9):
    w=int(math.sqrt(max(64-dz*dz,0)))
    f.set((-w,19,dz),'oak_fence'); f.set((w,19,dz),'oak_fence')
f.fill((-8,19,0),(-8,19,0),'oak_fence'); f.fill((-2,19,8),(2,19,8),'oak_fence'); f.fill((-2,19,-8),(2,19,-8),'oak_fence')
# cabana
f.fill((-6,19,-6),(5,22,5),'oak_planks'); f.fill((-5,19,-5),(4,22,4),'air'); f.fill((-2,19,-2),(1,22,1),'dark_oak_log')
f.fill((-1,19,-1),(-1,20,-1),'air'); f.fill((-2,19,-1),(-2,20,-1),'air'); f.fill((0,19,0),(0,20,0),'ladder[facing=north]'); f.fill((1,19,0),(1,20,0),'air')
for x,z in [(-6,-6),(5,-6),(-6,5),(5,5)]: f.fill((x,19,z),(x,22,z),'stripped_oak_log')
f.fill((-6,23,-6),(5,23,5),'spruce_slab[type=bottom]')
for x in (-4,-3,2,3): f.fill((x,20,-6),(x,21,-6),'glass_pane[east=true,west=true]'); f.fill((x,20,5),(x,21,5),'glass_pane[east=true,west=true]')
for z in (-4,-3,2,3): f.fill((-6,20,z),(-6,21,z),'glass_pane[north=true,south=true]'); f.fill((5,20,z),(5,21,z),'glass_pane[north=true,south=true]')
f.set((-1,19,5),'oak_door[half=lower,facing=north,hinge=left]'); f.set((-1,20,5),'oak_door[half=upper,facing=north,hinge=left]')
f.bed((-4,19,-3),(-4,19,-4),'lime','north'); f.bed((-3,19,-3),(-3,19,-4),'lime','north')
f.fill((3,19,-5),(4,20,-5),'barrel[facing=south]'); f.set((4,19,-3),'crafting_table'); f.set((4,19,-2),'furnace[facing=west]')
f.fill((-4,19,1),(-3,19,3),'green_carpet')
for p in [(-4,22,0),(3,22,2),(3,22,-3)]: f.set(p,'lantern[hanging=true]')
# copa del arbol
for y,r in [(24,7),(25,8),(26,8),(27,8),(28,7),(29,6),(30,5),(31,4),(32,2)]:
    f.fill((-r,y,-r//2),(r,y,r//2),'oak_leaves[persistent=true]','replace air'); f.fill((-r//2,y,-r),(r//2,y,r),'oak_leaves[persistent=true]','replace air')
    q=int(r*0.75); f.fill((-q,y,-q),(q,y,q),'oak_leaves[persistent=true]','replace air')
for y,r in [(16,6),(17,7)]:
    f.fill((-r,y,-1),(r,y,0),'oak_leaves[persistent=true]','replace air'); f.fill((-1,y,-r),(0,y,r),'oak_leaves[persistent=true]','replace air')
f.fill((-1,1,-1),(-1,18,-1),'bubble_column[drag=false]')
for x,z in [(3,3),(-4,-4),(3,-4),(-4,3)]: f.set((x,1,z),'lantern')
f.label((0,26,0) if False else (0,3,-4),'CASA EN EL ARBOL','gold')
f.msg('Casa en el arbol lista: entra por la puerta del lado oeste del tronco y la columna de agua te sube. Para bajar usa la escalera de mano (puerta del lado este).')
f.save('arbol')

# ===================== FUENTE MONUMENTAL CON FARO =====================
f=Fn('Construyendo FUENTE con faro en el centro...')
f.fill((-10,0,-10),(10,12,10),'air'); f.fill((-10,0,-10),(10,0,10),'polished_andesite')
for dz in range(-9,10):
    w=int(math.sqrt(max(81-dz*dz,0))); f.fill((-w,0,dz),(w,1,dz),'stone_bricks')
for dz in range(-8,9):
    w=int(math.sqrt(max(64-dz*dz,0))); f.fill((-w,1,dz),(w,1,dz),'water'); f.fill((-w,0,dz),(w,0,dz),'prismarine_bricks')
for x,z in [(-5,0),(5,0),(0,-5),(0,5),(-4,-4),(4,-4),(-4,4),(4,4)]: f.set((x,0,z),'sea_lantern')
f.fill((-1,1,-1),(1,5,1),'quartz_pillar'); f.fill((-1,6,-1),(1,6,1),'iron_block'); f.set((0,7,0),'beacon')
for x,z in [(-2,0),(2,0),(0,-2),(0,2)]: f.set((x,5,z),'water')
for x,z in [(-2,-2),(2,-2),(-2,2),(2,2)]: f.fill((x,1,z),(x,2,z),'quartz_block'); f.set((x,3,z),'end_rod[facing=up]')
f.label((0,10,0),'PLAZA CENTRAL','aqua')
f.msg('Fuente con faro lista.')
f.save('fuente')

# ===================== EDIFICIO DE GRANJAS (pisos) =====================
FL=[0,8,18,25,33,51]; TOP=73
f=Fn('Construyendo EDIFICIO DE GRANJAS de 6 pisos...')
f.fill((-8,0,-2),(53,TOP+2,29),'air') if False else None
for ya,yb in [(1,25),(26,50),(51,TOP+2)]:
    for xa,xb in [(-8,22),(23,53)]: f.fill((xa,ya,-2),(xb,yb,29),'air')
f.fill((-8,0,-2),(53,0,29),'stone_bricks')
def floor_slab(y,blk='stone_bricks',mode=''):
    for xa,xb in [(-1,25),(26,52)]: f.fill((xa,y,-1),(xb,y,28),blk,mode)
def farm(fn,ox,oy,oz): f.L.append(f'execute positioned ~{ox} ~{oy} ~{oz} run function granjas:_{fn}')
# piso 0: hornos
for k in range(3): farm('hornos',3+k*16,0,4)
floor_slab(0,'stone_bricks','replace air')
# piso 1: cana / sandia / comida
floor_slab(FL[1])
for k,n in enumerate(['cana','cana','cana']): farm(n,3+k*17,FL[1],5)
for k,n in enumerate(['sandia','sandia','comida']): farm(n,3+k*17,FL[1],16)
floor_slab(FL[1],'stone_bricks','replace air')
# piso 2: criaderos
floor_slab(FL[2]); farm('aldeanos',3,FL[2],1); farm('aldeanos',29,FL[2],1); floor_slab(FL[2],'stone_bricks','replace air')
# piso 3: comercio
floor_slab(FL[3]); farm('comercio',4,FL[3],4); floor_slab(FL[3],'stone_bricks','replace air')
# piso 4: hierro x2 (piso de vidrio para que los golems no aparezcan fuera)
floor_slab(FL[4],'glass'); farm('hierro',4,FL[4],3); farm('hierro',30,FL[4],3); floor_slab(FL[4],'glass','replace air')
# piso 5: experiencia
floor_slab(FL[5]); farm('experiencia',3,FL[5],2); floor_slab(FL[5],'stone_bricks','replace air')
floor_slab(TOP)
f.save('edif_a')

f=Fn('Edificio: paredes, ventanas, escaleras y luces...')
# paredes
for ya,yb in [(1,36),(37,TOP)]:
    f.fill((-1,ya,-1),(52,yb,-1),'stone_bricks'); f.fill((-1,ya,28),(52,yb,28),'stone_bricks')
    f.fill((-1,ya,-1),(-1,yb,28),'stone_bricks'); f.fill((52,ya,-1),(52,yb,28),'stone_bricks')
for y in FL:
    f.fill((0,y+2,-1),(51,y+3,-1),'glass'); f.fill((0,y+2,28),(51,y+3,28),'glass'); f.fill((52,y+2,0),(52,y+3,27),'glass')
for x in range(-1,53,6):
    for z in (-1,28): f.fill((x,1,z),(x,TOP,z),'stone_brick_wall') if False else f.fill((x,1,z),(x,TOP,z),'chiseled_stone_bricks')
f.fill((25,1,28),(27,3,28),'air')                                     # entrada principal (sur)
f.fill((24,0,29),(28,0,31),'polished_andesite'); f.set((24,1,29),'lantern'); f.set((28,1,29),'lantern')
f.fill((-1,TOP+1,-1),(52,TOP+1,-1),'stone_brick_wall'); f.fill((-1,TOP+1,28),(52,TOP+1,28),'stone_brick_wall')
f.fill((-1,TOP+1,-1),(-1,TOP+1,28),'stone_brick_wall'); f.fill((52,TOP+1,-1),(52,TOP+1,28),'stone_brick_wall')
# escaleras (lado oeste)
for ya,yb in [(1,37),(38,TOP+1)]:
    f.fill((-7,ya,-1),(-7,yb,28),'stone_bricks'); f.fill((-7,ya,-1),(-1,yb,-1),'stone_bricks'); f.fill((-7,ya,28),(-1,yb,28),'stone_bricks')
    f.fill((-6,ya,0),(-2,yb,27),'air'); f.fill((-4,ya,0),(-4,yb,27),'glass')
f.fill((-7,TOP+1,-1),(-1,TOP+1,28),'stone_bricks'); f.fill((-6,0,0),(-2,0,27),'stone_bricks')
s=[4]
for k in range(5):
    d=1 if k%2==0 else -1; Dy=FL[k+1]-FL[k]; s.append(s[k]+d*(Dy+1))
for k in range(6):
    y,z=FL[k],s[k]
    f.fill((-6,y,z),(-2,y,z),'stone_bricks'); f.fill((-4,y+1,z),(-4,y+3,z),'air')
    f.fill((-1,y+1,z),(-1,y+2,z),'air')
    f.set((-6,y+3,z),'lantern[hanging=true]') if False else None
for k in range(5):
    d=1 if k%2==0 else -1; Dy=FL[k+1]-FL[k]; lane=(-3,-2) if k%2==0 else (-6,-5)
    for i in range(1,Dy+1):
        z=s[k]+d*i
        f.fill((lane[0],FL[k]+i,z),(lane[1],FL[k]+i,z),f'stone_brick_stairs[facing={"south" if d>0 else "north"}]')
        f.fill((lane[0],FL[k]+i+1,z),(lane[1],FL[k]+i+3,z),'air')
# luces invisibles (solo en aire) para que no aparezcan monstruos adentro
lights={0:[3],1:[3,7],2:[3],3:[3],4:[3,9,15],5:[3,9,19]}
for k,ys in lights.items():
    for dy in ys:
        for x in range(2,52,6):
            for z in range(2,28,6): f.L.append(f'setblock {C(x,FL[k]+dy,z)} light[level=15] keep')
for y in range(3,TOP,5):
    for z in range(2,28,5): f.L.append(f'setblock {C(-3,y,z)} light[level=15] keep'); f.L.append(f'setblock {C(-6,y,z)} light[level=15] keep')
f.label((26,5,30),'EDIFICIO DE GRANJAS\\npiso 0: hornos | 1: cana y sandia | 2: criaderos\\n3: comercio | 4: hierro | 5: experiencia\\nescaleras: puerta del lado oeste','gold')
f.msg('Edificio de granjas listo. Entra por el sur; las escaleras estan en el lado oeste (puerta en cada piso).')
f.save('edif_b')
W('edificio_granjas',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_edificio_granjas'])
W('_edificio_granjas',['function granjas:_edif_a','function granjas:_edif_b'])

# ===================== PAISAJE: MONTANAS ALREDEDOR =====================
hills=[(-70,-122,22,26),(0,-128,20,30),(70,-122,22,24),(-100,-60,14,18),(100,-70,15,20),(102,15,13,16),(100,85,15,20),(40,100,14,18),(-30,100,14,16),(-100,95,14,18)]
P=['tellraw @s {"text":"Construyendo montanas alrededor...","color":"yellow"}']
for cx,cz,r,h in hills:
    jx=jz=0
    for t in range(1,h+1):
        rt=r*(1-t/(h+2))**0.8
        if rt<1: break
        jx=max(-2,min(2,jx+random.choice([-1,0,0,1]))); jz=max(-2,min(2,jz+random.choice([-1,0,0,1])))
        blk='grass_block' if t<h*0.55 else ('stone' if t<h-3 or h<20 else 'snow_block')
        a=int(rt); b=max(1,int(rt*0.45)); c=max(1,int(rt*0.75))
        for (x0,x1,z0,z1) in [(-a,a,-b,b),(-b,b,-a,a),(-c,c,-c,c)]:
            P.append(f'fill {C(cx+jx+x0,t,cz+jz+z0)} {C(cx+jx+x1,t,cz+jz+z1)} {blk}')
W('_paisaje',P)

# ===================== TREN (vagonetas) =====================
R=['tellraw @s {"text":"Construyendo el tren circular con estaciones...","color":"yellow"}']
X0L,X1L,Z0L,Z1L=-45,45,-40,40
stations=[(4,-40,'GRANJAS'),(28,-40,'PORTAL DEL END'),(45,-20,'CASA EN EL ARBOL'),(45,30,'TORRE DE ELITROS'),
          (23,40,'CUARTO DE COFRES'),(2,40,'PLAZA'),(-12,40,'ANIMALES'),(-36,40,'CASA EN LA MONTANA'),
          (-45,0,'CABALLERIZA'),(-45,-30,'GRANJA DE MOBS')]
path=[]
for x in range(X0L,X1L+1): path.append((x,Z0L))
for z in range(Z0L+1,Z1L+1): path.append((X1L,z))
for x in range(X1L-1,X0L-1,-1): path.append((x,Z1L))
for z in range(Z1L-1,Z0L,-1): path.append((X0L,z))
corner={(X0L,Z0L):'south_east',(X1L,Z0L):'south_west',(X1L,Z1L):'north_west',(X0L,Z1L):'north_east'}
# base y despeje
for (a,b) in [((X0L,Z0L),(X1L,Z0L)),((X0L,Z1L),(X1L,Z1L)),((X0L,Z0L),(X0L,Z1L)),((X1L,Z0L),(X1L,Z1L))]:
    R.append(f'fill {C(a[0],1,a[1])} {C(b[0],3,b[1])} air'); R.append(f'fill {C(a[0],0,a[1])} {C(b[0],0,b[1])} stone_bricks')
R.append(f'fill {C(X0L+1,1,Z0L)} {C(X1L-1,1,Z0L)} rail[shape=east_west]'); R.append(f'fill {C(X0L+1,1,Z1L)} {C(X1L-1,1,Z1L)} rail[shape=east_west]')
R.append(f'fill {C(X0L,1,Z0L+1)} {C(X0L,1,Z1L-1)} rail[shape=north_south]'); R.append(f'fill {C(X1L,1,Z0L+1)} {C(X1L,1,Z1L-1)} rail[shape=north_south]')
for (x,z),sh in corner.items(): R.append(f'setblock {C(x,1,z)} rail[shape={sh}]')
def shape_at(x,z): return 'east_west' if z in (Z0L,Z1L) and x not in (X0L,X1L) else 'north_south'
st_pos=set((x,z) for x,z,_ in stations)
def near_station(x,z): return any(abs(x-a)+abs(z-b)<=4 for a,b in st_pos)
for idx,(x,z) in enumerate(path):
    if (x,z) in corner or idx%8: continue
    if any(abs(x-a)+abs(z-b)<=3 for a,b in corner): continue
    if near_station(x,z): continue
    R.append(f'setblock {C(x,0,z)} redstone_block'); R.append(f'setblock {C(x,1,z)} powered_rail[shape={shape_at(x,z)},powered=true]')
for x,z,name in stations:
    sh=shape_at(x,z)
    if sh=='east_west': nxt=(x+1,z); side=(0,1) if z==Z0L else (0,-1)
    else: nxt=(x,z+1); side=(1,0) if x==X0L else (-1,0)
    for (a,b) in [(x,z),nxt]: R.append(f'setblock {C(a,1,b)} powered_rail[shape={sh},powered=false]')
    R.append(f'setblock {C(x+side[0],1,z+side[1])} stone_bricks'); R.append(f'setblock {C(x+side[0],2,z+side[1])} stone_button[face=floor,facing=north]')
    R.append(f'setblock {C(x-side[0],1,z-side[1])} barrel[facing=up]{{Items:[{{Slot:0b,id:"minecraft:minecart",count:8}}]}}')
    R.append(f'summon minecraft:text_display {C(x,4,z)} {{billboard:"center",text:{{text:"ESTACION: {name}",color:"aqua",bold:1b}},background:1073741824}}')
W('_tren',R)

# ===================== ARBOLES Y FLORES =====================
T=[]
trees=[(-35,-30,'fancy_oak'),(-25,-24,'birch'),(-36,-16,'oak'),(-22,-34,'cherry'),(40,-12,'fancy_oak'),(39,-30,'birch'),(18,-36,'oak') ,
       (-35,25,'cherry'),(-24,32,'fancy_oak'),(-37,15,'birch'),(35,25,'cherry'),(26,32,'oak'),(38,15,'fancy_oak'),
       (60,-30,'birch'),(72,-26,'fancy_oak'),(82,-38,'oak'),(62,24,'cherry'),(-66,24,'birch'),(-82,30,'fancy_oak'),(-92,0,'oak'),(-96,-26,'birch'),
       (-20,-90,'fancy_oak'),(25,-88,'cherry'),(80,10,'birch'),(85,-15,'oak')]
for x,z,t in trees: T.append(f'place feature minecraft:{t} {C(x,1,z)}')
for x,z in [(-30,-28),(30,30),(-28,30),(32,-12),(70,-30),(-80,25),(0,-85)]: T.append(f'place feature minecraft:flower_default {C(x,1,z)}')
W('_arboles',T)

# ===================== MEGABASE v7 =====================
MHUB='@e[type=minecraft:marker,tag=granjas_mega,limit=1]'
RX0,RX1,RZ0,RZ1=-115,115,-150,115
def stage(name,body,nxt=None,msg=None,delay='4s'):
    L=[]
    if msg: L.append(f'tellraw @a {{"text":"{msg}","color":"yellow"}}')
    L+=body
    W(f'_{name}b',L)
    W(f'_{name}',[f'execute at {MHUB} run function granjas:_{name}b']+([f'schedule function granjas:_{nxt} {delay} replace'] if nxt else []))
W('megabase',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_mega_nueva'])
W('_mega_nueva',['kill @e[type=minecraft:marker,tag=granjas_mega]','summon minecraft:marker ~ ~ ~ {Tags:["granjas_mega"]}','function granjas:_mega0'])
W('rehacer_megabase',[f'execute unless entity {MHUB} run tellraw @s {{"text":"No encuentro la megabase anterior. Usa /function granjas:megabase donde la quieras.","color":"red"}}',
                      f'execute at {MHUB} run function granjas:_mega0'])
W('_mega0',[
 f'forceload add ~{RX0} ~{RZ0} ~{RX1} ~-18', f'forceload add ~{RX0} ~-17 ~{RX1} ~{RZ1}',
 'tellraw @a {"text":"MEGABASE v7: borrando y preparando el terreno (230 x 265 bloques). Tarda como 1 minuto y el servidor se puede trabar. NO te vayas lejos.","color":"gold"}',
 'schedule function granjas:_mega1 8s replace'])
def flat_stage(ya,yb):
    L=[]
    for xa,xb in chunks(RX0,RX1,30):
        for za,zb in chunks(RZ0,RZ1,30): L.append(f'fill {C(xa,ya,za)} {C(xb,yb,zb)} air')
    return L
def floor_stage():
    L=[]
    for xa,xb in chunks(RX0,RX1,30):
        for za,zb in chunks(RZ0,RZ1,30): L.append(f'fill {C(xa,0,za)} {C(xb,0,zb)} grass_block'); L.append(f'fill {C(xa,-3,za)} {C(xb,-1,zb)} dirt')
    return L
stage('mega1',[f'execute positioned {C(RX0,-6,RZ0)} run kill @e[type=!minecraft:player,tag=!granjas_mega,tag=!granjas_hub,dx={RX1-RX0},dy=90,dz={RZ1-RZ0}]']+flat_stage(1,18),'mega2','Aplanando (1/4)...')
stage('mega2',flat_stage(19,36),'mega3','Aplanando (2/4)...')
stage('mega3',flat_stage(37,54),'mega4','Aplanando (3/4)...')
stage('mega4',flat_stage(55,80)[:0]+[l for l in flat_stage(55,72)]+floor_stage()+['kill @e[type=minecraft:item,distance=..300]'],'mega5','Aplanando (4/4)...')
plaza=[f'tp @a[distance=..14] ~ ~1 ~18', f'fill {C(-14,0,-14)} {C(14,0,14)} polished_andesite',
       f'fill {C(-1,0,-42)} {C(1,0,-15)} stone_bricks', f'fill {C(-1,0,15)} {C(1,0,43)} stone_bricks',
       f'fill {C(15,0,-1)} {C(54,0,1)} stone_bricks', f'fill {C(-48,0,-1)} {C(-15,0,1)} stone_bricks',
       'function granjas:_fuente','execute positioned ~28 ~ ~-25 run function granjas:_portal_end']
stage('mega5',plaza,'mega6','Construyendo plaza, fuente y portal del End...')
stage('mega6',['execute positioned ~-26 ~ ~-70 run function granjas:_edif_a'],'mega7','Construyendo el edificio de granjas (pisos)...','6s')
stage('mega7',['execute positioned ~-26 ~ ~-70 run function granjas:_edif_b','execute positioned ~-78 ~ ~-55 run function granjas:_mobs'],'mega8','Paredes, escaleras y granja de mobs...')
stage('mega8',['execute positioned ~-60 ~ ~70 run function granjas:_montana','execute positioned ~-72 ~ ~-12 run function granjas:_caballeriza'],'mega9','Montana con la casa y caballeriza...')
stage('mega9',['execute positioned ~-18 ~ ~45 run function granjas:_animales','execute positioned ~10 ~ ~45 run function granjas:_cofres',
               'execute positioned ~52 ~ ~48 run function granjas:_torre_elitros','execute positioned ~65 ~ ~0 run function granjas:_arbol'],'mega10','Animales, cofres, torre de elitros y casa en el arbol...')
golems=[]
for x,z in [(-10,-10),(10,-10),(-10,10),(10,10),(-38,-33),(38,-33),(-38,33),(38,33),(-55,15),(60,15),(0,-30),(0,30)]:
    golems.append(f'summon minecraft:iron_golem {C(x,1,z)} {{PlayerCreated:1b,PersistenceRequired:1b,CustomName:"Guardian"}}')
luces=[]
for x in range(RX0+3,RX1,8):
    for z in range(RZ0+3,RZ1,8): luces.append(f'setblock {C(x,1,z)} light[level=15] keep')
stage('mega10',['function granjas:_paisaje','function granjas:_arboles','function granjas:_tren']+golems,'mega11','Montanas, arboles, tren y golems guardianes...')
stage('mega11',luces+['function granjas:respaldo_on',
 f'summon minecraft:text_display {C(0,6,16)} {{billboard:"center",text:{{text:"MEGABASE\\nTren circular: estaciones en cada lugar\\nboton = arrancar  |  W = avanzar",color:"gold",bold:1b}}}}',
 'tellraw @a {"text":"MEGABASE v7 TERMINADA! Usa el tren circular: subete a una vagoneta en cualquier estacion, presiona el boton y luego W.","color":"green"}'],None,'Iluminando todo para que no aparezcan monstruos...')

def HR(x,y,z): return f'~{x-8} ~{y-1} ~{z-8}'      # coordenadas de la granja relativas a su marker go_hierro (8,1,8)
W('_hierro_vision',[
 f'kill @e[type=minecraft:zombie,name=Asustador,distance=..14]',
 f'fill {HR(6,11,6)} {HR(10,11,7)} air replace minecraft:red_bed',
 *[f'setblock {HR(x,11,10)} red_bed[facing=south,part=foot]' for x in (6,8,10)],
 *[f'setblock {HR(x,11,11)} red_bed[facing=south,part=head]' for x in (6,8,10)],
 f'fill {HR(6,10,13)} {HR(11,13,17)} air',
 f'fill {HR(6,10,13)} {HR(11,10,14)} smooth_stone', f'fill {HR(6,11,13)} {HR(11,12,14)} glass', f'fill {HR(7,11,13)} {HR(10,12,13)} air',
 f'fill {HR(6,13,13)} {HR(11,13,14)} glass', f'fill {HR(7,12,12)} {HR(10,12,12)} air',
 f'fill {HR(0,6,0)} {HR(17,6,17)} air replace water', f'fill {HR(8,5,0)} {HR(9,5,17)} air',
 f'fill {HR(0,6,0)} {HR(0,6,17)} water', f'fill {HR(17,6,0)} {HR(17,6,17)} water',
 f'fill {HR(8,5,0)} {HR(9,5,0)} water', f'fill {HR(8,5,17)} {HR(9,5,17)} water',
 f'summon minecraft:zombie {HR(8,11,13)} {{PersistenceRequired:1b,CustomName:"Asustador",equipment:{{head:{{id:"minecraft:carved_pumpkin",count:1}}}},drop_chances:{{head:0.0f}}}}'])
# ---------- ARREGLO para granjas de hierro ya construidas (los golems no aparecian) ----------
W('hierro_vision',['execute as @e[type=minecraft:marker,tag=go_hierro] at @s run function granjas:_hierro_vision',
 'execute store result score #n granjas if entity @e[type=minecraft:marker,tag=go_hierro]',
 'tellraw @s [{"text":"Granjas de hierro arregladas: ","color":"green"},{"score":{"name":"#n","objective":"granjas"},"color":"yellow"},{"text":". Se arreglo el agua (los golems se quedaban parados) y las camas se movieron junto al zombi. Los aldeanos tienen que DORMIR una noche antes de que aparezcan golems.","color":"green"}]'])

W('lista',['tellraw @s {"text":"--- TODO JUNTO ---\\n/function granjas:megabase   (nueva, donde estes)\\n/function granjas:rehacer_megabase   (borra y rehace la anterior en el mismo lugar)\\n--- SUELTAS (donde estes parado) ---\\nedificio_granjas, mobs, caballeriza, arbol, fuente, cofres, animales, casa_grande, montana, portal_end, torre_elitros, casa, cana, sandia\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, hierro_vision","color":"aqua"}'])
for n in ['caballeriza','arbol','fuente','cofres']:
    W(n,[f'execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_{n}'])
W('ayuda',['scoreboard objectives add granjas dummy','execute unless score #on granjas matches 0..1 run scoreboard players set #on granjas 0',
 'schedule function granjas:producir 30s replace','tellraw @a {"text":"[Granjas v7] /function granjas:lista  para ver todos los comandos","color":"gold"}'])
json.dump({"pack":{"description":"Granjas v7: megabase con tren, edificio de granjas y mas","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)
for n in ['_mega1b','_mega2b','_mega3b','_mega4b','_mega5b','_mega6b','_mega7b','_mega8b','_mega9b']: pass

z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
import re
ok_cmds={'fill','setblock','summon','tellraw','execute','function','kill','forceload','schedule','data','loot','scoreboard','tp','place','xp'}
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
            if vol>32768: print('GRANDE',fn,vol,line[:70]); bad=1
print('OK' if not bad else 'HAY ERRORES', total,'lineas')
