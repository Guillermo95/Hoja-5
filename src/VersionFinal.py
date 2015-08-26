#Universidad de Valle de Guatemala
#Algoritmos y Estructuras de Datos, Sección 30
#Edwin Fernando Coronado Roche, 14148
#Guillermo Javier de León Archila, 14022

"""  Programa para simular el funcionamiento de un cpu
     atendiendo varios procesos e Instrucciones de entrada
     y salida.                                         """


import simpy
import random
import math


seed = 21
intervalo = 10.0

def cpu(env, name, cap, ram, tiempollegada, tiempo_atencion, instrucciones):
    global totaltime
    # simulacion del tiempo de llegada del procesos
    yield env.timeout(tiempollegada)
    contador = instrucciones
    print('%s arriving at %d' % (name, env.now))
    llegada = env.now
    #se verifica la existencia de instrucciones a ejecutar
    while contador>0:
        #se crea la cantidad de ram que utilizara el procesos
        num = random.randint(1,10)
        #se verifica la disponibilidad de RAM
        if ram.level>num:
            #si hay RAM disponible se hace cola para que el cpu atienda el proceso
            with cap.request() as req:
                yield req
                #se solicita la RAM para ejecucion
                ram.get(num)
                print('%s esta siendo atendido por cpu en %s' % (name, env.now))
                #pasa el tiempo de atencion
                yield env.timeout(tiempo_atencion)
                if contador>2:
                    #se ejecutan 3 instruciones las cuales se restan de las instrucciones a realizar
                    contador = contador - 3
                    print name, " atendido, quedan ", contador, " instrucciones"
                else:
                    #si hay menos de tres instrucciones se interrumpe y finaliza el proceso
                    contador = 0
                #despues de ejecutar se compite con dispositivos de entrada y salida
                print('%s dejando cpu en %s' % (name, env.now))
                io = random.randint(1,2)
                #si hay un dispositivo este es atendido en 2 unidades de tiempo
                if io == 1:
                    print "atendiendo dispositivos I/O"
                    print "Tiempo de espera 2"
                    yield env.timeout(2)    
        else:
            #al no haber ram se libera la memoria para seguir con la ejecucion
            print"RAM insuficiente, liberando ram. tiempo de espera 1"
            recarga = 100 - ram.level
            ram.put(recarga)
            env.timeout(tiempo_atencion)
    tiempoTotal = env.now
    procesos.append(env.now - llegada) 
    totaltime = totaltime + tiempoTotal
    print ('%s finalizado en %s' % (name,tiempoTotal))

global procesos
procesos = []
env = simpy.Environment()  #crear ambiente de simulacion
cap = simpy.Resource(env, capacity=1) #el cpu puede atender solo un proceso a la vez
ram = simpy.Container(env, init=100, capacity=100) #la memoria RAM tiene 100 unidades de capacidad
random.seed(42)
totaltime = 0.0
nprocesos = 100 #cantidad de procesos a ejecutar
tot = 0.0
                                      

# se crean nprocesos
for i in range(nprocesos):
    instrucciones = random.randint(1,10)
    t = random.expovariate(1.0 / intervalo)
    env.process(cpu(env, 'proceso %d' % i, cap, ram, t, 1, instrucciones))

# correr la simulacion
env.run()
#se calcula promedio y desviacion estandar
promedio = totaltime / nprocesos
for i in range(len(procesos)-1):
    tot = tot + abs(procesos[i]-promedio)
desvest = math.sqrt(tot/nprocesos)

print "el tiempo total para los ", nprocesos, " procesos fue ", totaltime
print "el promedio fue: ", promedio
print "la desviacion estandar es ", desvest
