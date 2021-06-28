import sys
import pathlib
import math
import logging
import pygame
import numpy as np
from random import randrange, choice
from numpy import random
from math import log
from functools import cmp_to_key

 
class TYPE_GRAFO:
    GRAFO_NONE = 'NONE'
    GRAFO_BASE = 'BASE'
    GRAFO_MALLA = 'MALLA'
    GRAFO_ERDOS_N_RENYI = 'ERDOS_N_RENYI'
    GRAFO_GILBERT = 'GILBERT'
    GRAFO_GEOGRAFICO = 'GEOGRAFICO '
    GRAFO_BARABASI_ALBERT = 'BARBASI_ALBERT'
    GRAFO_DOROGOVTSEV_MENDES = 'DOROGOVTSEV_MENDES'
    GRAFO_MODELO_BFS = 'BFS'
    GRAFO_MODELO_DFS_I = 'DFS_I'
    GRAFO_MODELO_DFS_R = 'DFS_R'
    GRAFO_MODELO_DIJKSTRA = 'DIJKSTRA'
    GRAFO_MODELO_KRUSKAL = 'KRUSKAL'
    GRAFO_MODELO_KRUSKAL_INVERSO = 'KRUSKAL_INVERSO'
    GRAFO_MODELO_PRIM = 'PRIM'
    
class Nodo:
    label = ''
    grado = 0 #Solamente para BARBASI_ALBERT
    peso_dijkstra = sys.maxsize #Solamente para DIJKSTRA

    def __init__(self, name = None, type_node = None, num  = None, num_i = None, num_j = None):
        self.name = name
        self.type_node = type_node
        self.num = num
        self.num_i = num_i
        self.num_j = num_j
        self.color_BFS = ""
        self.color_DFS_R = ""
        self.color_DFS_I = ""
        self.visitado_DFS_R = False
        self.visitado_DFS_I = False
        self.visitado_DIJKSTRA = False
        self.visitado_KRUSKAL_INVERSO = False
        self.visitado_PRIM = False
        self.visitado_PRIM_TMP = False
        self.is_label_peso = False
    
    def __str__(self):
        return "NODO[num: {num}]".format(num = self.num)
 
    def __setitem__(self, k, v):
        if k == "visitado_KRUSKAL_INVERSO":
            self.visitado_KRUSKAL_INVERSO = v
        if k == "visitado_PRIM":
            self.visitado_PRIM = v
        if k == "visitado_PRIM_TMP":
            self.visitado_PRIM_TMP = v

    def __getitem__(self, k):
        if k == "visitado_KRUSKAL_INVERSO":
            return self.visitado_KRUSKAL_INVERSO
        if k == "visitado_PRIM":
            return self.visitado_PRIM
        if k == "visitado_PRIM_TMP":
            return self.visitado_PRIM_TMP

    def getLabel(self):
        prefix = 'nd_'
        if (self.type_node == TYPE_GRAFO.GRAFO_BASE 
        or self.type_node == TYPE_GRAFO.GRAFO_ERDOS_N_RENYI 
        or self.type_node == TYPE_GRAFO.GRAFO_GILBERT 
        or self.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO
        or self.type_node == TYPE_GRAFO.GRAFO_BARABASI_ALBERT
        or self.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES):
            return prefix + str(self.num)
        elif self.type_node == TYPE_GRAFO.GRAFO_MALLA:
            return prefix + str(self.num_i) + '_' + str(self.num_j)
    
class Arista:
    MAX_DISTANCIA = 1000 #Solamente para DIJKSTRA

    def __init__(self, nodo_inicial, nodo_final):
        self.nodo_inicial = nodo_inicial
        self.nodo_final = nodo_final
        self.distancia = 0    


    def setDistancia(self):
        self.distancia = random.randint(self.MAX_DISTANCIA)
    
    def __str__(self):
        return "ARISTA[NODO_INICIAL[num: {num_inicial}],NODO_FINAL[num: {num_final}]]".format(num_inicial = (str(self.nodo_inicial.num) if self.nodo_inicial is not None else "None"), num_final = (str(self.nodo_final.num) if self.nodo_final is not None else "None"))
    
class Grafo:
    NUM_DM_ARISTA_3 = 3 #Solamente para DOROGOVTSEV_MENDES
    LT_COLOR = ["yellow","magenta","blue","blueviolet","brown","cadetblue","chartreuse","chocolate","coral","cornflowerblue","crimson","darkblue","darkcyan","darkgoldenrod","darkgreen","darkmagenta","darkolivegreen","darkorange","darkred","darksalmon","darkseagreen","darkslateblue","darkslategray","darkturquoise","darkviolet","deeppink","deepskyblue","dimgray","dimgrey","dodgerblue","firebrick","forestgreen","fuchsia","gainsboro","ghostwhite","gold","goldenrod","gray","grey","green","greenyellow","honeydew","hotpink","indianred","indigo","ivory","khaki","lavender","lavenderblush","lawngreen","lemonchiffon","lightblue","lightcoral","lightcyan","lightgoldenrodyellow","lightgray","lightgreen","lightgrey","lightpink","lightsalmon","lightseagreen","lightskyblue","lightslategray","lightslategrey","lightsteelblue","lightyellow","lime","limegreen","linen","magenta","maroon","mediumaquamarine","mediumblue","mediumorchid","mediumpurple","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise","mediumvioletred","midnightblue","mintcream","mistyrose","moccasin","navajowhite","navy","oldlace","olive","olivedrab","orange","orangered","orchid","palegoldenrod","palegreen","paleturquoise","palevioletred","papayawhip","peachpuff","peru","pink","plum","powderblue","purple","red","rosybrown","royalblue","saddlebrown","salmon","sandybrown","seagreen","seashell","sienna","silver","skyblue","slateblue","slategray","slategrey","snow","springgreen","steelblue","tan","teal","thistle","tomato","turquoise","violet","wheat","white","whitesmoke","yellow","yellowgreen"]
    
    def __init__(self, es_dirigido = False):
        self.ltNodos = [] 
        self.ltAristas = [] 
        self.ltAristas_BFS = [] 
        self.ltAristas_DFS_R = [] 
        self.ltAristas_DFS_I = [] 
        self.ltAristas_DIJKSTRA = [] 
        self.ltAristas_KRUSKAL = []
        self.ltAristas_KRUSKAL_ARBOL = []
        self.ltAristas_KRUSKAL_ARBOL_INVERSO = []
        self.ltAristas_PRIM_ARBOL = []
        self.ltCapas = []
        self.max_random_nodos = 0 #Solamente para GILBERT
        self.type_node = TYPE_GRAFO.GRAFO_NONE
        self.is_BFS = False
        self.is_DFS_R = False
        self.is_DFS_I = False
        self.is_DIJKSTRA = False
        self.is_KRUSKAL = False
        self.is_KRUSKAL_INVERSO = False
        self.is_PRIM = False
        self.es_dirigido = es_dirigido
        self.set_aristas = set()#Solamente si es DIRIGIDO
        self.nodo_kruskal = Nodo()
        self.nodo_kruskal_inverso = Nodo()
        self.nodo_prim = Nodo()
        
