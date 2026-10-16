import os; GEN=os.path.dirname(os.path.abspath(__file__))  # carpeta generador/
exec(open(os.path.join(GEN,'gen2.py'),encoding='utf-8').read().split("# ================= TODAS EN FILA")[0])

# ================= CANA DE AZUCAR (observador + piston, carritos tolva) =================
N=12
f=Fn('Construyendo granja de CANA DE AZUCAR...')
f.fill((-3,0,-4),(N+1,8,3),'air'); f.fill((-3,0,-4),(N+1,0,3),'stone_bricks')
f.fill((-1,1,-3),(N,7,2),'stone_bricks')
f.fill((0,1,0),(N-1,1,0),'hopper[facing=west]'); f.set((-1,1,0),'barrel[facing=west]')
f.fill((0,2,0),(N-1,2,0),'rail[shape=east_west]')
f.fill((0,3,0),(N-1,3,0),'sand'); f.fill((0,3,1),(N-1,3,1),'water')
f.fill((0,4,0),(N-1,6,0),'air'); f.fill((-1,4,1),(N,7,1),'glass'); f.fill((-1,4,0),(-1,7,0),'glass'); f.fill((N,4,0),(N,7,0),'glass')
f.fill((0,4,0),(N-1,4,0),'sugar_cane')
f.fill((0,5,-1),(N-1,5,-1),'piston[facing=south]')
f.fill((0,6,-1),(N-1,6,-1),'observer[facing=south]')
f.fill((0,6,-2),(N-1,6,-2),'redstone_wire'); f.fill((-1,6,-3),(N,7,-3),'stone_bricks'); f.fill((-1,7,-2),(N,7,0),'glass')
for x in range(N): f.summon('hopper_minecart',(x,2,0))
f.label((-2,3,0),'CANA DE AZUCAR\\ncofre aqui abajo')
f.msg('Granja de cana lista. Es automatica: cuando la cana crece 3 bloques, los pistones la cortan y llega sola al cofre del lado oeste.')
f.save('cana')

# ================= MELONES Y CALABAZAS (comida + esmeraldas) =================
N=12
f=Fn('Construyendo granja de MELONES y CALABAZAS...')
f.fill((-3,0,-3),(N+1,8,4),'air'); f.fill((-3,0,-3),(N+1,0,4),'stone_bricks')
f.fill((-1,1,-2),(N,3,3),'stone_bricks')
f.fill((0,1,0),(N-1,1,0),'hopper[facing=south]'); f.fill((0,1,1),(N-1,1,1),'hopper[facing=west]'); f.set((-1,1,1),'barrel[facing=west]')
f.fill((0,2,0),(N-1,2,1),'rail[shape=east_west]')
f.fill((0,3,0),(N-1,3,0),'farmland[moisture=7]'); f.fill((0,3,1),(N-1,3,1),'dirt'); f.fill((0,3,-1),(N-1,3,-1),'water')
f.fill((-1,4,-1),(N,6,-1),'glass'); f.fill((-1,4,0),(-1,6,3),'glass'); f.fill((N,4,0),(N,6,3),'glass')
for x in range(N):
    f.set((x,4,0),('melon_stem' if x%2==0 else 'pumpkin_stem')+'[age=7]')
f.fill((0,4,1),(N-1,4,1),'air'); f.fill((0,5,0),(N-1,6,0),'air')
f.fill((0,4,2),(N-1,4,2),'piston[facing=north]'); f.fill((0,4,3),(N-1,4,3),'stone_bricks')
f.fill((0,5,1),(N-1,5,1),'observer[facing=down]'); f.fill((0,6,1),(N-1,6,1),'stone_bricks')
f.fill((0,5,2),(N-1,5,3),'stone_bricks'); f.fill((0,6,2),(N-1,6,2),'redstone_wire')
f.fill((-1,7,-1),(N,7,3),'glass')
for x in range(0,N,3): f.set((x,7,0),'glowstone')
for x in range(N):
    f.summon('hopper_minecart',(x,2,0)); f.summon('hopper_minecart',(x,2,1))
f.label((-2,3,1),'MELONES Y CALABAZAS\\ncofre aqui abajo')
f.msg('Granja de melones y calabazas lista. Cada vez que crece una, el piston la rompe y cae al cofre del lado oeste. Los melones se comen y al granjero le puedes vender ambos por esmeraldas.')
f.save('comida')

# ================= HORNOS AUTOMATICOS =================
N=8
f=Fn('Construyendo HORNOS automaticos...')
f.fill((-3,0,-3),(N+1,6,3),'air'); f.fill((-3,0,-3),(N+1,0,3),'stone_bricks')
f.fill((-1,1,-2),(N,4,-1),'stone_bricks'); f.fill((N,1,-2),(N,5,0),'stone_bricks')
f.fill((0,1,0),(N-1,1,0),'hopper[facing=west]'); f.set((-1,1,0),'barrel[facing=west]')
f.fill((0,2,0),(N-1,2,0),'furnace[facing=south]')
f.fill((0,3,0),(N-1,3,0),'hopper[facing=down]'); f.fill((-1,4,0),(N-1,4,0),'hopper[facing=east]'); f.set((-1,5,0),'barrel[facing=west]')
f.fill((0,2,-1),(N-1,2,-1),'hopper[facing=south]'); f.fill((-1,3,-1),(N-1,3,-1),'hopper[facing=east]'); f.set((-1,4,-1),'barrel[facing=west]')
f.set((-1,2,0),'stone_bricks'); f.set((-1,3,0),'stone_bricks'); f.set((-1,2,-1),'stone_bricks'); f.set((-1,1,-1),'stone_bricks')
f.label((-2,6,0),'HORNOS: arriba = lo que quieres cocinar\\nmedio = carbon   abajo = lo cocinado')
f.msg('Hornos listos (8). Desde el lado oeste: cofre de ARRIBA = minerales o comida cruda, cofre del MEDIO = carbon, cofre de ABAJO = todo cocinado.')
f.save('hornos')

