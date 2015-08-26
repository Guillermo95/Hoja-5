import simpy
import random

def cpu(env, memory, cap, Protime, instructions, cantProcesos):
    #tiempo para que se inicie el proceso
    for i in range(cantProcesos):
        memoryuse = random(10)
        while instructions > 0:
            contador = instructions
            yield env.timeout(Protime)
            print("El proceso no.%d se inicializo en %d" % (i, env.now))
            if contador>2:
                if memory.level > memoryuse:
                    memory.get(memoryuse)
                    with cap.request() as req:
                        yield req
                        print("se esta atendiendo a proceso no.%d en %d" % (i, env.now))
                        env.timout(1)
                        contador = contador - 3
                        print("proceso no.%d atendido en %d: instrucciones restantes %d" % (i, env.now, contador))
                else:
                    recarga = 100 - memory.level
                    memory.put(recarga)
                    env.timeout(2)
                    print ("se ha liberado la memoria en %d, memoria disponible: %d" % (env.now, memory.level))
            else:
                print("proceso no.%d finalizado en %d" % (name, env.now))


env = simpy.Environment()
cap = simpy.Resource(env, capacity=1)
memory = simpy.Container(env, init=100, capacity=100)

env.process(cpu(env, memory, cap, 3, 9, 6))
env.run()
