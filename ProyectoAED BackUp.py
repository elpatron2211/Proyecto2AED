# -*- coding: utf-8 -*-
"""
Algoritmos y Estructuras de Datos
Proyecto Fase No.2
Pablo Herrea, Juan Miguel Gonzalez-Campo, Pedro Marroquín, Paulo Sanchez
"""
import csv
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","1234"))

#-----------------------------------------------------------------------------
#se crean los querys para poder hacer las relaciones 
def GetCulturaDb(tx,cultura):
    query = "MATCH (c:Cultura) -- (l:Lugar) WHERE c.name = $nombre RETURN l.name as n"
    result_query = tx.run(query,nombre=cultura)
    firsts_relations = []
    for r in result_query:
        firsts_relations.append(r["n"])
    return firsts_relations

def GetTipoLugarDb(tx,TipoLugar):
    query = "MATCH (t:TipoLugar) -- (l:Lugar) WHERE t.name = $nombre RETURN l.name as n"
    result_query = tx.run(query,nombre=TipoLugar)
    second_relations = []
    for r in result_query:
        second_relations.append(r["n"])
    return second_relations

def GetCostosDb(tx,Costo):
    query = "MATCH (c:Costo) -- (l:Lugar) WHERE c.name = $nombre RETURN l.name as n"
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
    for n in lista1:
        if n in lista2 and n in lista3:
            RecommendedPlaces.append(n)        
    return RecommendedPlaces

def ShowRecommendations(recommendedplaces):
    if len(recommendedplaces) <= 0:
        print("Sus respuestas no han ayudado a los criterios de busqueda, lo sentimos")
    elif len(recommendedplaces) > 5:
        i = 0
        while i < 5:
            print(recommendedplaces[i])
            i = i+1
    else:
        for n in recommendedplaces:
            print(n)


#-----------------------------------------------------------------------------
#Funciones que trabajan la lógica de inicio de sesión y creación de usuarios

#Funcion para preguntar si se quiere iniciar sesion o registrar un nuevo usuario            
def IniciarORegistrar():
    onIn = True
    while (onIn):    
        print("Ingrese 1 para iniciar sesión, ingrese 2 para crear un usuario")
        try:
            option = 0
            while option <= 0 or option >2:
                print("Ingrese una opcion dentro del menu")
                option = int(input())
                break
            return option
        except Exception:
            print("Ha ingresado un dato invalido\nDato debe ser un numero, intentelo de nuevo")
            continue
    
#Funcion para iniciar sesión con un usuario existente, devuelve el nombre de usuario   
def inicioSesion():
    on = True
    cancelar1 = "999000111"
    while(on):
        print("Ingrese su nombre de usuario")
        usuario = input()
        if usuario in dictUsuarios:
            print("Ingrese su contrasenia")
            contrasenia = input()
            if dictUsuarios.get(usuario) == contrasenia:
                print("Se ha iniciado sesion!")
                return usuario
            else: 
                print("Contrasenia incorrecta, intentelo de nuevo")
                continue
        else:
            print("Usuario no encontrado, ingrese 1 para intentar de nuevo o 2 para regresar al menu de inicio")
            try:
                option = int(input("Ingrese una opcion del menu\n"))
                while option <= 0 or option >2:
                    print("Ingrese una opcion dentro del menu")
                    option = int(input())
                    break
                if option == 1:
                    continue
                if option == 2:
                    break
            except Exception:
                print("Ha ingresado un dato invalido\nDato debe ser un numero, intentelo de nuevo")
                return False
    if option == 2:
        return cancelar1
    
    
#Funcion para registrar un nuevo usuario, devuelve el nombre de usuario      
def registrar():
    on2 = True
    nuevoUsuario = ""
    while(on2):
        print("Ingrese un nombre de usuario")
        nuevoUsuario = ""
        nuevoUsuario = input()
        if nuevoUsuario in dictUsuarios or nuevoUsuario == "999000111":
            print("Lo sentimos ese usuario no esta disponible!")
            continue
        else: 
            break
    print("Ingrese su contrasenia")
    nuevaContrasenia = input()
    usuarioContrasenia = [nuevoUsuario, nuevaContrasenia]
    with open('usuarios.csv', mode ='a', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter
        csvwriter.writerow(usuarioContrasenia)
    print("Usuario aniadido!")
    return nuevoUsuario

#-----------------------------------------------------------------------------
#Inicio del Programa   

#Se lee el archivo que contiene los usuarios y contraseñas
with open('usuarios.csv', mode='r') as f:
    csvFile = csv.reader(f, delimiter =',')
    
    dictUsuarios = {rows[0]:rows[1] for rows in csvFile}

with open('recomendaciones.csv', mode='r') as f1:
    csvFile1 = csv.reader(f1, delimiter =',')
    
    dictRecomendaciones = {rows[0]:rows[1] for rows in csvFile1}

print(type(dictRecomendaciones.get("juan")))

   
#Inicio de sesión o registro de nuevos usuarios 
print("\n\nInicio de session\n")
usuario = ""
on1 = True
while (on1):
    InOReg = IniciarORegistrar()
    if (InOReg == 1):
        usuario = inicioSesion()
        if usuario == "999000111":
            continue
        else: 
            break
    else:
        usuario = registrar()
        break

#Comenzar preguntas para recomendaciones
print("\n\nHola "+usuario+"!")
print("Bienvenido a GuateGrafoTour, tu mejor sistema de recomendacion")
onIn = True
while (onIn):    
    print("Por favor, escribe 1 para ver tus recomendaciones anteriores o escribe 2 para encuentrar nuevas")
    try:
        option2 = 0
        while option2 <= 0 or option2 >2:
            print("Ingrese una opcion dentro del menu")
            option2 = int(input())
            break
        break
    except Exception:
        print("Ha ingresado un dato invalido\nDato debe ser un numero, intentelo de nuevo")
        continue

    
    
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
cultura_parameter = GetCultura(Cultura)
Tipo_parameter = GetTipoLugar(TipoLugar)
Costo_parameter = GetCosto(Costo)
with(driver.session()) as ses:
    LugarCultura = ses.write_transaction(GetCulturaDb,cultura_parameter)   
    LugarTipo = ses.write_transaction(GetTipoLugarDb,Tipo_parameter)
    LugarCosto = ses.write_transaction(GetCostosDb,Costo_parameter)
    
Recommended_places = RecomendationsEngine(LugarCultura, LugarTipo, LugarCosto)
usuarioRec = [usuario, Recommended_places]
with open('recomendaciones.csv', mode ='a', newline='') as f1:
        csvwriter1 = csv.writer(f1)
        csvwriter1
        csvwriter1.writerow(usuarioRec) 
print("De acuerdo con lo que ha respondido, los lugares recomendados para usted en orden de conveniencia son los siguientes:")
print()
ShowRecommendations(Recommended_places)
