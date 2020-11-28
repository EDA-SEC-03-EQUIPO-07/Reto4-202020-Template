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
from DISClib.Algorithms.Graphs import dfs as d
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.ADT import stack as st
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
        citibike['salida'] = m.newMap(numelements=200,
                                     maptype='CHAINING',
                                     comparefunction=compareStopIds)
        citibike['llegada'] = m.newMap(numelements=500,
                                     maptype='CHAINING',
                                     comparefunction=compareStopIds)
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
    return citibike


def addStation(citibike, stationid):
    if not gr.containsVertex(citibike["graph"], stationid):
        gr.insertVertex(citibike["graph"], stationid)
    return citibike


def añadirEstacionLlegada(citibike, idestacion, año, latitud, longitud):
    mapa = citibike['llegada']
    if not (m.contains(mapa, idestacion)):
        dicc = {'0-10':0,'11-20':0,'21-30':0,'31-40':0,'41-50':0,'51-60':0,'60+':0,'total':0,'latitud':latitud,'longitud':longitud}
    else:
        dicc = me.getValue(m.get(mapa, idestacion))

    newDicc = dicc
    newDicc[darRangoEdad(año)]+=1
    newDicc['total']+=1

    m.put(mapa, idestacion, newDicc)

def añadirEstacionSalida(citibike, idestacion, año, latitud, longitud):
    mapa = citibike['salida']
    if not (m.contains(mapa, idestacion)):
        dicc = {'0-10':0,'11-20':0,'21-30':0,'31-40':0,'41-50':0,'51-60':0,'60+':0,'total':0,'latitud':latitud,'longitud':longitud}
    else:
        dicc = me.getValue(m.get(mapa, idestacion))

    newDicc = dicc
    newDicc[darRangoEdad(año)]+=1
    newDicc['total']+=1

    m.put(mapa, idestacion, newDicc)


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
    scc = 0
    present = gr.containsVertex(citibike['graph'], id1)
    present_1 = gr.containsVertex(citibike['graph'], id2)
    if (present == True) and (present_1 == True):
        citibike['components'] = numSCC_2(citibike['graph'])
        scc = numSCC(citibike['graph'])
        pertenecer = sameCC(citibike['components'], id1, id2)
        be = ""
        if pertenecer == False:
            be = "No están en el mismo componente. "
        else:
            be = "Si están en el mismo componente. "
    else:
        be = "Una o dos estaciones son no válidas. "
    return (be, scc)


def segunda_consulta(citibike, time1, time2, identificador):
    present = gr.containsVertex(citibike['graph'], identificador)
    if present == True:
        segundos = (20*60)
        diccionario = {}
        dicc = {}
        list_vertex = lt.newList(cmpfunction=compareroutes)
        citibike['components'] = numSCC_2(citibike['graph'])
        key = gr.adjacents(citibike['graph'], identificador)
        ite = it.newIterator(key)
        while it.hasNext(ite):
            pro = it.next(ite)
            pertenecer = sameCC(citibike['components'], identificador, pro)
            if pertenecer == True:
                lt.addLast(list_vertex, pro)

        l = []
        l_1 = []
        contador = 0
        estrucura = d.DepthFirstSearch(citibike['graph'], identificador)
        tiempo_total = abs(int(time1)-int(time2))
        iterador = it.newIterator(list_vertex)
        while it.hasNext(iterador):
            enlace = it.next(iterador)
            true_or_false = d.hasPathTo(estrucura, enlace)
            ruta = d.pathTo(estrucura, enlace)
            if (true_or_false == True) and (lt.size(ruta) > 2):
                nombre_inicial = identificador
                tiempo = 0
                delete = lt.removeFirst(ruta)
                last = lt.lastElement(ruta)
                iterado = it.newIterator(ruta)
                while it.hasNext(iterado):
                    enla = it.next(iterado)
                    obtener_peso = gr.getEdge(
                        citibike['graph'], nombre_inicial, enla)
                    if (obtener_peso is not None) and (tiempo_total > obtener_peso["weight"]+segundos) and (nombre_inicial != enla):
                        tiempo_total = abs(
                            tiempo_total-(obtener_peso["weight"]+segundos))
                        tiempo += (obtener_peso['weight']+segundos)
                        if enla == last:
                            obtener_peso_inverso = gr.getEdge(
                                citibike['graph'], enla, identificador)
                            if (obtener_peso_inverso is not None) and (tiempo_total > obtener_peso_inverso["weight"]):
                                tiempo += obtener_peso_inverso["weight"]
                                l.append(delete)
                                l.append(enla)
                                l.append(tiempo)
                                diccionario['rutas circulares'] = l
                                contador += 1
                            elif (obtener_peso_inverso is None):
                                l_1.append(delete)
                                l_1.append(enla)
                                l_1.append(tiempo)
                                dicc['rutas no circulares'] = l_1
                        nombre_inicial = enla
                    else:
                        answer = "tiempo"

            elif (true_or_false == True) and (lt.size(ruta) == 2):
                posicion = lt.getElement(ruta, 2)
                obtener_peso_1 = gr.getEdge(
                    citibike['graph'], identificador, posicion)
                if (tiempo_total > obtener_peso_1["weight"]+segundos):
                    tiempo_total = abs(
                        tiempo_total-(obtener_peso_1["weight"]+segundos))
                    obtener_peso_inverso_1 = gr.getEdge(
                        citibike['graph'], posicion, identificador)
                    if (obtener_peso_inverso_1 is not None) and (tiempo_total > obtener_peso_inverso_1["weight"]):
                        l.append(identificador)
                        l.append(posicion)
                        l.append(
                            (obtener_peso_1['weight'] + segundos+obtener_peso_inverso_1["weight"]))
                        diccionario['rutas circulares'] = l
                        contador += 1

        answer = (diccionario, contador, dicc)
    else:
        answer = "La estación no es válida, ingrese otra. "
    return answer


