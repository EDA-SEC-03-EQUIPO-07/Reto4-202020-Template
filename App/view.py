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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________
initialStation = None
recursionLimit = 2000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Cantidad de cluester de viajes")
    print("4- Ruta turística circular")
    print("5- Estaciones críticas ")
    print("6- Ruta turística por resistencia")
    print("7- Ruta más corta entre estaciones")
    print("8- Ruta de interes turístico")
    print("9- Identificación de estaciones para publicidad")
    print("10- Identificación de bicicletas pata el mantenimiento")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        first_Station = input("id de la primera estación ")
        second_Station = input("id de la segunda estación ")
        value_1 = controller.connectedComponents(
            cont, first_Station, second_Station)
        executiontime = timeit.timeit(number=1)
        print("Los números " + str(first_Station) +
              " y " + str(second_Station) + " " + str(value_1))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        time1 = input("Ingrese el tiempo disponible ")
        time2 = input("Ingrese el tiempo disponible ")
        identificador = input("id de la estación ")
        value_2 = controller.segunda_consulta(
            cont, time1, time2, identificador)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_2))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        value_3 = controller.tercera_consulta(cont)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_3))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        time_max = input("Ingrese el tiempo máximo ")
        start_station_id = input("id de la estación inicial ")
        value_4 = controller.cuarta_consulta(cont, time_max, start_station_id)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_4))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        edad = input = (
            "Ingrese alguno de los siguientes rangos de edad 0-10 \n, 11-20\n, 21-30\n, 31-40\n, 41-50\n, 51-60\n, 60 +\n ")
        value_5 = controller.quinta_consulta(cont, edad)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_5))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        start_station_latitude = input = (
            "Ingrese la latitud de su ubicación actual ")
        start_station_longitude = input = (
            "Ingrese la longitud de su ubicación actual ")
        end_station_latitude = input = (
            "Ingrese la latitud a donde quiere viajar ")
        end_station_longitude = input = (
            "Ingrese la longitud a donde quiere viajar ")
        value_6 = controller.sexta_consulta(cont,
                                            start_station_latitude, start_station_longitude, end_station_latitude, end_station_longitude)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_6))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        edad = input = (
            "Ingrese alguno de los siguientes rangos de edad 0-10 \n, 11-20\n, 21-30\n, 31-40\n, 41-50\n, 51-60\n, 60 +\n ")
        value_7 = controller.septima_consulta(cont, edad)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_7))
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 10:
        bike_id = input("Ingrese el id de la bicicleta ")
        time = input("Ingrese una fecha ")
        value_8 = controller.octava_consulta(cont, bike_id, time)
        executiontime = timeit.timeit(number=1)
        print("La información es la siguiente " + str(value_8))
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)
