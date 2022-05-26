# -*- coding: utf-8 -*-
"""
Algoritmos y Estructuras de Datos
Proyecto Fase No.2
Pablo Herrea, Juan Miguel Gonzalez-Campo, Pedro Marroquín, Paulo Sanchez
"""
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","1234"))

#-----------------------------------------------------------------------------
#se crean los querys para poder hacer las relaciones 
def GetCulturaDb(tx,cultura):
    query = "MATCH (c:Costo) -- (l:Lugar) RETURN l.name as n"
    result_query = tx.run(query,nombre=cultura)
    firsts_relations = []
    for r in result_query:
        firsts_relations.append(r["n"])
    return firsts_relations

def GetTipoLugarDb(tx,TipoLugar):
    query = "MATCH (t:TipoLugar) -- (l:Lugar) RETURN l.name as n"
    result_query = tx.run(query,nombre=TipoLugar)
    second_relations = []
    for r in result_query:
        second_relations.append(r["n"])
    return second_relations

def GetCostosDb(tx,Costo):
    query = "MATCH (c:Costo) -- (l:Lugar) RETURN l.name as n"
    result_query = tx.run(query,nombre=Costo)
    third_relations = []
    for r in result_query:
        third_relations.append(r["n"])
    return third_relations
#-----------------------------------------------------------------------------
#Se crean los menus para tener la opinion del usuario
def MenuCultura():
    print("Que Cultura de Guatemala le atrae mas?")
    print("1.Maya")
    print("2.Ladina")
    print("3.Garifuna")
    try:
        option = int(input("Ingrese una opcion del menu\n"))
        while option <= 0 or option >3:
            print("Ingrese una opcion dentro del menu")
            option = int(input())
            break
        return option
    except Exception:
        print("Ha ingresado un dato invalido\nDato debe ser un numero, intentelo de nuevo")
        return False

def MenuTipoLugar():
    print("\nQue tipo de area le atrae mas?")
    print("1.Rural")
    print("2.Urbano")
    try:
        option = int(input("Ingrese una opcion del menu\n"))
        while option <= 0 or option >2:
            print("Ingrese una opcion dentro del menu")
            option = int(input())
            break
        return option
    except Exception:
        print("Ha ingresado un dato invalido\nDato debe ser un numero, intentelo de nuevo")

def MenuCostos():
    print("\nComo es su presupuesto para ir de turismo?")
    print("1.Alto")
    print("2.Medio")
    print("3.Bajo")
    try:
        option = int(input("Ingrese una opcion del menu\n"))
        while option <= 0 or option >3:
            print("Ingrese una opcion dentro del menu")
            option = int(input())
            break
        return option
    except Exception:
        print("Ha ingresado un dato invalido\nDato debe ser un numero, intentelo de nuevo")
        return False

def GetCultura(Cultura):
    if Cultura == 1:
        return "Cultura Maya"
    elif Cultura == 2:
        return "Cultura Ladina"
    elif Cultura == 3:
        return "Cultura Garífuna"
    
def GetTipoLugar(TipoLugar):
    if TipoLugar == 1:
        return "Rural"
    elif TipoLugar == 2:
        return "Urbano"

def GetCosto(CostoLugar):
    if CostoLugar == 1:
        return "Alto"
    elif CostoLugar == 2:
        return "Medio"
    elif CostoLugar == 3:
        return "Bajo"
#-----------------------------------------------------------------------------
#se crea la funcion que hara las recomendaciones
def RecomendationsEngine(lista1,lista2,lista3):
    RecommendedPlaces = []
    for element in lista1:
        if element in lista2 and element in lista3:
            RecommendedPlaces.append(element)
    return RecommendedPlaces

def ShowRecommendations(recommendedplaces):
    i=1
    for n in recommendedplaces:
        print(str(i)+".",n)
        i=i+1
#-----------------------------------------------------------------------------
#Inicio del Programa
print("Bienvenido a GuateGrafoTour, tu mejor sistema de recomendacion")
print("Por favor, vaya respondiendo las preguntas y siga las instrucciones a continuacion")
Cultura = MenuCultura()
while(Cultura==False):
    print()
    Cultura = MenuCultura()
    
TipoLugar = MenuTipoLugar()
while(TipoLugar==False):
    print()
    TipoLugar = MenuTipoLugar()

Costo = MenuCostos()
while(Costo == False):
    print()
    Costo = MenuCostos()

#-----------------------------------------------------------------------------
print()
print("Usted ha escogido lo siguiente...")
print("Cultura: "+GetCultura(Cultura))
print("Tipo de Lugar: "+GetTipoLugar(TipoLugar))
print("Presupuesto: "+GetCosto(Costo))
#-----------------------------------------------------------------------------
#se hacen las listas necesarias para comparar
with(driver.session()) as ses:
    LugarCultura = ses.write_transaction(GetCulturaDb,GetCultura(Cultura))
    LugarTipo = ses.write_transaction(GetTipoLugarDb,GetTipoLugar(TipoLugar))
    LugarCosto = ses.write_transaction(GetCostosDb,GetCosto(Costo))
    
Recommended_places = RecomendationsEngine(LugarCultura, LugarTipo, LugarCosto)
print("De acuerdo con lo que ha respondido, los lugares recomendados para usted en orden de conveniencia son los siguientes:")
print()
ShowRecommendations(Recommended_places)