#METODOS Creacion
    def crearNodos(self, num_nodos = None, max_nodos = None, num_i = None, num_j = None, prec = None):
        if (self.type_node == TYPE_GRAFO.GRAFO_BASE 
        or self.type_node == TYPE_GRAFO.GRAFO_ERDOS_N_RENYI 
        or self.type_node == TYPE_GRAFO.GRAFO_GILBERT 
        or self.type_node == TYPE_GRAFO.GRAFO_BARABASI_ALBERT):
            if max_nodos is not None:
                self.max_random_nodos = random.randint(max_nodos)
            elif num_nodos is not None:
                self.max_random_nodos = num_nodos
            for i in range(self.max_random_nodos):
                self.ltNodos.append(Nodo(type_node = self.type_node, num = i))
        elif self.type_node == TYPE_GRAFO.GRAFO_MALLA:
            num = 0
            for i in range(num_i):
                for j in range(num_j):
                    self.ltNodos.append(Nodo(type_node = self.type_node, num = num, num_i = i, num_j = j))
                    num = num + 1
        elif self.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO:
            for num in range(num_nodos):
                self.ltNodos.append(Nodo(type_node = self.type_node, num = num, num_i = round(random.random()*num_i, prec), num_j = round(random.random()*num_j, prec)))
        elif self.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES:
            self.ltNodos.append(Nodo(type_node = self.type_node, num = 0, num_i = 0, num_j = 0))
            self.ltNodos.append(Nodo(type_node = self.type_node, num = 1, num_i = 0, num_j = 2))
            self.ltNodos.append(Nodo(type_node = self.type_node, num = 2, num_i = 2, num_j = 1))
            for num in range(self.NUM_DM_ARISTA_3, self.NUM_DM_ARISTA_3 + num_nodos):
                self.ltNodos.append(Nodo(type_node = self.type_node, num = num))
        
    def crearAristas(self, type_node = None, num_nodos = None, max_num_aristas = None, num_i = None, num_j = None, probabilidad = None, r_distancia = None, max_grado = None):
        type_node_if = self.type_node if type_node is None else type_node
        if type_node_if == TYPE_GRAFO.GRAFO_BASE:
            print()
        elif type_node_if == TYPE_GRAFO.GRAFO_MALLA:
            num = 0
            for i in range(num_i):
                for j in range(num_j):
                    nodo_inicial = self.findNodoMalla(i,j)
                    if(i < num_i - 1):
                        self.appendArista(nodo_inicial = nodo_inicial, nodo_final = self.findNodoMalla(i+1,j))
                    if(j < num_j - 1):
                        self.appendArista(nodo_inicial = nodo_inicial, nodo_final = self.findNodoMalla(i,j+1))
        elif type_node_if == TYPE_GRAFO.GRAFO_ERDOS_N_RENYI:
            max_random_aristas = (num_nodos-1) + random.randint(max_num_aristas)
            for i in range(max_random_aristas):
                self.appendArista(nodo_inicial = self.findNodo(random.randint(self.max_random_nodos)), 
                                             nodo_final = self.findNodo(random.randint(self.max_random_nodos)))
        elif type_node_if == TYPE_GRAFO.GRAFO_GILBERT:
            for i in range(self.max_random_nodos):
                for j in range(self.max_random_nodos):
                    if(i != j and random.randint(1,101) <= probabilidad * 100 ):
                        self.appendArista(nodo_inicial = self.findNodo(i), nodo_final = self.findNodo(j))
        elif type_node_if == TYPE_GRAFO.GRAFO_GEOGRAFICO:
            for nodo_inicial in self.ltNodos:
                for nodo_final in self.ltNodos:
                    dist = math.sqrt(pow(nodo_final.num_i - nodo_inicial.num_i,2) + pow(nodo_final.num_j - nodo_inicial.num_j,2))
                    if dist <= r_distancia and nodo_inicial.num != nodo_final.num:
                        self.appendArista(nodo_inicial = nodo_inicial, nodo_final = nodo_final)
        elif type_node_if == TYPE_GRAFO.GRAFO_BARABASI_ALBERT:
            for i_nodo in range(num_nodos):
                i_nodo_anterio = i_nodo - 1
                while i_nodo_anterio >= 0:
                    nodo_actual = self.findNodo(i_nodo)
                    nodo_anterior =  self.findNodo(i_nodo_anterio)
                    if nodo_actual.grado < max_grado and nodo_anterior.grado < max_grado:
                        probabilidad_grado = (1 - (nodo_actual.grado / max_grado)) * 100
                        if random.randint(1,101) <= probabilidad_grado:
                            nodo_actual.grado = nodo_actual.grado + 1
                            nodo_anterior.grado = nodo_anterior.grado + 1
                            self.appendArista(nodo_inicial = nodo_actual, nodo_final = nodo_anterior)
                    i_nodo_anterio = i_nodo_anterio - 1
        elif type_node_if == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES:
            self.appendArista(nodo_inicial = self.findNodo(0), nodo_final = self.findNodo(1))
            self.appendArista(nodo_inicial = self.findNodo(1), nodo_final = self.findNodo(2))
            self.appendArista(nodo_inicial = self.findNodo(2), nodo_final = self.findNodo(0))
            for i_nodo in range(self.NUM_DM_ARISTA_3, self.NUM_DM_ARISTA_3 + num_nodos):
                nodo_actual = self.findNodo(i_nodo)
                num_aristas = len(self.ltAristas)
                prob_arista = random.randint(num_aristas)
                #print("num_aristas: " + str(num_aristas) + " prob_arista: " + str(prob_arista))
                o_arista = self.ltAristas[prob_arista]
                nodo_actual.num_i = o_arista.nodo_inicial.num_i + 1
                nodo_actual.num_j = o_arista.nodo_inicial.num_j + 1
                self.appendArista(nodo_inicial = nodo_actual, nodo_final = o_arista.nodo_inicial)
                self.appendArista(nodo_inicial = nodo_actual, nodo_final = o_arista.nodo_final)
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_BFS:
            self.ltNodos.sort(key = self.sortNodo)
            #print("ltNodosIncial: " + str(len(self.ltNodos)))
            ltNodo_Capa0 = [self.getNodoInicialConectado()]
            self.ltCapas.append(ltNodo_Capa0)
            #print("Capa0")#DEBUG
            #self.printCapa()#DEBUG
            ltNodos_Capa1 = self.findNodosConectadosNodo(ltNodo_Capa0[0])#Capa1
            ltNodosActual = self.findNodoEnCapas(ltNodos_Capa1, self.ltCapas)
            ltNodosActual = self.filterNodoFinal(ltNodosActual)
            ltNodosActual.sort(key = self.sortNodo)
            self.ltCapas.append(ltNodosActual)
            #print("Capa1")#DEBUG
            #self.printCapa()#DEBUG
            #iCapa = 2
            ltCapaN = ltNodos_Capa1
            while(len(ltCapaN) > 0):#CapaN
                ltNodosN = []
                for nodo in ltCapaN:
                    ltNodosJoin = self.findNodosConectadosNodo(nodo)
                    ltNodosActual = self.findNodoEnCapas(ltNodosJoin, self.ltCapas)
                    ltNodosN = ltNodosN + ltNodosActual
                ltNodosN = self.filterNodoFinal(ltNodosN)
                ltNodosN.sort(key = self.sortNodo)
                self.ltCapas.append(ltNodosN)
                #print("Capa" + str(iCapa))#DEBUG
                #self.printCapa()#DEBUG
                #iCapa = iCapa + 1
                ltCapaN = ltNodosN

            nodo_agregado = [(self.ltCapas[0])[0].num]
            for i_capa in range(1, len(self.ltCapas)):
                capa_anterior = self.ltCapas[i_capa - 1]
                capa_actual = self.ltCapas[i_capa]
                for nodo_inicial in capa_anterior:
                    for nodo_final in capa_actual: 
                        if not nodo_final.num in nodo_agregado:
                            arista = self.findArista(nodo_inicial, nodo_final)
                            if arista is not None:
                                self.ltAristas_BFS.append(arista)
                                nodo_agregado.append(nodo_inicial.num)
                                nodo_agregado.append(nodo_final.num)
            #Set Color BFS 
            i_color = 0
            for ltNodo in self.ltCapas:
                for nodo in ltNodo:
                    nodo.color_BFS = self.LT_COLOR[i_color]
                i_color = (i_color + 1) % len(self.LT_COLOR)
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_DFS_R:
            self.ltNodos.sort(key = self.sortNodo)
            nodo_inicial = self.getNodoInicialConectado()
            self.depthDFR_R(nodo_inicial, i_color = 0)
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_DFS_I:
            self.ltNodos.sort(key = self.sortNodo)
            nodo_inicial = self.getNodoInicialConectado()
            nodo_inicial.visitado_DFS_I = True

            lt_arbol = []
            i_profundidad = 0
            lt_arbol.append([nodo_inicial])
            while i_profundidad >= 0:
                i_next_profundidad = i_profundidad + 1
                i_last_profundidad = i_profundidad - 1
                lt_nodos = lt_arbol[i_profundidad]
                lt_arbol.append([])
                #print("------------Capa: " + str(i_profundidad) + "\tNodosAgregados: " + str(len(lt_nodos)))#DEBUG
                is_new = False
                for nodo in lt_nodos:
                    ltNodosConect = self.findNodosConectadosNodo(nodo)
                    ltNodosConect.sort(key = self.sortNodo)
                    #print("BUSQUEDA: " + str(nodo) + "\tSizeDeNodosConectados: " + str(len(ltNodosConect)))#DEBUG
                    i_nodo_count = 1
                    for nodo_conect in ltNodosConect:
                        if nodo_conect.visitado_DFS_I == True:
                            #print("NodoAgregadoPreviamente: {0}\tNodoPosicion: {1:d}".format(nodo_conect, i_nodo_count))#DEBUG
                            i_nodo_count = i_nodo_count + 1
                            continue

                        arista = self.findArista(nodo, nodo_conect)
                        if arista is not None :
                            self.ltAristas_DFS_I.append(arista)
                            nodo_conect.visitado_DFS_I = True
                            nodo_conect.color_DFS_I = self.LT_COLOR[(i_profundidad) % len(self.LT_COLOR)]
                            lt_arbol[i_next_profundidad].append(nodo_conect)
                            #print("AppendNodo: {2}\tASiguienteCapa: {0:d}\tNodoPosicion: {1:d}".format(i_next_profundidad, i_nodo_count, nodo_conect), end='\n')#DEBUG
                            is_new = True
                            break
                if is_new:
                    i_profundidad = i_next_profundidad
                else:
                    i_profundidad = i_last_profundidad
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_DIJKSTRA:
            self.crearAristasDistancia(self.ltAristas_DIJKSTRA)

            #Algoritmo DIJKSTRA
            self.ltNodos.sort(key = self.sortNodo)
            nodo_inicial = self.getNodoInicialConectado()
            nodo_inicial.peso_dijkstra = 0
            nodo_inicial.visitado_DIJKSTRA = True

            ltNodoAgregado = [nodo_inicial]
            
            while True:
                #logging.debug("NodoInicial={nodo_inicial}".format(nodo_inicial=nodo_inicial))#DEBUG
                set_visitado_nodo = set()
                arista = self.setPesosDIJKSTRA(nodo_inicial, ltNodoAgregado, set_visitado_nodo)
                if arista is not None:
                    arista.nodo_final.peso_dijkstra = arista.nodo_inicial.peso_dijkstra + arista.distancia
                    arista.nodo_final.visitado_DIJKSTRA = True
                    ltNodoAgregado.append(arista.nodo_final)
                else:
                    break
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_KRUSKAL:
            if len(self.ltAristas_KRUSKAL) <= 0:
                self.crearAristasDistancia(self.ltAristas_KRUSKAL)

            mz_conjunto = []
            #Algoritmo DIJKSTRA
            self.ltAristas_KRUSKAL.sort(key = self.sortAristaPeso)
            for arista_kruskal in self.ltAristas_KRUSKAL:
                logging.debug("---\nDistancia={distancia}".format(distancia=arista_kruskal.distancia))
                self.appendMatrizKruskal(mz_conjunto, arista_kruskal)
            #Calcular distancia(MST)
            distancia_max = 0
            for arista in self.ltAristas_KRUSKAL_ARBOL:
                distancia_max = distancia_max + arista.distancia
            self.nodo_kruskal = Nodo()
            self.nodo_kruskal.is_label_peso = True
            self.nodo_kruskal.name = "Peso: " + str(distancia_max)
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_KRUSKAL_INVERSO:
            if len(self.ltAristas_KRUSKAL) <= 0:
                self.crearAristasDistancia(self.ltAristas_KRUSKAL)

            set_grafo = set()
            nodo_inicial = self.getNodoInicialConectado()
            self.encontrarGrafo(self.ltAristas_KRUSKAL, nodo_inicial, set_grafo, "visitado_KRUSKAL_INVERSO")
            i_grafo_size = len(set_grafo)
            #Algoritmo DIJKSTRA Inverso
            ltAristaEliminadas = []
            self.ltAristas_KRUSKAL.sort(key = self.sortAristaPeso, reverse = True)
            for arista_kruskal in self.ltAristas_KRUSKAL:
                set_grafo_nuevo = set()
                ltAristaTmp = []
                for arista_kruskal_tmp in self.ltAristas_KRUSKAL:
                    arista_kruskal_tmp.nodo_inicial.visitado_KRUSKAL_INVERSO = False
                    arista_kruskal_tmp.nodo_final.visitado_KRUSKAL_INVERSO = False
                    ltAristaTmp.append(arista_kruskal_tmp)
                #Eliminar arista actual
                ltAristaTmp.remove(arista_kruskal)
                #Eliminar aristas previamente eliminadas
                for arista_eliminada in ltAristaEliminadas:
                    ltAristaTmp.remove(arista_eliminada)
                logging.debug("---\nDistancia={distancia}".format(distancia=arista_kruskal.distancia))
                self.encontrarGrafo(ltAristaTmp, nodo_inicial, set_grafo_nuevo, "visitado_KRUSKAL_INVERSO")
                i_grafoTmp_size = len(set_grafo_nuevo)
                logging.debug("i_grafoTmp_size={i_grafoTmp_size} , i_grafo_size={i_grafo_size}".format(i_grafoTmp_size=i_grafoTmp_size, i_grafo_size=i_grafo_size))
                if i_grafo_size != i_grafoTmp_size:
                    self.ltAristas_KRUSKAL_ARBOL_INVERSO.append(arista_kruskal)
                else:
                    ltAristaEliminadas.append(arista_kruskal)
                #Calcular distancia(MST)
            distancia_max = 0
            for arista in self.ltAristas_KRUSKAL_ARBOL_INVERSO:
                distancia_max = distancia_max + arista.distancia
            self.nodo_kruskal_inverso = Nodo()
            self.nodo_kruskal_inverso.is_label_peso = True
            self.nodo_kruskal_inverso.name = "Peso: " + str(distancia_max)
        elif type_node_if == TYPE_GRAFO.GRAFO_MODELO_PRIM:
            if len(self.ltAristas_KRUSKAL) <= 0:
                self.crearAristasDistancia(self.ltAristas_KRUSKAL)

            set_grafo = set()
            set_grafo_tmp = set()
            set_nodo = set()
            nodo_inicial = self.getNodoInicialConectado()
            self.encontrarGrafo(self.ltAristas_KRUSKAL, nodo_inicial, set_grafo, "visitado_PRIM")
            self.setInOrAdd(set_nodo, nodo_inicial.num)
            for arista_kruskal in self.ltAristas_KRUSKAL:
                arista_kruskal.nodo_inicial.visitado_PRIM = False
                arista_kruskal.nodo_final.visitado_PRIM = False
                
            dict_grafo = {}
            while len(set_grafo_tmp) != len(set_grafo):
                self.depthPrim(self.ltAristas_KRUSKAL, nodo_inicial, dict_grafo)
                ltValues = list(dict_grafo.keys())
                ltValues.sort()
                if len(ltValues) > 0:
                    value = ltValues[0]
                    arista = dict_grafo[value]["arista"]
                    nodo_conect = dict_grafo[value]["nodo_conect"]
                    dict_grafo.pop(value)
                    if self.setInOrAdd(set_nodo, nodo_conect.num):
                        logging.debug("Value={value} ".format(value=value))
                        nodo_inicial = nodo_conect
                        self.ltAristas_PRIM_ARBOL.append(arista)
                        
                        set_grafo_tmp = set()
                        nodo_inicial_tmp = self.getNodoInicialConectado()
                        
                        self.encontrarGrafo(self.ltAristas_PRIM_ARBOL, nodo_inicial_tmp, set_grafo_tmp, "visitado_PRIM_TMP")
                        for arista_kruskal in self.ltAristas_PRIM_ARBOL:
                            arista_kruskal.nodo_inicial.visitado_PRIM_TMP = False
                            arista_kruskal.nodo_final.visitado_PRIM_TMP = False

                logging.debug("set_grafo={set_grafo}, set_grafo_tmp={set_grafo_tmp} ".format(set_grafo_tmp=len(set_grafo_tmp),set_grafo=len(set_grafo)))
            distancia_max = 0
            for arista in self.ltAristas_PRIM_ARBOL:
                distancia_max = distancia_max + arista.distancia
            self.nodo_prim = Nodo()
            self.nodo_prim.is_label_peso = True
            self.nodo_prim.name = "Peso: " + str(distancia_max)
                