# ================= GRANJA DE MOBS (polvora, huesos, flechas, hilo) =================
H=28
f=Fn('Construyendo granja de MOBS en el cielo (polvora, huesos, flechas)...')
f.fill((-2,0,-2),(19,H+5,19),'air'); f.fill((-2,0,-2),(19,0,19),'stone_bricks')
f.fill((-1,H-3,-1),(18,H+3,18),'stone_bricks','hollow')
f.fill((0,H,0),(17,H,17),'stone_bricks')                   # piso donde aparecen (2 de alto: sin endermen)
for z in (2,5,8,11,14): f.fill((0,H,z),(17,H,z),'spruce_trapdoor[open=true,facing=north,half=bottom]')
for a,b in [((0,H-2,0),(0,H-2,17)),((17,H-2,0),(17,H-2,17)),((0,H-2,0),(17,H-2,0)),((0,H-2,17),(17,H-2,17))]: f.fill(a,b,'water')
f.fill((7,1,7),(10,H-4,10),'stone_bricks'); f.fill((8,2,8),(9,H-3,9),'air')
f.fill((8,1,8),(9,1,8),'hopper[facing=south]'); f.fill((8,1,9),(9,1,9),'hopper[facing=south]')
f.fill((8,1,10),(9,1,10),'barrel[facing=south]')
for x in range(0,18,4):
    for z in range(0,18,4): f.set((x,H+4,z),'torch')
for p in [(5,1,12),(12,1,12),(5,1,5),(12,1,5),(3,1,9),(14,1,9)]: f.set(p,'torch')
f.label((8,3,12),'GRANJA DE MOBS\\nquedate aqui cerca (AFK)')
f.msg('Granja de mobs lista. Los mobs aparecen arriba en la oscuridad, caen 24 bloques y mueren solos. Quedate cerca de los cofres (lado sur): ahi llega la polvora, huesos, flechas e hilo.')
f.save('mobs')

# ================= TODAS / NUEVAS =================
def fila(nombre, partes, largo, msg):
    L=[f'tellraw @s {{"text":"{msg}","color":"yellow"}}',
       f'fill {C(-4,1,-7)} {C(largo,4,-5)} air', f'fill {C(-4,0,-7)} {C(largo,0,-5)} stone_bricks']
    for x in range(-4,largo+1,8): L.append(f'setblock {C(x,1,-7)} lantern')
    for off,fn in partes: L.append(f'execute positioned ~{off} ~ ~ run function granjas:_{fn}' if off else f'function granjas:_{fn}')
    L.append('tellraw @s {"text":"Listo: sigue el camino de piedra con faroles hacia el ESTE.","color":"green"}')
    open(f'{F}/_{nombre}.mcfunction','w').write('\n'.join(L)+'\n')
    open(f'{F}/{nombre}.mcfunction','w').write(f'execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_{nombre}\n')
fila('todas',[(0,'hierro'),(30,'experiencia'),(52,'aldeanos'),(76,'comercio'),(116,'cana'),(136,'comida'),(156,'hornos'),(172,'mobs')],192,
     'Construyendo las 8 granjas en fila hacia el ESTE (unos 200 bloques)...')
fila('nuevas',[(0,'cana'),(20,'comida'),(40,'hornos'),(56,'mobs')],76,'Construyendo las 4 granjas nuevas en fila hacia el ESTE...')

H=['tellraw @a {"text":"[Granjas v3] Parate en un terreno PLANO y despejado (borra lo que haya) y usa:","color":"gold"}',
 'tellraw @a {"text":"/function granjas:nuevas  (cana, comida, hornos y mobs juntas)\\n/function granjas:todas   (las 8 juntas)\\n/function granjas:hierro | experiencia | aldeanos | comercio\\n/function granjas:cana | comida | hornos | mobs","color":"aqua"}']
open(f'{F}/ayuda.mcfunction','w').write('\n'.join(H)+'\n')
json.dump({"pack":{"description":"Granjas v3: 8 granjas automaticas","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)

z=os.path.join(GEN,'build','granjas_datapack.zip')
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
import re
for fn in os.listdir(F):
    for line in open(f'{F}/{fn}'):
        m=re.match(r'fill ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*) ~(\S*)',line)
        if m:
            v=[int(t) if t else 0 for t in m.groups()]
            vol=(abs(v[3]-v[0])+1)*(abs(v[4]-v[1])+1)*(abs(v[5]-v[2])+1)
            if vol>32768: print('DEMASIADO GRANDE',fn,vol)
print(sorted(os.listdir(F)))
