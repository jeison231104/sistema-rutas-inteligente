import heapq

# -----------------------------
# BASE DE CONOCIMIENTO (REGLAS)
# -----------------------------
reglas = {"evitar_estaciones": ["E"], "criterio": "tiempo"}  # estaciones restringidas

# -----------------------------
# GRAFO DEL SISTEMA DE TRANSPORTE
# -----------------------------
grafo = {
    "A": {"B": 2, "C": 4},
    "B": {"A": 2, "D": 7, "E": 3},
    "C": {"A": 4, "D": 1},
    "D": {"B": 7, "C": 1, "F": 5},
    "E": {"B": 3, "F": 8},
    "F": {"D": 5, "E": 8},
}

# -----------------------------
# HEURÍSTICA (estimación al destino)
# -----------------------------
heuristica = {"A": 7, "B": 6, "C": 2, "D": 1, "E": 5, "F": 0}


# -----------------------------
# FUNCIÓN PARA LIMPIAR ENTRADA
# -----------------------------
def limpiar_entrada(texto):
    texto = texto.strip().upper()
    texto = texto.replace("ESTACION ", "")
    return texto


# -----------------------------
# FUNCIÓN A* (A ESTRELLA)
# -----------------------------
def a_estrella(inicio, fin):
    abiertos = []
    heapq.heappush(abiertos, (0, inicio))

    costo = {inicio: 0}
    camino = {inicio: None}

    while abiertos:
        _, actual = heapq.heappop(abiertos)

        if actual == fin:
            break

        for vecino, peso in grafo[actual].items():

            # Aplicar regla: evitar estaciones restringidas
            if vecino in reglas["evitar_estaciones"]:
                continue

            nuevo_costo = costo[actual] + peso

            if vecino not in costo or nuevo_costo < costo[vecino]:
                costo[vecino] = nuevo_costo
                prioridad = nuevo_costo + heuristica[vecino]
                heapq.heappush(abiertos, (prioridad, vecino))
                camino[vecino] = actual

    # Reconstruir ruta
    ruta = []
    nodo = fin

    if nodo not in camino:
        return None, float("inf")

    while nodo:
        ruta.append(nodo)
        nodo = camino[nodo]

    ruta.reverse()
    return ruta, costo[fin]


# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
def main():
    print("\n=== SISTEMA INTELIGENTE DE RUTAS ===\n")

    print("Estaciones disponibles:")
    for estacion in grafo.keys():
        print(f"- Estacion {estacion}")

    inicio = limpiar_entrada(input("\nIngrese la estación de inicio: "))
    fin = limpiar_entrada(input("Ingrese la estación destino: "))

    # Validación
    if inicio not in grafo or fin not in grafo:
        print("\n❌ Error: estación inválida")
        return

    if inicio == fin:
        print("\n⚠️ El punto de inicio y destino son iguales")
        return

    ruta, costo_total = a_estrella(inicio, fin)

    if ruta is None:
        print("\n❌ No se encontró una ruta disponible")
    else:
        print("\n✅ Ruta encontrada:", " → ".join([f"Estacion {r}" for r in ruta]))
        print("📊 Costo total:", costo_total)


# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == "__main__":
    main()
