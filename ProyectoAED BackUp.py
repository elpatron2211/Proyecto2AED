# -*- coding: utf-8 -*-
"""
Algoritmos y Estructuras de Datos
Proyecto Fase No.2
Pablo Herrea, Juan Miguel Gonzalez-Campo, Pedro Marroquín, Paulo Sanchez
"""
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","1234"))
def getLugar(tx,nombre):
    query = "MATCH (l:Lugar) return l.name as n"
    result = tx.run(query,nombre=nombre)
    lugares = []
    for r in result:
        lugares.append(r["n"])
    return lugares


with(driver.session()) as ses:
    result = ses.write_transaction(getLugar,"Tikal")#esto es una lista
    for r in result:
        print(r)#r son los elementos en esa lista
        
#tengo que hacer tres querys que me regrese listas