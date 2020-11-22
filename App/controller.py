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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadFile(analyzer, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(analyzer, trip)
    return analyzer


def loadTrips(analyzer):
    for filename in cf.os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename)
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer, id1, id2):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer, id1, id2)


def segunda_consulta(analyzer, time1, time2, identificador):
    return model.segunda_consulta(analyzer, time1, time2, identificador)


def tercera_consulta(analyzer):
    return model.tercera_consulta(analyzer)


def cuarta_consulta(analyzer, time, id1):
    return model.cuarta_consulta(analyzer, time, id1)


def quinta_consulta(analyzer, edad):
    return model.quinta_consulta(analyzer, edad)


def sexta_consulta(analyzer, start_station_latitude, start_station_longitude, end_station_latitued, end_station_longitude):
    return model.sexta_consulta(analyzer, start_station_latitude, start_station_longitude, end_station_latitued, end_station_longitude)


def septima_consulta(analyzer, edad):
    return model.septima_consulta(analyzer, edad)


def octava_consulta(analyzer, identificador, time):
    time = datetime.datetime.strptime(time, '%Y-%m-%d')
    return model.segunda_consulta(identificador, time.date())