#
    def appendMatrizKruskal(self, mz_conjunto, arista):
        i_find_inicial = -1
        i_find_final = -1

        num_inicial = arista.nodo_inicial.num
        num_final = arista.nodo_final.num
        num_arbol = 0

        logging.debug("mz_conjunto={mz_conjunto}".format(mz_conjunto=mz_conjunto))

        i_size = len(mz_conjunto)
        for i in range(i_size):
            j_size = len(mz_conjunto[i])
            for j in range(j_size):
                nodo_num = mz_conjunto[i][j]
                if nodo_num ==  num_inicial:
                    i_find_inicial = i
                if nodo_num ==  num_final:
                    i_find_final = i
                if  i_find_inicial != -1 and i_find_final != -1 and i_find_inicial == i_find_final:  
                    #Se hace un ciclo
                    return

        logging.debug("i_find_inicial={i_find_inicial} , i_find_final={i_find_final}".format(i_find_inicial=i_find_inicial, i_find_final=i_find_final))
        #Carga Inicial. No existe en el conjunto
        if i_find_inicial == -1 and i_find_final == -1:  
            mz_conjunto.append([num_inicial, num_final])
            self.ltAristas_KRUSKAL_ARBOL.append(arista)
            return

        #Fusion de conjuntos
        if i_find_inicial > -1 and i_find_final > -1:  
            for nodo_num in mz_conjunto[i_find_final]:
                mz_conjunto[i_find_inicial].append(nodo_num)
            mz_conjunto[i_find_final] = []
            self.ltAristas_KRUSKAL_ARBOL.append(arista)
            return
            
        if i_find_inicial > -1:  
            mz_conjunto[i_find_inicial].append(num_final)
            self.ltAristas_KRUSKAL_ARBOL.append(arista)

        if i_find_final > -1:  
            mz_conjunto[i_find_final].append(num_inicial)
            self.ltAristas_KRUSKAL_ARBOL.append(arista)

    def crearAristasDistancia(self, ltAristas_Param):
        #Asignasion de Sentido de nuevas ARISTAS -> Orden Nodo
        #"""
        for arista in self.ltAristas:
            nodo_inicial = arista.nodo_inicial
            nodo_final = arista.nodo_final
            if nodo_inicial != nodo_final and self.existeAristaNodosOpuestos(nodo_inicial, nodo_final) == False:
                oArista = None
                if nodo_inicial.num < nodo_final.num:
                    oArista = Arista(nodo_inicial = nodo_inicial, nodo_final = nodo_final)
                else:
                    oArista = Arista(nodo_inicial = nodo_final, nodo_final = nodo_inicial) 
                oArista.setDistancia()
                ltAristas_Param.append(oArista)
        #"""
        #Asignasion de Sentido de nuevas ARISTAS -> Orden Camino
        """
        set_orden_nodo = set()
        set_orden_nodo2 = set()
        self.ltNodos.sort(key = self.sortNodo)
        nodo_inicial = self.getNodoInicialConectado()
        self.depthOrdenDijkstra(nodo_inicial, set_orden_nodo, set_orden_nodo2)
        """
                    
    def depthOrdenDijkstra(self, nodo_inicial, set_orden_nodo, set_orden_nodo2):
        ltNodosConect = self.findNodosConectadosNodo(nodo_inicial)
        ltNodosConect.sort(key = self.sortNodo)
        for nodo_conect in ltNodosConect:
            if self.setInOrAdd(set_orden_nodo, str(nodo_inicial.num) + "->" + str(nodo_conect.num)) and self.setInOrAdd(set_orden_nodo, str(nodo_conect.num) + "->" + str(nodo_inicial.num)):
                oArista = self.findArista(nodo_inicial, nodo_conect)
                if oArista is not None and nodo_inicial != nodo_conect and self.existeAristaNodosOpuestos(nodo_inicial, nodo_conect) == False:
                    oAristaNuevo = Arista(nodo_inicial = nodo_inicial, nodo_final = nodo_conect)
                    oAristaNuevo.setDistancia()
                    self.ltAristas_DIJKSTRA.append(oAristaNuevo)
                    self.depthOrdenDijkstra(nodo_conect, set_orden_nodo, set_orden_nodo2)

        #for nodo_conect in ltNodosConect:
        #    if self.setInOrAdd(set_orden_nodo2, str(nodo_inicial.num) + "->" + str(nodo_conect.num)) and self.setInOrAdd(set_orden_nodo2, str(nodo_conect.num) + "->" + str(nodo_inicial.num)):
        #        self.depthOrdenDijkstra(nodo_conect, set_orden_nodo, set_orden_nodo2)



    def setPesosDIJKSTRA(self, nodo_inicial, ltNodoAgregado, set_visitado_nodo):
        logging.debug("->In setPesosDIJKSTRA")#DEBUG
        if nodo_inicial.visitado_DIJKSTRA == True:
            logging.debug("NodoInicial={nodo_inicial}".format(nodo_inicial=nodo_inicial))#DEBUG
            ltNodosConect = self.findNodosConectadosNodoDir(nodo_inicial)
            ltNodosConect.sort(key = self.sortNodo)
            peso_dijkstra_max = sys.maxsize
            arista_menor = None
            for nodo_conect in ltNodosConect:
                logging.debug("NodoConect={nodo_conect}".format(nodo_conect = nodo_conect))#DEBUG
                arista = self.findAristaLt(self.ltAristas_DIJKSTRA, nodo_inicial, nodo_conect)
                if arista is not None :
                    if nodo_inicial in ltNodoAgregado and nodo_conect not in ltNodoAgregado :
                            tp = self.getDijkstraCaminoMenor(arista_menor, arista, peso_dijkstra_max)
                            arista_menor = tp[0]
                            peso_dijkstra_max = tp[1]
                    elif nodo_inicial in ltNodoAgregado and nodo_conect in ltNodoAgregado :
                        if self.setInOrAdd(set_visitado_nodo, nodo_conect):
                            arista_depth = self.setPesosDIJKSTRA(nodo_conect, ltNodoAgregado, set_visitado_nodo)
                            if arista_depth is not None:
                                tp = self.getDijkstraCaminoMenor(arista_menor, arista_depth, peso_dijkstra_max)
                                arista_menor = tp[0]
                                peso_dijkstra_max = tp[1]
            logging.debug("RETURN arista_menor={arista_menor}".format(arista_menor=arista_menor))#DEBUG
            logging.debug("->Out setPesosDIJKSTRA")#DEBUG
            return arista_menor
        return None
    
    def getDijkstraCaminoMenor(self, arista_actual, arista_nueva, peso_dijkstra_max):
        nodo_inicial = arista_nueva.nodo_inicial
        nodo_final = arista_nueva.nodo_final

        distancia = arista_nueva.distancia
        peso_nuevo = nodo_inicial.peso_dijkstra + distancia
        #logging.debug("peso_nuevo={peso_nuevo}".format(peso_nuevo=peso_nuevo))
        if peso_nuevo < peso_dijkstra_max:
            peso_dijkstra_max = peso_nuevo
            logging.debug("AristaNueva={arista_nueva} Peso={peso_nuevo}".format(arista_nueva=arista_nueva, peso_nuevo=peso_nuevo))
            return arista_nueva, peso_dijkstra_max
        return arista_actual, peso_dijkstra_max

    def encontrarGrafo (self, ltAristas, nodo_inicial, set_grafo, str_visitado):
        nodo_inicial[str_visitado] = True
        self.setInOrAdd(set_grafo, nodo_inicial.num)
        ltNodosConect = self.findNodosConectadosNodoLt(nodo_inicial, ltAristas)
        ltNodosConect.sort(key = self.sortNodo)
        for nodo_conect in ltNodosConect:
            if nodo_conect[str_visitado] == False:
                arista = self.findArista(nodo_inicial, nodo_conect)
                if arista is not None :
                    self.encontrarGrafo(ltAristas, nodo_conect, set_grafo, str_visitado)

    def depthDFR_R (self, nodo_inicial, i_color):
        nodo_inicial.visitado_DFS_R = True
        nodo_inicial.color_DFS_R = self.LT_COLOR[(i_color) % len(self.LT_COLOR)]
        ltNodosConect = self.findNodosConectadosNodo(nodo_inicial)
        ltNodosConect.sort(key = self.sortNodo)
        for nodo_conect in ltNodosConect:
            if nodo_conect.visitado_DFS_R == False:
                arista = self.findArista(nodo_inicial, nodo_conect)
                if arista is not None :
                    self.ltAristas_DFS_R.append(arista)
                    self.depthDFR_R(nodo_conect, i_color + 1)

    def depthPrim (self, ltAristas, nodo_inicial, dict_grafo):
        nodo_inicial.visitado_PRIM = True
        ltNodosConect = self.findNodosConectadosNodoLt(nodo_inicial, ltAristas)
        
        if len(ltNodosConect) <= 0:
            return
        ltNodosConect.sort(key = self.sortNodo)
        for nodo_conect in ltNodosConect:
            if nodo_conect.visitado_PRIM == False:
                arista = self.findAristaLt(ltAristas, nodo_inicial, nodo_conect)
                if arista is not None :
                    logging.debug("DISTANCIA={distancia} ".format(distancia=arista.distancia))
                    dict_grafo[arista.distancia] = {"arista":arista, "nodo_conect":nodo_conect}
        logging.debug("DIC={dict_grafo} ".format(dict_grafo=dict_grafo))
    
            

