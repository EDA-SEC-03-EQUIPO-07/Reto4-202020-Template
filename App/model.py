"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        citibike = {
            'salida': None,
            'llegada': None,
            'graph': None
        }

        citibike['salida'] = {}
        citibike['llegada'] = {}
        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStopIds)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo
def addTrip(citibike, trip):
    origin = trip["start station id"]
    destination = trip["end station id"]
    duration = int(trip["tripduration"])
    if origin != destination:
        año = int(trip["birth year"])
        latitudS = float(trip["start station latitude"])
        longitudS = float(trip["start station longitude"])
        latitudE = float(trip["end station latitude"])
        longitudE = float(trip["end station longitude"])
        añadirEstacionSalida(citibike, origin, año, latitudS, longitudS)
        añadirEstacionLlegada(citibike, destination, año, latitudE, longitudE)
        addStation(citibike, origin)
        addStation(citibike, destination)
        addConnection(citibike, origin, destination, duration)


def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike["graph"], origin, destination)
    if edge is None:
        gr.addEdge(citibike["graph"], origin, destination, int(duration), 1)
    else:
        peso = edge['weight']
        edge['weight'] = (peso+int(duration))/2
        edge['count'] += 1
        #gr.addEdge(citibike["graph"], origin,destination, promedio, (edge['count'] + 1))
    return citibike


def addStation(citibike, stationid):
    if not gr.containsVertex(citibike["graph"], stationid):
        gr.insertVertex(citibike["graph"], stationid)
    return citibike


def añadirEstacionLlegada(citibike, idestacion, año, latitud, longitud):
    dicc = citibike['llegada']
    if not (idestacion in dicc):
        dicc[idestacion] = {'0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0,
                            '51-60': 0, '60+': 0, 'total': 0, 'latitud': latitud, 'longitud': longitud}

    newDicc = dicc[idestacion]
    newDicc[darRangoEdad(año)] += 1
    newDicc['total'] += 1


def añadirEstacionSalida(citibike, idestacion, año, latitud, longitud):
    dicc = citibike['salida']
    if not (idestacion in dicc):
        dicc[idestacion] = {'0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0,
                            '51-60': 0, '60+': 0, 'total': 0, 'latitud': latitud, 'longitud': longitud}

    newDicc = dicc[idestacion]
    newDicc[darRangoEdad(año)] += 1
    newDicc['total'] += 1


def darRangoEdad(año):
    rango = ''
    edad = 2020-año
    if edad >= 0 and edad <= 10:
        rango = '0-10'
    elif edad >= 11 and edad <= 20:
        rango = '11-20'
    elif edad >= 21 and edad <= 30:
        rango = '21-30'
    elif edad >= 31 and edad <= 40:
        rango = '31-40'
    elif edad >= 41 and edad <= 50:
        rango = '41-50'
    elif edad >= 51 and edad <= 60:
        rango = '51-60'
    else:
        rango = '60+'

    return rango
# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(citibike, id1, id2):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    citibike['components'] = numSCC_2(citibike['graph'])
    scc = numSCC(citibike['graph'])
    pertenecer = sameCC(citibike['components'], id1, id2)
    be = ""
    if pertenecer == False:
        be = "No están en el mismo componente"
    else:
        be = "Si están en el mismo componente"
    return (be, scc)


def segunda_consulta(citibike, time1, time2, identificador):
    present = gr.containsVertex(citibike['graph'], identificador)
    if present == True:
        nombre_inicial = identificador
        dicc = {}
        lista = lt.newList(cmpfunction=compareroutes)
        tiempo_total = abs(int(time1)-int(time2))
        citibike['components'] = numSCC_2(citibike['graph'])
        number = numSCC(citibike['graph'])
        key = gr.adjacents(citibike['graph'], nombre_inicial)
        tiempo = 0
        ite = it.newIterator(key)
        while tiempo < tiempo_total and it.hasNext(ite):
            pro = it.next(ite)
            pertenecer = sameCC(citibike['components'], nombre_inicial, pro)
            if pertenecer == True:
                peso = gr.getEdge(citibike["graph"], nombre_inicial, pro)
                p = peso["weight"]
                res = abs(tiempo_total-(p+20))
                tiempo = res
                dicc["inicial"] = nombre_inicial
                dicc["final"] = pro
                dicc["tiempo"] = peso
                lt.addLast(lista, dicc)
                nombre_inicial = pro
                #nombre_final = pro
        answer = (number, lista)
    else:
        answer = "La estación no es válida, ingrese otra. "
    return answer


def tercera_consulta(citibike):
    print(citibike['llegada'])
    tree = om.newMap(omaptype='RBT', comparefunction=compareroutes)
    diccionario = {}
    list_vertext = gr.vertices(citibike["graph"])
    ite = it.newIterator(list_vertext)
    while it.hasNext(ite):
        vertex = it.next(ite)
        arrive = gr.adjacents(citibike["graph"], vertex)
        #if arrive['first'] is not None:

            # print(arrive)
            # if arrive > 0:
            #   om.put(tree, arrive, vertex)
    l = []
    number = om.size(tree)
    resta = abs(number-3)
    less = om.select(tree, resta)
    greater = om.maxKey(tree)
    ran = om.values(tree, less, greater)
    i = it.newIterator(ran)
    while it.hasNext(i):
        name = it.next(i)
        l.append(name)
    diccionario["llegadas"] = l

    tree_1 = om.newMap(omaptype='RBT', comparefunction=compareroutes)
    list_vertext_1 = gr.vertices(citibike["graph"])
    ite_1 = it.newIterator(list_vertext_1)
    while it.hasNext(ite_1):
        vertex_1 = it.next(ite_1)
        arrive_1 = gr.outdegree(citibike["graph"], vertex_1)
        if arrive_1 > 0:
            om.put(tree_1, arrive_1, vertex_1)
    l_1 = []
    number_1 = om.size(tree_1)
    resta_1 = abs(number_1-3)
    less_1 = om.select(tree_1, resta_1)
    greater_1 = om.maxKey(tree_1)
    ran_1 = om.values(tree_1, less_1, greater_1)
    iterar = it.newIterator(ran_1)
    while it.hasNext(iterar):
        name_1 = it.next(iterar)
        l_1.append(name_1)
    diccionario["salidas"] = l_1
    print(gr.adjacents(citibike['graph'], '72'))


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])
# ==============================
# Funciones Helper
# ==============================


def numSCC_2(graph):
    return scc.KosarajuSCC(graph)


def numSCC(graph):
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)


def sameCC(sc, station1, station2):
    return scc.stronglyConnected(sc, station1, station2)


# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