def tercera_consulta(citibike):
    tree = om.newMap(omaptype='RBT', comparefunction=compareroutes)
    tree_1 = om.newMap(omaptype='RBT', comparefunction=compareroutes)
    tree_2 = om.newMap(omaptype='RBT', comparefunction=compareroutes)
    diccionario = {}
    diccionario_salida = {}
    diccionario_llegada = {}
    diccionario_menos = {}
    list_vertext = gr.vertices(citibike["graph"])
    ite = it.newIterator(list_vertext)
    while it.hasNext(ite):
        vertex = it.next(ite)
        arrive = gr.adjacents(citibike["graph"], vertex)
        if arrive is not None:
            iterador = it.newIterator(arrive)
            while it.hasNext(iterador):
                vertex_arrive = it.next(iterador)
                num = gr.getEdge(citibike["graph"], vertex, vertex_arrive)
                if num['vertexA'] in diccionario_salida:
                    diccionario_salida[num['vertexA']] += num['count']
                if num['vertexA'] not in diccionario_salida:
                    diccionario_salida[num['vertexA']] = num['count']
                if num['vertexB'] in diccionario_llegada:
                    diccionario_llegada[num['vertexB']] += num['count']
                else:
                    diccionario_llegada[num['vertexB']] = num['count']

    for llave_salida in diccionario_salida:
        om.put(tree, diccionario_salida[llave_salida], llave_salida)
        diccionario_menos[llave_salida] = diccionario_salida[llave_salida]
        if llave_salida in diccionario_llegada:
            diccionario_menos[llave_salida] += diccionario_llegada[llave_salida]

    for llave_menos in diccionario_menos:
        om.put(tree_2, diccionario_menos[llave_menos], llave_menos)
    l_2 = []
    number_2 = om.size(tree_2)
    resta_2 = abs(number_2-3)
    re = abs(number_2-resta_2)
    less_2 = om.select(tree_2, re-1)
    greater_2 = om.minKey(tree_2)
    ran_2 = om.values(tree_2, greater_2, less_2)
    i_2 = it.newIterator(ran_2)
    while it.hasNext(i_2):
        name_2 = it.next(i_2)
        l_2.append(name_2)
    diccionario["Menos salidas y llegadas de viajes"] = l_2

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
    l.reverse()
    diccionario["salida"] = l

    for llave_llegada in diccionario_llegada:
        om.put(tree_1, diccionario_llegada[llave_llegada], llave_llegada)
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
    l_1.reverse()
    diccionario["llegada"] = l_1
    return diccionario


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