#METODOS Modelado Tipos
    def modeloBase(self, num_i, num_j):
        self.type_node = TYPE_GRAFO.GRAFO_BASE
        self.crearNodos(num = 10)
        
    def modeloMalla(self, param_num_i, param_num_j):
        self.type_node = TYPE_GRAFO.GRAFO_MALLA
        self.crearNodos(num_i = param_num_i, num_j = param_num_j)
        self.crearAristas( num_i = param_num_i, num_j = param_num_j)
        
    def modeloErdosNRenyi(self, num_nodos = None, max_num_aristas = None):
        self.type_node = TYPE_GRAFO.GRAFO_ERDOS_N_RENYI
        self.crearNodos(num_nodos = num_nodos)
        self.crearAristas(num_nodos = num_nodos, max_num_aristas = max_num_aristas)#Aristas >= (num_nodos - 1) + RandomInt(max_num_aristas) ... RandomInt() tiene como Limite(max_num_aristas)
        
    def modeloGilbert(self, num_nodos, probabilidad):
        self.type_node = TYPE_GRAFO.GRAFO_GILBERT
        self.crearNodos(num_nodos = num_nodos)
        self.crearAristas(num_nodos = num_nodos, probabilidad = probabilidad)
        
    def modeloGeografico(self, num_nodos, w_rec, h_rec, prec, r_distancia):
        self.type_node = TYPE_GRAFO.GRAFO_GEOGRAFICO
        self.crearNodos(num_nodos = num_nodos, num_i = w_rec, num_j = h_rec, prec = prec)
        self.crearAristas(num_nodos = num_nodos, r_distancia = r_distancia)
        
    def modeloBarabasiAlbert(self, num_nodos, max_grado):
        self.type_node = TYPE_GRAFO.GRAFO_BARABASI_ALBERT
        self.crearNodos(num_nodos = num_nodos)
        self.crearAristas(num_nodos = num_nodos, max_grado = max_grado)
        
    def modeloDorogovtsevMendes(self, num_nodos):
        self.type_node = TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES
        self.crearNodos(num_nodos = num_nodos)
        self.crearAristas(num_nodos = num_nodos)
        
    def modeloGrafoBFS(self):
        self.ltAristas_BFS = [] 
        self.is_BFS = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_BFS, num_nodos = self.max_random_nodos)
        
    def modeloGrafoDFS_I(self):
        self.ltAristas_DFS_I = [] 
        self.is_DFS_I = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_DFS_I, num_nodos = self.max_random_nodos)
        
    def modeloGrafoDFS_R(self):
        self.ltAristas_DFS_R = [] 
        self.is_DFS_R = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_DFS_R, num_nodos = self.max_random_nodos)
        
    def modeloGrafoDijkstra(self):
        self.is_DIJKSTRA = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_DIJKSTRA)
        
    def modeloGrafoKruskal(self):
        self.is_KRUSKAL = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_KRUSKAL)
        
    def modeloGrafoKruskalInverso(self):
        self.is_KRUSKAL_INVERSO = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_KRUSKAL_INVERSO)
        
    def modeloGrafoPrim(self):
        self.is_PRIM = True
        self.crearAristas(type_node = TYPE_GRAFO.GRAFO_MODELO_PRIM)
        
    def modeloGrafoPygame(self, grafo, is_BASE = False, is_BFS = False, is_DFS_R = False, is_DFS_I = False, is_DIJKSTRA = False, is_KRUSKAL = False, is_KRUSKAL_INVERSO = False, is_PRIM = False):
        ltAristas = []
        title = "None"
        if grafo.type_node == TYPE_GRAFO.GRAFO_BASE:
            title = "GRAFO_BASE"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_ERDOS_N_RENYI :
            title = "GRAFO_ERDOS_N_RENYI"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_GILBERT :
            title = "GRAFO_GILBERT"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO:
            title = "GRAFO_GEOGRAFICO"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_BARABASI_ALBERT:
            title = "GRAFO_BARABASI_ALBERT"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES:
            title = "GRAFO_DOROGOVTSEV_MENDES"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_MALLA:
            title = "GRAFO_MALLA"

        if is_BASE:
            ltAristas = self.ltAristas
        elif is_BFS:
            ltAristas = self.ltAristas_BFS
            title = title + "_BFS"
        elif is_DFS_R:
            ltAristas = self.ltAristas_DFS_R
            title = title + "_DFS_R"
        elif is_DFS_I:
            ltAristas = self.ltAristas_DFS_I
            title = title + "_DFS_I"
        elif is_DIJKSTRA:
            ltAristas = self.ltAristas_DIJKSTRA
            title = title + "_DIJSKTRA"
        elif is_KRUSKAL:
            ltAristas = self.ltAristas_KRUSKAL_ARBOL
            title = title + "_KRUSKA"
        elif is_KRUSKAL_INVERSO:
            ltAristas = self.ltAristas_KRUSKAL_ARBOL_INVERSO
            title = title + "_KRUSKA_INVERSO"
        elif is_PRIM:
            ltAristas = self.ltAristas_PRIM_ARBOL
            title = title + "_PRIM"
        if len(ltAristas) > 0:
            pygame_start(grafo, ltAristas, title)
        
    def modeloGrafoPygame_QuadTree(self, grafo, is_BASE = False, is_BFS = False, is_DFS_R = False, is_DFS_I = False, is_DIJKSTRA = False, is_KRUSKAL = False, is_KRUSKAL_INVERSO = False, is_PRIM = False):
        ltAristas = []
        title = "None"
        if grafo.type_node == TYPE_GRAFO.GRAFO_BASE:
            title = "GRAFO_BASE"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_ERDOS_N_RENYI :
            title = "GRAFO_ERDOS_N_RENYI"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_GILBERT :
            title = "GRAFO_GILBERT"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO:
            title = "GRAFO_GEOGRAFICO"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_BARABASI_ALBERT:
            title = "GRAFO_BARABASI_ALBERT"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES:
            title = "GRAFO_DOROGOVTSEV_MENDES"
        elif grafo.type_node == TYPE_GRAFO.GRAFO_MALLA:
            title = "GRAFO_MALLA"

        if is_BASE:
            ltAristas = self.ltAristas
        elif is_BFS:
            ltAristas = self.ltAristas_BFS
            title = title + "_BFS"
        elif is_DFS_R:
            ltAristas = self.ltAristas_DFS_R
            title = title + "_DFS_R"
        elif is_DFS_I:
            ltAristas = self.ltAristas_DFS_I
            title = title + "_DFS_I"
        elif is_DIJKSTRA:
            ltAristas = self.ltAristas_DIJKSTRA
            title = title + "_DIJSKTRA"
        elif is_KRUSKAL:
            ltAristas = self.ltAristas_KRUSKAL_ARBOL
            title = title + "_KRUSKA"
        elif is_KRUSKAL_INVERSO:
            ltAristas = self.ltAristas_KRUSKAL_ARBOL_INVERSO
            title = title + "_KRUSKA_INVERSO"
        elif is_PRIM:
            ltAristas = self.ltAristas_PRIM_ARBOL
            title = title + "_PRIM"
        if len(ltAristas) > 0:
            pygame_start_QuadTree(grafo, ltAristas, "QuadTree_" +title)
            
