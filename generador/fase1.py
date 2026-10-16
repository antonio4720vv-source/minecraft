# FASE 1: torre de 5 granjas de hierro + edificio de 4 criaderos con sala de comercio.
# Uso: python fase1.py  -> regenera todo el datapack (gen6 + fase 1) en build/granjas_datapack.zip
# En el juego: /function granjas:fase1   (construye al ESTE y SUR de donde estas parado)
import os; GEN=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(GEN,'gen6.py'),encoding='utf-8').read())

M='@e[type=minecraft:marker,tag=granjas_f1,limit=1]'
IX,IZ=8,4      # origen de la torre de hierro (relativo al marker)
VX,VZ=34,4     # origen del edificio de aldeanos

class G:
    """Constructor con origen desplazado. Coordenadas locales: y=0 es el suelo."""
    def __init__(s,ox,oz): s.ox,s.oz,s.L=ox,oz,[]
    def p(s,x,y,z): return C(x+s.ox,y,z+s.oz)
    def fill(s,a,b,blk,mode=''): s.L.append(f'fill {s.p(*a)} {s.p(*b)} {blk}{(" "+mode) if mode else ""}')
    def set(s,a,blk): s.L.append(f'setblock {s.p(*a)} {blk}')
    def summon(s,e,a,nbt=''): s.L.append(f'summon minecraft:{e} {s.p(*a)} {nbt}'.rstrip())
    def label(s,a,t,color='gold'):
        s.L.append(f'summon minecraft:text_display {s.p(*a)} {{billboard:"center",text:{{text:"{t}",color:"{color}",bold:1b}},background:1073741824}}')
    def walls(s,x0,x1,y0,y1,z0,z1,blk):          # 4 paredes, sin piso ni techo
        s.fill((x0,y0,z0),(x1,y1,z0),blk); s.fill((x0,y0,z1),(x1,y1,z1),blk)
        s.fill((x0,y0,z0),(x0,y1,z1),blk); s.fill((x1,y0,z0),(x1,y1,z1),blk)

ZOMBI='{PersistenceRequired:1b,CustomName:"Asustador",equipment:{head:{id:"minecraft:carved_pumpkin",count:1}},drop_chances:{head:0.0f}}'

# =====================================================================
#  TORRE DE HIERRO: 5 pisos (base de cada piso en y = 4,14,24,34,44)
#  Cada piso: plataforma 18x18 con agua en los bordes oeste/este que empuja a un
#  canal central (x=8..9); el canal lleva al foso del medio (8..9, 8..9).
#  El foso atraviesa TODOS los pisos: los golems caen hasta las fogatas de abajo
#  y el hierro baja por tolvas a 4 barriles en el cuarto de la planta baja.
#  Capsula de 3 aldeanos al este (lejos del foso) con el zombi a menos de 8 bloques
#  y una rendija a la altura de los ojos (en Java el vidrio tapa la vista).
# =====================================================================
FLOORS=[4+10*k for k in range(5)]; TOPI=54
def hierro_base():
    g=G(IX,IZ)
    g.fill((-1,0,-1),(18,3,18),'stone_bricks')
    g.fill((5,1,5),(12,3,12),'air'); g.fill((0,1,8),(4,2,9),'air')          # cuarto de barriles + pasillo
    g.fill((8,3,8),(9,2,9),'hopper[facing=down]'); g.fill((8,1,8),(9,1,9),'barrel[facing=up]')
    for p in [(6,0,6),(11,0,11),(6,0,11),(11,0,6),(2,0,8)]: g.set(p,'glowstone')
    g.set((-1,1,8),'iron_door[half=lower,facing=east,hinge=left]'); g.set((-1,2,8),'iron_door[half=upper,facing=east,hinge=left]')
    g.set((-2,2,9),'stone_button[face=wall,facing=west]'); g.set((0,2,9),'stone_button[face=wall,facing=east]')
    for i,(x,z) in enumerate([(8,8),(9,8),(8,9),(9,9),(8,8)]):
        g.summon('marker',(x,1,z),'{Tags:["go_hierro","f1"]}')               # 5 = una por granja (respaldo)
    g.label((-3,4,8),'TORRE DE HIERRO\\n5 granjas - barriles adentro')
    return g.L
