from igraph import Graph
import matplotlib.pyplot as plt
import random

#Activar modo interactivo
plt.ion()
plt.figure(figsize=(6, 6)) #Crea el grafo

#FUNCION QUE DIBUJA EL GRAFO

def grafo_tiempo_real(grafo, infectados, paso):
    plt.clf()  #limpiar contenido de la figura existente

    layout = grafo.layout("circle")
    x = [p[0] for p in layout]
    y = [p[1] for p in layout]

    #Colores: infectados en rojo, sanos en verde
    colores = ["red" if v["name"] in infectados else "green" for v in grafo.vs]

    plt.scatter(x, y, c=colores, s=800)

    #Aristas
    for e in grafo.es:
        v1 = layout[e.tuple[0]]
        v2 = layout[e.tuple[1]]
        plt.plot([v1[0], v2[0]], [v1[1], v2[1]], 'k-', linewidth=1)

    #Etiquetas de nodos
    for i, label in enumerate(grafo.vs["name"]):
        plt.text(x[i], y[i], label, ha='center', va='center', color="white", fontsize=12)

    plt.title(f"Paso de tiempo t = {paso}")
    plt.axis('off')
    plt.pause(2)


#AQUI COMIENZA EL PROGRAMA PRINCIPAL

archivo = input("Ruta del archivo .edgelist: ")
grafo = Graph.Read_Ncol(archivo, directed=False)

print("Vértices del grafo:", grafo.vs["name"])
print()

inicio = input("Nodo inicial de contagio: ")
pasos = int(input("Número de pasos de tiempo: "))

infectados = {inicio}

#PASO 0 (VISUALIZACION)
print("\n========= Paso 0 =========")
print("Nodo inicial infectado:", infectados)

grafo_tiempo_real(grafo, infectados, 0)

#CONTAGIOS

for t in range(1, pasos + 1):

    print(f"\n========= Paso {t} =========")
    print("Infectados actuales:", infectados)

    nuevos = set()
    infectados_previos = infectados.copy()

    print("\nEvaluando contagios:")
    print("(Solo contagian los infectados del paso previo)", infectados_previos)

    for v in infectados_previos:
        indice = grafo.vs.find(name=v).index
        vecinos = [grafo.vs[n]["name"] for n in grafo.neighbors(indice)]

        for vec in vecinos:
            if vec not in infectados:
                prob = random.random()
                print(f"\n - {vec} tiene a {v} como vecino contagiado")
                print(f"   Probabilidad generada: {prob:.2f}")

                if prob >= 0.5:
                    print("   → Se contagia ")
                    nuevos.add(vec)
                else:
                    print("   → NO se contagia ")

    infectados.update(nuevos)

    if len(nuevos) == 0:
        print("\nNuevos contagiados en este paso: (ninguno)")
    else:
        print("\nNuevos contagiados en este paso:", nuevos)

    print("Infectados totales ahora:", infectados)

    grafo_tiempo_real(grafo, infectados, t)

    # Si todos se contagian
    if len(infectados) == len(grafo.vs):
        print("\n ¡Todos los nodos están contagiados!")
        break

print("\nSimulación terminada.")
plt.ioff()
plt.show()
