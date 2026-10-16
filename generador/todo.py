# TODO EN UNO: /function granjas:todo construye las 4 fases separadas alrededor del jugador,
# una despues de otra (para no trabar el servidor), y al final tiende los ferrocarriles.
# Uso: python todo.py  -> genera el datapack final (gen6 + fases 1 a 4 + todo)
#
#   Fase 1 (hierro y aldeanos) ...... 120 al oeste, 100 al norte
#   Fase 2 (animales y cultivos) .... 130 al este, 110 al norte
#   Fase 3 (casas y portales) ....... 180 al oeste, 100 al sur
#   Fase 4 (estacion central, estatua, cofres, bunker) en el centro (donde estas parado)
import os; GEN=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(GEN,'fase4.py'),encoding='utf-8').read())

MT='@e[type=minecraft:marker,tag=granjas_todo,limit=1]'
POS_TODO={1:(-120,-100),2:(130,-110),3:(-180,100),4:(0,0)}
W('todo',['execute align xyz positioned ~0.5 ~ ~0.5 run function granjas:_todo_0'])
W('_todo_0',['kill @e[type=minecraft:marker,tag=granjas_todo]','summon minecraft:marker ~ ~ ~ {Tags:["granjas_todo"]}','forceload add ~ ~',
 'tellraw @a {"text":"[TODO] Se construye todo el megaproyecto en unos 4 minutos: fase 1, 2, 3 y al final la 4 con las vias. No te alejes ni apagues el servidor.","color":"gold"}',
 'function granjas:_todo_1',
 'schedule function granjas:_todo_2 35s replace','schedule function granjas:_todo_3 75s replace','schedule function granjas:_todo_4 125s replace'])
for n,(x,z) in POS_TODO.items():
    W(f'_todo_{n}',[f'execute at {MT} positioned ~{x} ~ ~{z} run forceload add ~ ~',
                    f'tellraw @a {{"text":"[TODO] Empezando la fase {n}...","color":"yellow"}}',
                    f'execute at {MT} positioned ~{x} ~ ~{z} run function granjas:fase{n}'])

W('lista',['tellraw @s {"text":"--- TODO DE UNA VEZ ---\\n/function granjas:todo   (las 4 fases + vias, unos 4 minutos)\\n--- FASES SUELTAS ---\\n/function granjas:fase1   (torre de hierro + criaderos y comercio)\\n/function granjas:fase2   (establo, invernadero, bambu, sandia y calabaza)\\n/function granjas:fase3   (montana con casa, casa del arbol, portales, caballeriza, torre de elitros)\\n/function granjas:fase4   (bunker, estatua, salon de cofres y ferrocarriles)\\n/function granjas:ferrocarriles   (vuelve a tender las vias)\\n/function granjas:rehacer_fase1 ... rehacer_fase4\\n--- OTROS ---\\nrespaldo_on, respaldo_off, quitar_carga, hierro_vision","color":"aqua"}'])
W('ayuda',['scoreboard objectives add granjas dummy','execute unless score #on granjas matches 0..1 run scoreboard players set #on granjas 0',
 'schedule function granjas:producir 30s replace','tellraw @a {"text":"[Granjas] Para construir todo: /function granjas:todo   |   lista de comandos: /function granjas:lista","color":"gold"}'])

z=os.path.join(GEN,'build','granjas_datapack.zip')
json.dump({"pack":{"description":"Megaproyecto completo: /function granjas:todo","min_format":88,"max_format":999}},open(f'{B}/pack.mcmeta','w'),indent=1)
if os.path.exists(z): os.remove(z)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as Z:
    for r,_,fs in os.walk(B):
        for n in fs: p=os.path.join(r,n); Z.write(p,os.path.relpath(p,B))
print('TODO: OK ->', z)