def hierro_piso(k):
    b=FLOORS[k]; g=G(IX,IZ)
    g.fill((-1,b,-1),(18,b,18),'stone_bricks')
    if k==0: g.fill((8,b,8),(9,b,9),'soul_campfire[lit=true]')
    else:    g.fill((8,b,8),(9,b,9),'air')                                    # el foso sigue hacia abajo
    g.fill((0,b+1,0),(17,b+9,17),'air')
    g.walls(-1,18,b+1,b+1,-1,18,'stone_bricks'); g.walls(-1,18,b+2,b+9,-1,18,'glass')
    for x in range(-1,19,6):
        for z in (-1,18): g.fill((x,b+1,z),(x,b+9,z),'chiseled_stone_bricks')
    g.fill((0,b+1,0),(17,b+1,17),'smooth_stone'); g.fill((8,b+1,0),(9,b+1,17),'air')   # plataforma + canal
    g.fill((0,b+2,0),(0,b+2,17),'water'); g.fill((17,b+2,0),(17,b+2,17),'water')
    g.fill((8,b+1,0),(9,b+1,0),'water'); g.fill((8,b+1,17),(9,b+1,17),'water')
    for x in (2,5,13,16):
        for z in (2,6,11,15): g.set((x,b+4,z),'light[level=15]')               # sin monstruos adentro
    # capsula de aldeanos
    g.fill((11,b+6,5),(16,b+6,14),'smooth_stone')
    g.fill((11,b+7,5),(16,b+8,14),'glass'); g.fill((12,b+7,6),(15,b+8,11),'air'); g.fill((12,b+7,13),(15,b+8,13),'air')
    g.fill((11,b+9,5),(16,b+9,14),'glass')
    g.fill((12,b+8,12),(15,b+8,12),'air')                                     # rendija: ven al zombi, nadie pasa
    for x in (12,13,14): g.set((x,b+7,10),'red_bed[facing=south,part=foot]'); g.set((x,b+7,11),'red_bed[facing=south,part=head]')
    for x in (12,14,15): g.summon('villager',(x,b+7,7),'{PersistenceRequired:1b,CustomName:"Trabajador del hierro"}')
    g.summon('zombie',(13,b+7,13),ZOMBI)
    return g.L
def hierro_techo():
    g=G(IX,IZ)
    g.fill((-1,TOPI,-1),(18,TOPI,18),'glass')            # vidrio: ahi no pueden aparecer golems
    for x,z in [(-1,-1),(18,-1),(-1,18),(18,18)]: g.set((x,TOPI+1,z),'lantern')
    # torre de escalera (lado oeste)
    g.fill((-5,0,10),(-2,TOPI+3,14),'stone_bricks'); g.fill((-4,1,12),(-3,TOPI+2,12),'air')
    g.fill((-3,1,12),(-3,TOPI,12),'ladder[facing=west]')
    g.fill((-5,1,12),(-5,2,12),'air')                                          # entrada (lado oeste)
    g.fill((-2,TOPI+1,12),(-2,TOPI+2,12),'air')                                # salida a la azotea
    for b in FLOORS: g.fill((-2,b+3,12),(-2,b+4,12),'glass')                   # ventana a cada piso
    for y in range(4,TOPI,6): g.set((-4,y,12),'light[level=15]')
    g.label((-6,4,12),'ESCALERA\\na la azotea','aqua')
    return g.L

# =====================================================================
#  EDIFICIO DE ALDEANOS: 4 criaderos (base y = 0,4,8,12) + sala de comercio (y=16)
#  Criadero: 4 adultos con pan y 22 camas; los bebes pasan por un hueco de 1 bloque
#  al corral del este. Escalera de mano al este (x=19) une todos los pisos.
# =====================================================================
VF=[0,4,8,12]; HB=16; TOPV=HB+5; HW=31
def criadero(k):
    b=VF[k]; g=G(VX,VZ)
    g.fill((-1,b,-1),(17,b,11),'stone_bricks')
    g.fill((-1,b+1,-1),(17,b+3,11),'air')
    g.walls(-1,11,b+1,b+3,-1,11,'glass')
    for x,z in [(-1,-1),(11,-1),(-1,11),(11,11)]: g.fill((x,b+1,z),(x,b+3,z),'stripped_spruce_log')
    for x in range(0,11):
        g.set((x,b+1,0),'white_bed[facing=south,part=foot]'); g.set((x,b+1,1),'white_bed[facing=south,part=head]')
        g.set((x,b+1,10),'white_bed[facing=north,part=foot]'); g.set((x,b+1,9),'white_bed[facing=north,part=head]')
    g.set((11,b+1,5),'air')                                                    # solo pasan los bebes
    g.walls(11,17,b+1,b+3,2,8,'glass'); g.set((11,b+1,5),'air'); g.set((11,b+2,5),'glass')
    g.set((17,b+1,5),'iron_door[half=lower,facing=west,hinge=left]'); g.set((17,b+2,5),'iron_door[half=upper,facing=west,hinge=left]')
    g.set((16,b+2,6),'stone_button[face=wall,facing=west]')
    for p in [(2,b+3,5),(8,b+3,5),(5,b+3,3),(5,b+3,7),(14,b+3,5)]: g.set(p,'light[level=15]')
    inv='['+','.join(['{id:"minecraft:bread",count:64}']*8)+']'
    for i,(x,z) in enumerate([(3,4),(5,4),(3,6),(5,6)]):
        g.summon('villager',(x,b+1,z),'{PersistenceRequired:1b,CustomName:"Padre '+str(k*4+i+1)+'",Inventory:'+inv+'}')
    g.summon('marker',(14,b+1,5),'{Tags:["go_bebes","f1"]}')
    # pasillo hacia la escalera
    g.fill((18,b+1,4),(18,b+2,6),'air'); g.set((18,b+2,6),'stone_button[face=wall,facing=east]')
    return g.L