#METODOS Impresion
    def printGrafo(self, nameFile):
        prefix_name = ""
        if self.type_node == TYPE_GRAFO.GRAFO_BASE:
            prefix_name = "BASE_"
        elif self.type_node == TYPE_GRAFO.GRAFO_MALLA:
            prefix_name = "MALLA_"
        elif self.type_node == TYPE_GRAFO.GRAFO_ERDOS_N_RENYI:
            prefix_name = "ERDOS_N_RENYI_"
        elif self.type_node == TYPE_GRAFO.GRAFO_GILBERT:
            prefix_name = "GILBERT_"
        elif self.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO:
            prefix_name = "GEOGRAFICO_"
        elif self.type_node == TYPE_GRAFO.GRAFO_BARABASI_ALBERT:
            prefix_name = "BARABASI_ALBERT_"
        elif self.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES:
            prefix_name = "DOROGOVTSEV_MENDES_"
            
        prefix_BFS = "BFS_"
        prefix_DFS_I = "DFS_I_"
        prefix_DFS_R = "DFS_R_"
        prefix_DIJKSTRA = "DIJKSTRA_"
        prefix_KRUSKAL = "KRUSKAL_"
        prefix_KRUSKAL_INVERSO = "KRUSKAL_INVERSO_"
        prefix_PRIM = "PRIM_"

        timestamp = ""
        #f = open(os.path.join(pathlib.Path().absolute(),  "Output\\" + nameFile + timestamp + ".gv"), "w")
        f = open("Output\\" + prefix_name + nameFile + timestamp + ".gv", "w")
        f.write("graph {\n")
        self.printNodos(f)
        self.printAristasGenerico(f, self.ltAristas)
        f.write("}")
        f.close()

        if self.is_BFS:
            f = open("Output\\" + prefix_name + prefix_BFS + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            self.printNodosColor(f, TYPE_GRAFO.GRAFO_MODELO_BFS)
            self.printAristasGenerico(f, self.ltAristas_BFS)
            f.write("}")
            f.close()

        if self.is_DFS_I:
            f = open("Output\\" + prefix_name + prefix_DFS_I + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            self.printNodosColor(f, TYPE_GRAFO.GRAFO_MODELO_DFS_I)
            self.printAristasGenerico(f, self.ltAristas_DFS_I)
            f.write("}")
            f.close()

        if self.is_DFS_R:
            f = open("Output\\" + prefix_name + prefix_DFS_R + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            self.printNodosColor(f, TYPE_GRAFO.GRAFO_MODELO_DFS_R)
            self.printAristasGenerico(f, self.ltAristas_DFS_R)
            f.write("}")
            f.close()

        if self.is_DIJKSTRA:
            f = open("Output\\" + prefix_name + prefix_DIJKSTRA + nameFile + timestamp + ".gv", "w")
            f.write("digraph {\n")
            self.printNodosColor(f, TYPE_GRAFO.GRAFO_MODELO_DFS_R, is_dijkstra = True)
            self.printAristasGenerico(f, self.ltAristas_DIJKSTRA, es_dir = True)
            f.write("}")
            f.close()

        if self.is_KRUSKAL or self.is_KRUSKAL_INVERSO or self.is_PRIM:
            f = open("Output\\" + prefix_name + prefix_KRUSKAL + "ORIGEN_" + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            self.printNodos(f)
            self.printAristasGenerico(f, self.ltAristas_KRUSKAL, no_es_dir = True)
            f.write("}")
            f.close()
        
        if self.is_KRUSKAL:
            f = open("Output\\" + prefix_name + prefix_KRUSKAL + "ARBOL_" + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            f.write("nodo_peso [label=<" + self.nodo_kruskal.name + "> color=\"blue\"];\n")
            self.printNodos(f)
            self.printAristasGenerico(f, self.ltAristas_KRUSKAL_ARBOL, no_es_dir = True)
            f.write("}")
            f.close()
        
        if self.is_KRUSKAL_INVERSO:
            f = open("Output\\" + prefix_name + prefix_KRUSKAL_INVERSO + "ARBOL_" + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            f.write("nodo_peso [label=<" + self.nodo_kruskal_inverso.name + "> color=\"blue\"];\n")
            self.printNodos(f)
            self.printAristasGenerico(f, self.ltAristas_KRUSKAL_ARBOL_INVERSO, no_es_dir = True)
            f.write("}")
            f.close()
        
        if self.is_PRIM:
            f = open("Output\\" + prefix_name + prefix_PRIM + "ARBOL_" + nameFile + timestamp + ".gv", "w")
            f.write("graph {\n")
            f.write("nodo_peso [label=<" + self.nodo_prim.name + "> color=\"blue\"];\n")
            self.printNodos(f)
            self.printAristasGenerico(f, self.ltAristas_PRIM_ARBOL, no_es_dir = True)
            f.write("}")
            f.close()

        
    def printNodos(self, f):
        if (self.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO
            or self.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES):
            for nodo in self.ltNodos:
                f.write(nodo.getLabel() + "[pos=\"" + str(nodo.num_i) + "," + str(nodo.num_j) +"!\"];\n")
        else:
            for nodo in self.ltNodos:
                f.write(nodo.getLabel() + ";\n")

    def printNodosColor(self, f, type_node, is_dijkstra = False):
        if self.type_node == TYPE_GRAFO.GRAFO_GEOGRAFICO or self.type_node == TYPE_GRAFO.GRAFO_DOROGOVTSEV_MENDES:
            for nodo in self.ltNodos:
                if(is_dijkstra):
                    f.write(nodo.getLabel() + "[label=<" + nodo.getLabel() + "<br/>Peso:" + str("MAX" if nodo.peso_dijkstra == sys.maxsize else nodo.peso_dijkstra) 
                    + "> pos=\"" + str(nodo.num_i) + "," + str(nodo.num_j) +"!\" color=\"" + self.getNodoColor(nodo, type_node) + "\"];\n")
                else:
                    f.write(nodo.getLabel() + "[pos=\"" + str(nodo.num_i) + "," + str(nodo.num_j) +"!\" color=\"" + self.getNodoColor(nodo, type_node) + "\"];\n")
        else:
            for nodo in self.ltNodos:
                if(is_dijkstra):
                    f.write(nodo.getLabel() + "[label=<" + nodo.getLabel() + "<br/>Peso:" + str("MAX" if nodo.peso_dijkstra == sys.maxsize else nodo.peso_dijkstra) + "> color=\"" + self.getNodoColor(nodo, type_node) + "\"];\n")
                else:
                    f.write(nodo.getLabel() + "[color=\"" + self.getNodoColor(nodo, type_node) + "\"];\n")
        
    def getNodoColor(self, nodo, type_node):
        if type_node == TYPE_GRAFO.GRAFO_MODELO_BFS:
            return nodo.color_BFS
        elif type_node == TYPE_GRAFO.GRAFO_MODELO_DFS_I:
            return nodo.color_DFS_I
        elif type_node == TYPE_GRAFO.GRAFO_MODELO_DFS_R:
            return nodo.color_DFS_R


    def printAristasGenerico(self, f, ltAristas, es_dir = False, no_es_dir = False):
        for arista in ltAristas:
            #print(arista)
            if(es_dir):
                f.write(arista.nodo_inicial.getLabel() + " -> " + arista.nodo_final.getLabel() +  "[label=\"" + str(arista.distancia) + "\"];\n")
            elif(no_es_dir):
                f.write(arista.nodo_inicial.getLabel() + " -- " + arista.nodo_final.getLabel() +  "[label=\"" + str(arista.distancia) + "\"];\n")
            else:
                f.write(arista.nodo_inicial.getLabel() + "--" + arista.nodo_final.getLabel() + ";\n")

#METODOS Apoyo
    def findNodoMalla(self, num_i, num_j):
        for nodo in self.ltNodos:
            if nodo.num_i == num_i and nodo.num_j == num_j:
                return nodo
    
    def findNodo(self, num):
        for nodo in self.ltNodos:
            if nodo.num == num:
                #print(str(num) + ":" + nodo.getLabel())
                return nodo
    
    def getNodoInicialConectado(self):
        for nodo_inicial in self.ltNodos:
            ltCapaTmp = self.findNodosConectadosNodo(nodo_inicial)#Capa0
            if len(ltCapaTmp) > 0:
                return nodo_inicial
    
    def findNodosConectadosNodo(self, nodo):
        ltNodosFinal = []
        for arista in self.ltAristas:
            o_nodo_inicial = arista.nodo_inicial
            o_nodo_final = arista.nodo_final
            if o_nodo_inicial.num == nodo.num and o_nodo_inicial.num != o_nodo_final.num:
                ltNodosFinal.append(o_nodo_final)
            elif o_nodo_final.num == nodo.num  and o_nodo_inicial.num != o_nodo_final.num:
                ltNodosFinal.append(o_nodo_inicial)
        return ltNodosFinal
    
    def findNodosConectadosNodoLt(self, nodo, ltAristas):
        ltNodosFinal = []
        for arista in ltAristas:
            o_nodo_inicial = arista.nodo_inicial
            o_nodo_final = arista.nodo_final
            if o_nodo_inicial.num == nodo.num and o_nodo_inicial.num != o_nodo_final.num:
                ltNodosFinal.append(o_nodo_final)
            elif o_nodo_final.num == nodo.num  and o_nodo_inicial.num != o_nodo_final.num:
                ltNodosFinal.append(o_nodo_inicial)
        return ltNodosFinal
    
    def findNodosConectadosNodoDir(self, nodo):
        ltNodosFinal = []
        for arista in self.ltAristas_DIJKSTRA:
            o_nodo_inicial = arista.nodo_inicial
            o_nodo_final = arista.nodo_final
            if o_nodo_inicial.num == nodo.num and o_nodo_inicial.num != o_nodo_final.num:
                ltNodosFinal.append(o_nodo_final)
        return ltNodosFinal
    
    def findArista(self, nodo_inicial: Nodo, nodo_final: Nodo):
        ltNodosFinal = []
        for arista in self.ltAristas:
            o_nodo_inicial = arista.nodo_inicial
            o_nodo_final = arista.nodo_final
            if (o_nodo_inicial.num == nodo_inicial.num and o_nodo_final.num == nodo_final.num) or (o_nodo_final.num == nodo_inicial.num and o_nodo_inicial.num == nodo_final.num):
                return arista
    
    def findAristaLt(self, ltAristas: list, nodo_inicial: Nodo, nodo_final: Nodo):
        ltNodosFinal = []
        for arista in ltAristas:
            o_nodo_inicial = arista.nodo_inicial
            o_nodo_final = arista.nodo_final
            if (o_nodo_inicial.num == nodo_inicial.num and o_nodo_final.num == nodo_final.num) or (o_nodo_final.num == nodo_inicial.num and o_nodo_inicial.num == nodo_final.num):
                return arista

    def findNodoGeografico(self, r_distancia):
        ltNodosDistancia = []
        for nodo_inicial in self.ltNodos:
            for nodo_final in self.ltNodos:
                dist = math.sqrt(pow(nodo_final.num_i - nodo_inicial.num_i,2) + pow(nodo_final.num_j - nodo_inicial.num_j,2))
                if dist <= r_distancia and nodo_inicial.num != nodo_final.num:
                    return ltNodosDistancia

    #Buscar NODOS anteriores y en capa actuales
    def findNodoEnCapas(self, ltCapaNueva, ltCapasActutales):
        ltCapaNuevaFinal = []
        for nodo_nuevo in ltCapaNueva:
            agregar = True
            for ltNodosActuales in ltCapasActutales:
                for nodo_actual in ltNodosActuales:
                    if nodo_actual.num == nodo_nuevo.num:
                        agregar = False
                        break
            for nodo_actual_capa in ltCapaNuevaFinal:
                if nodo_actual_capa.num == nodo_nuevo.num:
                    agregar = False
                    break
            if agregar:
                ltCapaNuevaFinal.append(nodo_nuevo)
        return ltCapaNuevaFinal

    def filterNodoFinal(self, ltCapaNueva):
        ltCapaNuevaFinal = []
        for nodo_nuevo in ltCapaNueva:
            agregar = True
            for nodo_actual_capa in ltCapaNuevaFinal:
                if nodo_actual_capa.num == nodo_nuevo.num:
                    agregar = False
                    break
            if agregar:
                ltCapaNuevaFinal.append(nodo_nuevo)
        return ltCapaNuevaFinal
    
    def existeAristaNodosOpuestos(self, nodo_inicial, nodo_final):#Solamente si es DIRIGIDO
        return str(nodo_final.num) + "_" + str(nodo_inicial.num) in self.set_aristas

    def appendArista(self, nodo_inicial, nodo_final):
        if self.es_dirigido:
            if self.existeAristaNodosOpuestos(nodo_inicial, nodo_final) == False:
                self.ltAristas.append(Arista(nodo_inicial = nodo_inicial, nodo_final = nodo_final))
                self.setInOrAdd(self.set_aristas, str(nodo_inicial.num) + "_" + str(nodo_final.num))
                #print(str(len(self.set_aristas)))#DEBUG
        else:
            self.ltAristas.append(Arista(nodo_inicial = nodo_inicial, nodo_final = nodo_final))

    def setInOrAdd(self, o_set, str_key):
        return not(str_key in o_set or o_set.add(str_key))

    def deleteAristas(self, num_nodo_inicial, num_nodo_final):
        ltDelAristas = []
        for arista in self.ltAristas:
            if arista.nodo_inicial.num == num_nodo_inicial and arista.nodo_final.num == num_nodo_final:
                ltDelAristas.append(arista)
        for delArista in ltDelAristas:
            self.ltAristas.remove(delArista)
            
    def getSizeNodos(self):
        return len(self.ltNodos)
            
    def getSizeAristas(self):
        return len(self.ltAristas)

    def sortNodo(self, nodo):
        return nodo.num

    def sortAristaPeso(self, arista:Arista):
        return arista.distancia
#METODOS Apoyo DEBUG
    def printCapa(self):
        ltNodos = self.ltCapas[len(self.ltCapas)-1]
        for nodo in ltNodos:
            print(nodo)

class GRAFO_GUI:
    REFRESH = 20
    COUNT_PRINT = 100
    SIZE_SCREEN = 800, 800
    BGCOLOR = (255,255,255)
    NODECOLOR = (204,0,255)
    RADIUS_SIZE = 3
    GRIDSPACING = 50
    PADDING_QUADTREE = SIZE_SCREEN[0]/2,SIZE_SCREEN[1]/2

class AristaGUI(object):
    def __init__(self, nodo_inicial_gui, nodo_final_gui):
        self.nodo_inicial_gui = nodo_inicial_gui
        self.nodo_final_gui = nodo_final_gui

class NodoGUI(object):
    
    def __init__(self, id, name):
        #print("ID: {id}".format(id=id))#Debug
        self.id = id
        self.name = name
        self.pygame_rect = None
        self.color = GRAFO_GUI.NODECOLOR
 
    def setpos(self, pos, graph = None):
        if self.pygame_rect and graph:
            graph.dict_nodos.pop(pos, None)
        self.pygame_rect = pygame.Vector2(pos[0], pos[1])
        if graph:
            graph.dict_nodos[pos] = self
 
    def  __hash__(self):
        return self.id
 
def pygame_crearGrafoSpring(grafo, ltAristas):
    grafoGUI = GrafoGUI()
    dic_add_nodos = grafoGUI.dic_add_nodos
    for oArista in ltAristas:
        #print(oArista)#Debug
        nodo_inicial = oArista.nodo_inicial
        nodo_final = oArista.nodo_final
        num_inicial = nodo_inicial.num
        num_final = nodo_final.num
        if not num_inicial in dic_add_nodos:
            node = NodoGUI(id=num_inicial, name=nodo_inicial.name)
            dic_add_nodos[num_inicial] = node
            grafoGUI.addNodo(node)
        if not num_final in dic_add_nodos:
            node = NodoGUI(id=num_final, name=nodo_final.name)
            dic_add_nodos[num_final] = node
            #print("NameIncial:{p1} NameFinal:{p2} ".format(p1=node.name,p2=dic_add_nodos[num_final].name))#Debug
            grafoGUI.addNodo(node)
        
        grafoGUI.addArista(dic_add_nodos[num_inicial], dic_add_nodos[num_final])
    #print("Dict:{p1}".format(p1=dic_add_nodos))#Debug
    return grafoGUI

class GrafoGUI():

    CONSTANT_FR = 27.01
    CONSTANT_C1 = 15
    CONSTANT_C2 = 200

    def __init__(self):
        self.set_nodos = set()
        self.set_arista = set()
        self.dict_nodos = dict()
        self.dic_add_nodos = dict()
        self.print_nodos = True
        self.print_aristas = True
        self.print_distancia = True
        self.count_print = 0
 
    def addNodo(self, node, is_FR = False):
        not_add =  True
        while not_add:
            #x, y = (randrange(0, GRAFO_GUI.SIZE_SCREEN[0]), randrange(0, GRAFO_GUI.SIZE_SCREEN[1]))
            if is_FR:
                x, y = (randrange(-GRAFO_GUI.SIZE_SCREEN[0]/2, GRAFO_GUI.SIZE_SCREEN[0]/2), randrange(-GRAFO_GUI.SIZE_SCREEN[1]/2, GRAFO_GUI.SIZE_SCREEN[1]/2))
            else:
                x, y = (randrange(0, GRAFO_GUI.SIZE_SCREEN[0]), randrange(0, GRAFO_GUI.SIZE_SCREEN[1]))
            if not (x,y) in self.dict_nodos:
                self.set_nodos.add(node)
                node.setpos((x,y), self)
                not_add = False

    def addArista(self, nodo_inicial_gui, nodo_final_gui):
        #if num_inicial != num_final:
            #print("NodoIncial:{p1} NodoFinal:{p2} ".format(p1=num_inicial,p2=num_final))#Debug
        self.set_arista.add(AristaGUI(nodo_inicial_gui, nodo_final_gui))

    def calcularDistancia(self):

        SCREEN.fill(GRAFO_GUI.BGCOLOR)
        K = self.CONSTANT_FR * math.sqrt((GRAFO_GUI.SIZE_SCREEN[0]* GRAFO_GUI.SIZE_SCREEN[1])/len(self.set_arista))
        for oArista in self.set_arista:
            nodo_inicial_gui = oArista.nodo_inicial_gui
            nodo_final_gui = oArista.nodo_final_gui
            pos_nodo_inicial_gui = nodo_inicial_gui.pygame_rect
            pos_nodo_final_gui = nodo_final_gui.pygame_rect
            pos_x_inicial = pos_nodo_inicial_gui[0]
            pos_y_inicial = pos_nodo_inicial_gui[1]
            pos_x_final = pos_nodo_final_gui[0]
            pos_y_final = pos_nodo_final_gui[1]
            distancia = math.sqrt((pos_x_inicial - pos_x_final)**2 + (pos_y_inicial - pos_y_final)**2)
            fSpring = self.CONSTANT_C1 * log(distancia/self.CONSTANT_C2)
            angle = 0
            x = GRAFO_GUI.SIZE_SCREEN[0] / 2
            y = GRAFO_GUI.SIZE_SCREEN[1] / 2
            print("MitadX:{p1}\MitadY:{p2}".format(p1=x,p2=y))#Debug

            print("PosIncial:{p1}\tPosFinal:{p2}\tDistancia:{p3}\tfSpring:{p4}\t".format(p1=pos_nodo_inicial_gui,p2=pos_nodo_final_gui,p3=distancia,p4=fSpring), end='')#Debug
            if pos_x_final < x and pos_y_final < y:
                print("Vector1\t", end='')#Debug
                angle = 225            
            elif pos_x_final > x and pos_y_final < y:
                print("Vector2\t", end='')#Debug
                angle = 135
            elif pos_x_final > x and pos_y_final > y:
                print("Vector3\t", end='')#Debug
                angle = 45
            elif pos_x_final < x and pos_y_final > y:
                print("Vector4\t", end='')#Debug
                angle = 315            
            

            new_pos = (pos_x_inicial, pos_y_inicial ) + pygame.Vector2(fSpring, 0).rotate(angle)
            print("new_pos:{new_pos}".format(new_pos=new_pos))#Debug
            fA = (distancia ** 2) / K
            fR = (K ** 2) / distancia
            #print("vec: {p1}".format(p1=vec))
            #print("Nodo:{p1} React:{p2} ".format(p1=node.id,p2=node.pygame_rect))
            #pygame.draw.circle(SCREEN, GRAFO_GUI.BGCOLOR, nodo_final_gui.pygame_rect, GRAFO_GUI.RADIUS_SIZE)
            #pygame.draw.line(SCREEN, GRAFO_GUI.BGCOLOR, nodo_inicial_gui.pygame_rect, nodo_final_gui.pygame_rect)
            
            SCREEN.fill(GRAFO_GUI.BGCOLOR)
            nodo_final_gui.setpos((new_pos[0],new_pos[1]), self)
            for node in self.set_nodos:
                pygame.draw.circle(SCREEN, node.color, node.pygame_rect, GRAFO_GUI.RADIUS_SIZE)
            for arista in self.set_arista:
                pygame.draw.line(SCREEN, GRAFO_GUI.NODECOLOR, arista.nodo_inicial_gui.pygame_rect, arista.nodo_final_gui.pygame_rect)
            pygame.display.flip()
            pygame.time.delay(GRAFO_GUI.REFRESH)
            #print("PosIncial:{p1} PosFinal:{p2} Distancia:{p3} fA:{p4} fR:{p5}".format(p1=pos_nodo_inicial_gui,p2=pos_nodo_final_gui,p3=distancia,p4=fA,p5=fR))#Debug
    

    def formulaRepulsion(self, quad, searchPoint) :
        #print("-> " + str(quad))
        if len(quad.points) == 0:
            return
        num_V = len(quad.points)
        #K = .6 * math.sqrt((GRAFO_GUI.SIZE_SCREEN[0]*GRAFO_GUI.SIZE_SCREEN[1])/num_V)
        K = .6 * math.sqrt((GRAFO_GUI.SIZE_SCREEN[0]*GRAFO_GUI.SIZE_SCREEN[1])/num_V)
        distance = quad.distanceFromCentroide(searchPoint)
        if distance == 0:
            return
        x_centroide, y_centroide = quad.pointFromCentroide()
        fRepulsion = ((K * K) / distance)
        angle = quad.angle_between((searchPoint.x, searchPoint.y), ( x_centroide, y_centroide))
        #print("Punto x:{x1} y:{y1} Centroide x:{x} y:{y}".format(x1=searchPoint.x, y1=searchPoint.y,x=x_centroide,y= y_centroide))
        #print("FormulaRepulsion:{fRepulsion}, K:{K}, distance={distance}, num_V={num_V}, angle={angle}".format(num_V=num_V, fRepulsion=fRepulsion,distance=distance,K=K, angle=angle))
        #print((x_centroide, y_centroide )  + pygame.Vector2(fRepulsion, 0).rotate(angle))
        for nodo in self.set_nodos:
            if (nodo.pygame_rect[0], nodo.pygame_rect[1]) == (searchPoint.x, searchPoint.y):
                #print("FIND")
                nodo.pygame_rect[0], nodo.pygame_rect[1] = ((x_centroide, y_centroide )  + pygame.Vector2(fRepulsion, 0).rotate(angle))
                nodo.pygame_rect[0], nodo.pygame_rect[1] = nodo.pygame_rect[0] % GRAFO_GUI.PADDING_QUADTREE[0], nodo.pygame_rect[1] % GRAFO_GUI.PADDING_QUADTREE[0]
        #searchPoint.x = searchPoint.x + fRepulsion
        #searchPoint.y = searchPoint.y + fRepulsion
        for childQuad in quad.children():
            self.formulaRepulsion(childQuad, searchPoint)


class Point():
    def __init__(self, x, y, data=None) :
        self.x = x
        self.y = y
        self.userData = data

    def distanceFrom(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt((dx * dx) + (dy * dy))

    def __str__(self):
        return "Point:{{x: {x}, y: {y}}}".format(x=self.x,y=self.y)
        
class Rectangle():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = x - w / 2
        self.right = x + w / 2
        self.top = y - h / 2
        self.bottom = y + h / 2
        self.cuadrante = ""

    def contains(self, point):
        return self.left <= point.x and point.x <= self.right and self.top <= point.y and point.y <= self.bottom
    

    def intersects(self, range):
        return not(self.right < range.left or range.right < self.left or self.bottom < range.top or range.bottom < self.top)

    def subdivide(self, quadrant):
        self.cuadrante = quadrant
        if quadrant== 'ne':
            return Rectangle(self.x + self.w / 4, self.y - self.h / 4, self.w / 2, self.h / 2)
        elif quadrant== 'nw':
            return Rectangle(self.x - self.w / 4, self.y - self.h / 4, self.w / 2, self.h / 2)
        elif quadrant==  'se':
            return Rectangle(self.x + self.w / 4, self.y + self.h / 4, self.w / 2, self.h / 2)
        elif quadrant==  'sw':
            return Rectangle(self.x - self.w / 4, self.y + self.h / 4, self.w / 2, self.h / 2)
    #Distancia al Quad mas cercano
    def xDistanceFrom(self, point):
        if (self.left <= point.x and point.x <= self.right):
            return 0
        return min(abs(point.x - self.left), abs(point.x - self.right))
    #Distancia al Quad mas cercano
    def yDistanceFrom(self, point):
        if (self.top <= point.y and point.y <= self.bottom):
            return 0
        return min(abs(point.y - self.top), abs(point.y - self.bottom))
    

    def distanceFrom(self, point):
        dx = self.xDistanceFrom(point)
        dy = self.yDistanceFrom(point)
        #print("{rectangle}, point:{point} dx:{dx} dy:{dy} ".format(rectangle=self,point=point,dx=dx,dy=dy))
        return math.sqrt((dx * dx) + (dy * dy))

    def __str__(self):
        return "Rectangle:{{cuadrante: {cuadrante}, left: {left}, right: {right}, top: {top}, bottom: {bottom}}}".format(cuadrante=self.cuadrante,left=self.left,right=self.right,top=self.top,bottom=self.bottom)

class QuadTree():

    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
    
    def children(self) :
        if (self.divided):
            return [self.northeast, self.northwest, self.southeast, self.southwest]
        else:
            return []

    def subdivide(self): 
        self.northeast = QuadTree(self.boundary.subdivide('ne'), self.capacity)
        self.northwest = QuadTree(self.boundary.subdivide('nw'), self.capacity)
        self.southeast = QuadTree(self.boundary.subdivide('se'), self.capacity)
        self.southwest = QuadTree(self.boundary.subdivide('sw'), self.capacity)
        self.divided = True
    
    def pointFromCentroide(self): 
        #print("distanceFromCentroide")
        x = 0
        y = 0
        count = 0
        for pt in self.points:
            x = x + pt.x
            y = y + pt.y
            count = count + 1
        #print("Point dx:{dx} dy:{dy} ".format(dx=x,dy=y))
        if(count > 0):
            x = x / count
            y = y / count
            #print("Return dx:{dx} dy:{dy} ".format(dx=x,dy=y))
            return x, y
        else:
            return None, None

    def distanceFromCentroide(self, point): 
        #print("distanceFromCentroide")
        x, y = self.pointFromCentroide()
        if x is None or y is None:
            return sys.maxsize
        else:
            x = point.x - x
            y = point.y - y
            return math.sqrt((x * x) + (y * y))

    def insert(self, point):
        if (not(self.boundary.contains(point))):
            #print("False point:{point}".format(point=point))
            return False

        if (len(self.points) < self.capacity):
            self.points.append(point)
            #print("True point:{point}".format(point=point))
            return True

        if (not(self.divided)):
            #print("Subdivide point:{point}".format(point=point))
            self.subdivide()

        return (self.northeast.insert(point) or self.northwest.insert(point) or self.southeast.insert(point) or self.southwest.insert(point))

    def query(self, range, found):
        if (not found):
            found = []

        if (not range.intersects(self.boundary)):
            return found

        for p in self.points:
            if (range.contains(p)):
                found.append(p)

        if (self.divided):
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)

        return found

    """
    def closest(self, searchPoint, maxEncontrar = 1, maxDistance = sys.maxsize) :
        return self.kNearest(searchPoint, maxEncontrar, maxDistance, 0, 0)["found"]

    def kNearest(self, searchPoint, maxEncontrar, maxDistance, furthestDistance, encontradosAhora) :
        print("maxDistance:{maxDistance}".format(maxDistance=maxDistance))
        found = []
        ltChild = []
        return_dict = dict()
        return_dict["found"] = []
        return_dict["furthestDistance"] = 0
        #Se ordena por cuadrante mas cercano
        #ltQuads = sorted(self.children(), key=cmp_to_key(lambda a, b: a.boundary.distanceFrom(searchPoint) - b.boundary.distanceFrom(searchPoint)))
        print("Sort->")
        ltQuads = sorted(self.children(), key=cmp_to_key(lambda a, b: a.distanceFromCentroide(searchPoint) - b.distanceFromCentroide(searchPoint)))
        print("<-Sort")
        #Se obtienen los nodos de los cuadrantes mas cercanos. Eficiente
        for childQuad in ltQuads:
            distance = childQuad.distanceFromCentroide(searchPoint)
            print("DistanceCentroid:{distance} ".format(distance=distance))
            if (distance > maxDistance):
                continue
            elif (encontradosAhora < maxEncontrar or distance < furthestDistance):
                result = childQuad.kNearest(searchPoint, maxEncontrar, maxDistance, furthestDistance, encontradosAhora)
                if not(result is None):
                    childPoints = result["found"]
                    for ch in childPoints:
                        found.append(ch)
                    encontradosAhora = encontradosAhora + len(childPoints)
                    furthestDistance = result["furthestDistance"]
        #Se ordenan los puntos 
        ltPoints = sorted(self.points, key=cmp_to_key(lambda a, b: a.distanceFrom(searchPoint) - b.distanceFrom(searchPoint)))
        for p in ltPoints:
            distance = p.distanceFrom(searchPoint)
            if (distance > maxDistance):
                continue
            elif (encontradosAhora < maxEncontrar or distance < furthestDistance) :
                found.append(p)
                furthestDistance = max(distance, furthestDistance)
                encontradosAhora = encontradosAhora + 1
        ltPointsFound = sorted(found, key=cmp_to_key(lambda a, b: a.distanceFrom(searchPoint) - b.distanceFrom(searchPoint)))
        return_dict["found"] = ltPointsFound[0:maxEncontrar]
        return_dict["furthestDistance"] = furthestDistance
        return return_dict
    """
       
    def angle_between(self, p1, p2):
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        return (np.rad2deg((ang1 - ang2) % (2 * np.pi))) 

    def forEach(self, fn):
        self.points.forEach(fn)
        if (self.divided):
            self.northeast.forEach(fn)
            self.northwest.forEach(fn)
            self.southeast.forEach(fn)
            self.southwest.forEach(fn)

    def merge(self, other, capacity) :
        left = min(self.boundary.left, other.boundary.left)
        right = max(self.boundary.right, other.boundary.right)
        top = min(self.boundary.top, other.boundary.top)
        bottom = max(self.boundary.bottom, other.boundary.bottom)
        height = bottom - top
        width = right - left
        midX = left + width / 2
        midY = top + height / 2
        boundary = Rectangle(midX, midY, width, height)
        result = QuadTree(boundary, capacity)
        #self.forEach(point => result.insert(point))
        #other.forEach(point => result.insert(point))
        self.forEach(result.insert(point))
        other.forEach(result.insert(point))

        return result

    def length(self):
        count = len(self.points)
        if (self.divided):
            count += len(self.northwest)
            count += len(self.northeast)
            count += len(self.southwest)
            count += len(self.southeast)
        return count
 
    def __str__(self):
        return "QuadTree:{{Boundary: {boundary}, Capacity: {capacity}, Points: {points}, 1-Northeast: {northeast}, 1-Northwest: {northwest}, 1-Southeast: {southeast}, 1-Southwest: {southwest}}}".format(boundary=self.boundary,capacity=self.capacity,points=','.join(str(x) for x in self.points),northeast=self.northeast,northwest= self.northwest,southeast= self.southeast,southwest= self.southwest)
 
def pygame_init():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(GRAFO_GUI.SIZE_SCREEN)
 
def pygame_quit():
    pygame.quit()
 
def pygame_start(grafo, ltAristas, title):
    grafoGUI = pygame_crearGrafoSpring(grafo, ltAristas)
    pygame_init()
    pygame.display.set_caption(title)
    SCREEN.fill(GRAFO_GUI.BGCOLOR)
    while True:
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break
        if grafoGUI.print_nodos:
            for node in grafoGUI.set_nodos:
                #print("Nodo:{p1} React:{p2} ".format(p1=node.id,p2=node.pygame_rect))
                pygame.draw.circle(SCREEN, node.color, node.pygame_rect, GRAFO_GUI.RADIUS_SIZE)
                pygame.display.flip()
                pygame.time.delay(GRAFO_GUI.REFRESH)
            grafoGUI.print_nodos = False
        #grafoGUI.update()
        if grafoGUI.print_aristas:
            for arista in grafoGUI.set_arista:
                #print("NodoIncial:{p1} NodoFinal:{p2} ".format(p1=arista.nodo_inicial_gui.id,p2=arista.nodo_final_gui.id))
                pygame.draw.line(SCREEN, GRAFO_GUI.NODECOLOR, arista.nodo_inicial_gui.pygame_rect, arista.nodo_final_gui.pygame_rect)
                pygame.display.flip()
                pygame.time.delay(GRAFO_GUI.REFRESH)
            grafoGUI.print_aristas = False
        if grafoGUI.print_distancia:
            grafoGUI.calcularDistancia()
            grafoGUI.print_distancia = False
        #Cuando se traba
        pygame.display.flip()


def pygame_crearGrafoQuadTree(grafo, ltAristas):
    grafoGUI = GrafoGUI()
    dic_add_nodos = grafoGUI.dic_add_nodos
    for oArista in ltAristas:
        #print(oArista)#Debug
        nodo_inicial = oArista.nodo_inicial
        nodo_final = oArista.nodo_final
        num_inicial = nodo_inicial.num
        num_final = nodo_final.num
        if not num_inicial in dic_add_nodos:
            node = NodoGUI(id=num_inicial, name=nodo_inicial.name)
            dic_add_nodos[num_inicial] = node
            grafoGUI.addNodo(node, is_FR = True)
        if not num_final in dic_add_nodos:
            node = NodoGUI(id=num_final, name=nodo_final.name)
            dic_add_nodos[num_final] = node
            #print("NameIncial:{p1} NameFinal:{p2} ".format(p1=node.name,p2=dic_add_nodos[num_final].name))#Debug
            grafoGUI.addNodo(node, is_FR = True)
        
        grafoGUI.addArista(dic_add_nodos[num_inicial], dic_add_nodos[num_final])
    #print("Dict:{p1}".format(p1=dic_add_nodos))#Debug
    return grafoGUI

def pygame_start_QuadTree(grafo, ltAristas, title):
    grafoGUI = pygame_crearGrafoQuadTree(grafo, ltAristas)
    pygame_init()
    pygame.display.set_caption(title)
    SCREEN.fill(GRAFO_GUI.BGCOLOR)
    rect = Rectangle(0,0,GRAFO_GUI.SIZE_SCREEN[0],GRAFO_GUI.SIZE_SCREEN[1])
    print_qt = True
    while True:
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break
        if print_qt:
            iniQuadTree = QuadTree(rect,2)
            
            if grafoGUI.print_nodos:
                for node in grafoGUI.set_nodos:
                    x, y =node.pygame_rect
                    iniQuadTree.insert(Point(x,y))#ArribaIzq
                grafoGUI.print_nodos = False
            """
            iniQuadTree.insert(Point(200,-190))
            iniQuadTree.insert(Point(200,-180))
            iniQuadTree.insert(Point(200,-170))
            iniQuadTree.insert(Point(200,-160))
            iniQuadTree.insert(Point(200,-150))
            iniQuadTree.insert(Point(200,-140))
            iniQuadTree.insert(Point(200,-130))
            iniQuadTree.insert(Point(200,-120))
            iniQuadTree.insert(Point(200,-110))
            iniQuadTree.insert(Point(200,-100))
            iniQuadTree.insert(Point(200,-90))
            iniQuadTree.insert(Point(200,-80))
            
            printPointsQuadTree([iniQuadTree])
            printAreaQuadTree(iniQuadTree.children())
										  
            pygame.display.flip()
            pygame.time.delay(GRAFO_GUI.REFRESH)
            """
									
            if grafoGUI.print_aristas:
                printPointsQuadTree_GUI(grafoGUI)
                printAreaQuadTree(iniQuadTree.children())
                printAristasQuadTree(grafoGUI)
                #pygame.display.flip()
                #pygame.time.delay(GRAFO_GUI.REFRESH)
                calcularFR(iniQuadTree, [iniQuadTree], grafoGUI)        
                grafoGUI.print_aristas = False
            pygame.display.flip()
            pygame.time.delay(GRAFO_GUI.REFRESH)
            
            """
            #SCREEN.fill(GRAFO_GUI.BGCOLOR)
            #printPointsQuadTree([qt])
            #pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(0 + GRAFO_GUI.PADDING_QUADTREE[0], 0 + GRAFO_GUI.PADDING_QUADTREE[1], 400, 400), 1)            
			
            print_qt = False
            """
def calcularFR(iniQuadTree, ltQuadTree, grafoGUI):
    #print("calcularFR")
    for oQuad in ltQuadTree:
        for point in oQuad.points:
            calcularFR(iniQuadTree, oQuad.children(), grafoGUI)
            
            grafoGUI.formulaRepulsion(oQuad, point)
            SCREEN.fill(GRAFO_GUI.BGCOLOR)
            printPointsQuadTree_GUI(grafoGUI)
            printAreaQuadTree([iniQuadTree])
            printAristasQuadTree(grafoGUI)
            if grafoGUI.count_print % GRAFO_GUI.COUNT_PRINT == 0:
                pygame.display.flip()
                pygame.time.delay(GRAFO_GUI.REFRESH)
                grafoGUI.count_print = 0
            grafoGUI.count_print = grafoGUI.count_print + 1
            #print(pt)

def printPointsQuadTree_GUI(grafoGUI):
    #print("-> " + str(ltQuadTree))#Debug
    for node in grafoGUI.set_nodos:
        #print("Nodo:{p1} React:{p2} ".format(p1=node.id,p2=node.pygame_rect))
        pygame.draw.circle(SCREEN, node.color, node.pygame_rect + GRAFO_GUI.PADDING_QUADTREE, GRAFO_GUI.RADIUS_SIZE)

def printPointsQuadTree(ltQuadTree):
    if not(ltQuadTree is None):
        for oQuadTree in ltQuadTree:
            for point in oQuadTree.points:
                pygame.draw.circle(SCREEN, (255, 0, 0), pygame.Vector2(point.x + GRAFO_GUI.PADDING_QUADTREE[0], point.y + GRAFO_GUI.PADDING_QUADTREE[1]), GRAFO_GUI.RADIUS_SIZE)
                #pygame.display.flip()
                #pygame.time.delay(GRAFO_GUI.REFRESH)
            printPointsQuadTree(oQuadTree.children())

def printAreaQuadTree(ltQuadTree):
    #print("-> " + str(ltQuadTree))#Debug
    if not(ltQuadTree is None):
        for oQuadTree in ltQuadTree:
            pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(oQuadTree.boundary.left + GRAFO_GUI.PADDING_QUADTREE[0], oQuadTree.boundary.top + GRAFO_GUI.PADDING_QUADTREE[1], oQuadTree.boundary.w, oQuadTree.boundary.h), 1)
            printAreaQuadTree(oQuadTree.children())

def printAristasQuadTree(grafoGUI):
    if grafoGUI.print_aristas:
        for arista in grafoGUI.set_arista:
            #print("NodoIncial:{p1} NodoFinal:{p2} ".format(p1=arista.nodo_inicial_gui.id,p2=arista.nodo_final_gui.id))
            pygame.draw.line(SCREEN, GRAFO_GUI.NODECOLOR, arista.nodo_inicial_gui.pygame_rect + GRAFO_GUI.PADDING_QUADTREE, arista.nodo_final_gui.pygame_rect + GRAFO_GUI.PADDING_QUADTREE)
            #pygame.display.flip()
            #pygame.time.delay(GRAFO_GUI.REFRESH)
        #grafoGUI.print_aristas = False


#Ejecuciones de salida para cada metodo
oGrafo = Grafo()
#oGrafo.modeloMalla(param_num_i = 10, param_num_j = 50)
#oGrafo.modeloErdosNRenyi(num_nodos = 500, max_num_aristas = 4)
#oGrafo.modeloGilbert(num_nodos = 500, probabilidad = 0.01)
#oGrafo.modeloGeografico(num_nodos = 500, w_rec = 40, h_rec = 20, prec = 4, r_distancia = 4)
#oGrafo.modeloBarabasiAlbert(num_nodos = 500, max_grado = 5)
oGrafo.modeloDorogovtsevMendes(num_nodos = 500)

"""
#oGrafo.modeloErdosNRenyi(num_nodos = 100, max_num_aristas = 4)
oGrafo.modeloGrafoBFS()
oGrafo.modeloGrafoDFS_R()
oGrafo.modeloGrafoDFS_I()
oGrafo.modeloGrafoDijkstra()
oGrafo.modeloGrafoKruskal()
oGrafo.modeloGrafoKruskalInverso()
oGrafo.modeloGrafoPrim()

oGrafo.modeloGrafoPygame(grafo = oGrafo, is_PRIM = True)
print("SizeNodo: " + str(oGrafo.getSizeNodos()))
print("SizeArista: " + str(oGrafo.getSizeAristas()))
"""
oGrafo.modeloGrafoPygame_QuadTree(grafo = oGrafo, is_BASE = True)
print("SizeNodo: " + str(oGrafo.getSizeNodos()))
print("SizeArista: " + str(oGrafo.getSizeAristas()))