def cuarta_consulta(citibike, time, idstation):
    djkgraph = djk.Dijkstra(citibike['graph'], idstation)
    vertices = gr.vertices(citibike['graph'])

    keyvertex = vertices
    itevertex = it.newIterator(keyvertex)

    maxvertex = -1
    lista = None
    finalvertex = -1

    while(it.hasNext(itevertex)):
        vertex = it.next(itevertex)

        if(djk.distTo(djkgraph, vertex) <= float(time) and maxvertex < stack.size(djk.pathTo(djkgraph, vertex))):
            maxvertex = stack.size(djk.pathTo(djkgraph, vertex))
            lista = djk.pathTo(djkgraph, vertex)
            finalvertex = vertex

    return idstation, finalvertex, lista


def quinta_consulta(citibike, agerange):
    keysalida = m.keySet(citibike['salida'])
    keyllegada = m.keySet(citibike['llegada'])
    itellegada = it.newIterator(keyllegada)
    itesalida = it.newIterator(keysalida)

    maxllegada = -1
    maxsalida = -1
    idllegada = -1
    idsalida = -1

    while(it.hasNext(itellegada) or it.hasNext(itesalida)):
        if(it.hasNext(itesalida)):
            salida = it.next(itesalida)
            salidaentry = m.get(citibike['salida'], salida)
            if(maxsalida < me.getValue(salidaentry)[agerange]):
                maxsalida = me.getValue(salidaentry)[agerange]
                idsalida = me.getKey(salidaentry)


                
        if(it.hasNext(itellegada)):
            llegada = it.next(itellegada)
            llegadaentry = m.get(citibike['llegada'], llegada)
            if(maxllegada < me.getValue(llegadaentry)[agerange]):
                maxllegada = me.getValue(llegadaentry)[agerange]
                idllegada = me.getKey(llegadaentry)

    djkgraph = djk.Dijkstra(citibike['graph'], idsalida)
    camino = djk.pathTo(djkgraph, idllegada)

    return idsalida, idllegada, camino   



def sexta_consulta(citibike, latitud0, longitud0, latitud1, longitud1):
    keysalida = m.keySet(citibike['salida'])
    keyllegada = m.keySet(citibike['llegada'])
    itellegada = it.newIterator(keyllegada)
    itesalida = it.newIterator(keysalida)

    maxradiollegada = 5000
    maxradiosalida = 5000
    idllegada = -1
    idsalida = -1

    while(it.hasNext(itellegada) or it.hasNext(itesalida)):
        if(it.hasNext(itellegada)):
            llegada = it.next(itellegada)
            llegadaentry = m.get(citibike['llegada'], llegada)
            longitud = me.getValue(llegadaentry)['longitud']
            latitud = me.getValue(llegadaentry)['latitud']
            newradiollegada = pointCircle(latitud1, longitud1, latitud,longitud)
            if(newradiollegada < maxradiollegada):
                maxradiollegada = newradiollegada
                idllegada = llegada
            newradiosalida = pointCircle(latitud0, longitud0, latitud,longitud)
            if(newradiosalida < maxradiosalida):
                maxradiosalida = newradiosalida
                idsalida = llegada



        if(it.hasNext(itesalida)):
            salida = it.next(itesalida)
            salidaentry = m.get(citibike['salida'], salida)
            longitud = me.getValue(salidaentry)['longitud']
            latitud = me.getValue(salidaentry)['latitud']
            newradiollegada = pointCircle(latitud1, longitud1, latitud,longitud)
            if(newradiollegada < maxradiollegada):
                maxradiollegada = newradiollegada
                idllegada = llegada
            newradiosalida = pointCircle(latitud0, longitud0, latitud,longitud)
            if(newradiosalida < maxradiosalida):
                maxradiosalida = newradiosalida
                idsalida = llegada


    djkgraph = djk.Dijkstra(citibike['graph'], idsalida)
    camino = djk.pathTo(djkgraph, idllegada)
    duracion = djk.distTo(djkgraph, idllegada)

    return idsalida, idllegada, duracion, camino

def pointCircle(latc, lonc, latp, lonp):
    # Formula de Haversine
    R = 6371 # Radio de la tierra en Km
    dLat = aRadianes(float(latp)-float(latc)) # Pasar a radianes
    dLon = aRadianes(float(lonp)-float(lonc))
    a = math.sin(dLat/2)*2 + math.cos(aRadianes(float(latc))) * math.cos(aRadianes(float(latp))) * math.sin(dLon/2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c # Distancia en km
    return d

def aRadianes(deg):
    return deg * (float(math.pi)/180.0)
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
    stopcode = me.getKey(keyvaluestop)
    if (str(stop) == str(stopcode)):
        return 0
    elif (str(stop) > str(stopcode)):
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