def escalera_v():
    g=G(VX,VZ)
    g.fill((18,0,3),(20,HB,7),'stone_bricks')
    g.fill((19,1,5),(19,HB+1,5),'ladder[facing=west]'); g.set((20,HB+1,5),'stone_bricks')
    g.fill((19,1,3),(19,2,4),'air')                                           # entrada desde la calle (lado norte)
    g.set((19,0,2),'stone_bricks'); g.set((18,1,2),'lantern'); g.set((20,1,2),'lantern')
    g.label((19,4,1),'CRIADEROS (4 pisos)\\ny SALA DE COMERCIO arriba\\nentra y sube por la escalera')
    return g.L
PROF=[('armorer','blast_furnace','Armero'),('butcher','smoker','Carnicero'),('cartographer','cartography_table','Cartografo'),
('cleric','brewing_stand','Clerigo'),('farmer','composter','Granjero'),('fisherman','barrel','Pescador'),('fletcher','fletching_table','Flechero'),
('leatherworker','cauldron','Peletero'),('librarian','lectern','Bibliotecario 1'),('librarian','lectern','Bibliotecario 2'),('librarian','lectern','Bibliotecario 3'),
('mason','stonecutter','Albanil'),('shepherd','loom','Pastor'),('toolsmith','smithing_table','Herrero de herramientas'),('weaponsmith','grindstone','Herrero de armas')]
def comercio():
    g=G(VX,VZ); b=HB
    g.fill((-1,b,-1),(HW,b,12),'stone_bricks'); g.set((19,b,5),'ladder[facing=west]')
    g.fill((-1,b+1,-1),(HW,b+4,12),'air')
    g.walls(-1,HW,b+1,b+4,-1,12,'stone_bricks')
    for x in range(1,HW,4): g.fill((x,b+2,12),(x+1,b+3,12),'glass')          # ventanas al sur
    for x in range(-1,HW+1,6):
        for z in (-1,12): g.fill((x,b+1,z),(x,b+4,z),'stripped_dark_oak_log')
    g.fill((-1,b+5,-1),(HW,b+5,12),'dark_oak_planks')
    g.fill((0,b+1,0),(30,b+3,2),'stone_bricks')                               # mostrador
    for i,(p,ws,name) in enumerate(PROF):
        X=1+2*i
        g.set((X,b+1,0),ws); g.fill((X,b+1,1),(X,b+2,1),'air'); g.set((X,b+2,2),'air'); g.set((X,b+3,2),'glowstone')
        g.summon('villager',(X,b+1,1),'{PersistenceRequired:1b,Xp:1,CustomName:"'+name+'",CustomNameVisible:1b,VillagerData:{profession:"minecraft:'+p+'",level:1,type:"minecraft:plains"}}')
    g.fill((0,b,3),(30,b,11),'polished_andesite'); g.fill((2,b+1,6),(28,b+1,8),'red_carpet')
    for x in range(3,HW,6):
        for z in (5,9): g.set((x,b+4,z),'lantern[hanging=true]')
    g.set((20,b+1,5),'stone_bricks'); g.set((19,b+1,5),'ladder[facing=west]')            # sale la escalera
    g.label((15,b+4,7),'SALA DE COMERCIO\\n15 aldeanos (3 bibliotecarios)','aqua')
    return g.L

# =====================================================================
#  ETAPAS (con schedule para no trabar el servidor)
# =====================================================================
AX0,AX1,AZ0,AZ1=-2,70,-4,26
def limpiar(ya,yb):
    return [f'fill {C(xa,ya,AZ0)} {C(xb,yb,AZ1)} air' for xa,xb in chunks(AX0,AX1,36)]
def etapa(n,body,nxt=None,msg=None,delay='3s'):
    L=([f'tellraw @a {{"text":"[Fase 1] {msg}","color":"yellow"}}'] if msg else [])+body
    W(f'_f1_{n}b',L)
    W(f'_f1_{n}',[f'execute at {M} run function granjas:_f1_{n}b']+([f'schedule function granjas:_f1_{nxt} {delay} replace'] if nxt else []))
W('fase1',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_f1_nueva'])
W('_f1_nueva',['kill @e[type=minecraft:marker,tag=granjas_f1]','summon minecraft:marker ~ ~ ~ {Tags:["granjas_f1"]}','function granjas:_f1_0'])
W('rehacer_fase1',[f'execute unless entity {M} run tellraw @s {{"text":"No encuentro la Fase 1. Usa /function granjas:fase1 donde la quieras.","color":"red"}}',
                   f'execute at {M} run function granjas:_f1_0'])
W('_f1_0',[f'execute at {M} run forceload add ~{AX0} ~{AZ0} ~{AX1} ~{AZ1}',
 'tellraw @a {"text":"[Fase 1] Preparando terreno de 72 x 30 bloques al ESTE y SUR. Tarda unos 25 segundos. No te alejes.","color":"gold"}',
 'schedule function granjas:_f1_1 5s replace'])
etapa(1,[f'execute positioned {C(AX0,-6,AZ0)} run kill @e[type=!minecraft:player,tag=!granjas_f1,tag=!granjas_mega,tag=!granjas_hub,dx={AX1-AX0},dy=80,dz={AZ1-AZ0}]']
      +limpiar(1,15)+limpiar(16,30),'2','Limpiando (1/2)...')
etapa(2,limpiar(31,45)+limpiar(46,62)+[f'fill {C(xa,0,AZ0)} {C(xb,0,AZ1)} grass_block' for xa,xb in chunks(AX0,AX1,36)]
      +[f'fill {C(xa,-3,AZ0)} {C(xb,-1,AZ1)} dirt' for xa,xb in chunks(AX0,AX1,36)]
      +[f'fill {C(AX0,0,0)} {C(AX1,0,2)} stone_bricks',f'fill {C(0,0,AZ0)} {C(2,0,AZ1)} stone_bricks']
      +[f'setblock {C(x,1,0)} lantern' for x in range(AX0,AX1,8)]
      +['kill @e[type=minecraft:item,distance=..120]'],'3','Limpiando (2/2)...')
etapa(3,hierro_base()+hierro_piso(0)+hierro_piso(1),'4','Torre de hierro: planta baja y pisos 1-2...')
etapa(4,hierro_piso(2)+hierro_piso(3)+hierro_piso(4)+hierro_techo(),'5','Torre de hierro: pisos 3-5 y azotea...')
etapa(5,escalera_v()+criadero(0)+criadero(1)+criadero(2)+criadero(3),'6','Edificio de aldeanos: 4 criaderos...')
etapa(6,comercio()+['function granjas:respaldo_on',
 'tellraw @a {"text":"[Fase 1] LISTA! Torre de hierro (5 granjas, barriles en la planta baja, puerta oeste) y edificio de aldeanos (4 criaderos + sala de comercio arriba). Los golems empiezan cuando los aldeanos duermen la primera noche.","color":"green"}'],
      None,'Sala de comercio...')

W('lista',['tellraw @s {"text":"--- FASE 1 ---\\n/function granjas:fase1   (torre de 5 granjas de hierro + edificio de 4 criaderos y comercio)\\n/function granjas:rehacer_fase1\\n--- TODO JUNTO (version anterior) ---\\n/function granjas:megabase\\n/function granjas:rehacer_megabase\\n--- SUELTAS ---\\nedificio_granjas, mobs, caballeriza, arbol, fuente, cofres, animales, casa_grande, montana, portal_end, torre_elitros, casa, cana, sandia\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, hierro_vision","color":"aqua"}'])
json.dump({"pack":{"description":"Granjas v8: fase 1 (torre de hierro + aldeanos)","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)

z=os.path.join(GEN,'build','granjas_datapack.zip')
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
print('FASE 1:', 'OK' if not bad else 'HAY ERRORES', '->', z)
