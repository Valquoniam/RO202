import graph
import sys
import numpy as np

def main():
    
    ################# GRAPHE DE L'EXERCICE 2 ###############
    cities = []
    cities.append("Paris")
    cities.append("Hambourg")
    cities.append("Londres")
    cities.append("Amsterdam")
    cities.append("Edimbourg")
    cities.append("Berlin")
    cities.append("Stockholm")
    cities.append("Rana")
    cities.append("Oslo")

    g = graph.Graph(cities)
    
    g.addArc("Paris", "Hambourg", 7)
    g.addArc("Paris",  "Londres", 4)
    g.addArc("Paris",  "Amsterdam", 3)
    g.addArc("Hambourg",  "Stockholm", 1)
    g.addArc("Hambourg",  "Berlin", 1)
    g.addArc("Londres",  "Edimbourg", 2)
    g.addArc("Amsterdam",  "Hambourg", 2)
    g.addArc("Amsterdam",  "Oslo", 8)
    g.addArc("Stockholm",  "Oslo", 2)
    g.addArc("Stockholm",  "Rana", 5)
    g.addArc("Berlin",  "Amsterdam", 2)
    g.addArc("Berlin",  "Stockholm", 1)
    g.addArc("Berlin",  "Oslo", 3)
    g.addArc("Edimbourg",  "Oslo", 7)
    g.addArc("Edimbourg",  "Amsterdam", 3)
    g.addArc("Edimbourg",  "Rana", 6)
    g.addArc("Oslo",  "Rana", 2)
    
    ################# GRAPHES DE L'EXERCICE 4 ###############
    
    # Premier graphe
    fig2a = graph.Graph(np.array(["r","a", "b", "c", "d", "e", "f", "g"]))
    fig2a.addArc("r","a",5)
    fig2a.addArc("r","b",4)
    fig2a.addArc("b","a",5)
    fig2a.addArc("b","c",3)
    fig2a.addArc("b","g",9)
    fig2a.addArc("a","c",3)
    fig2a.addArc("c","d",2)
    fig2a.addArc("c","f",6)
    fig2a.addArc("c","g",8)
    fig2a.addArc("d","e",2)
    fig2a.addArc("d","a",8)
    fig2a.addArc("e","c",4)
    fig2a.addArc("g","f",5)
    
    # Deuxième graphe
    fig2b = graph.Graph(np.array(["r","A", "B", "C", "D", "E", "F", "G"]))
    fig2b.addArc("r","A",2)
    fig2b.addArc("r","G",3)
    fig2b.addArc("F","G",3)
    fig2b.addArc("F","D",4)
    fig2b.addArc("A","F",1)
    fig2b.addArc("A","B",3)
    fig2b.addArc("B","C",2)
    fig2b.addArc("D","C",2)
    fig2b.addArc("E","D",3)
    fig2b.addArc("E","F",2)
    fig2b.addArc("G","E",2)
    
    #########################################################
    # Applique l'algorithme de Dijkstra pour obtenir une arborescence
    tree1 = dijkstra(g, "Paris")
    print(tree1)
    
    tree2 =  dijkstra(fig2a, "r")
    print(tree2)
    
    tree3 =  dijkstra(fig2b, "r")
    print(tree3)

############ RESULTATS OBTENUS #############
    """
1er arbre :
    Poids du chemin : 17.0 

'Paris' - 'Londres' (4.0)
'Paris' - 'Amsterdam' (3.0)
'Hambourg' - 'Berlin' (1.0)
'Hambourg' - 'Stockholm' (1.0)
'Londres' - 'Edimbourg' (2.0)
'Amsterdam' - 'Hambourg' (2.0)
'Stockholm' - 'Oslo' (2.0)
'Oslo' - 'Rana' (2.0)

2ème arbre :
    Poids du chemin : 31.0

'r' - 'a' (5.0)
'r' - 'b' (4.0)
'b' - 'c' (3.0)
'b' - 'g' (9.0)
'c' - 'd' (2.0)
'c' - 'f' (6.0)
'd' - 'e' (2.0)

3ème arbre :
    Poids du chemin : 17.0

'r' - 'A' (2.0)
'r' - 'G' (3.0)
'A' - 'B' (3.0)
'A' - 'F' (1.0)
'B' - 'C' (2.0)
'F' - 'D' (4.0)
'G' - 'E' (2.0)
    """

def dijkstra(g, origin):

   ########### INITIALISATION ##############
   
   # Créer un nouveau graphe contenant les mêmes sommets que g
   tree = graph.Graph(g.nodes)
    
   # Get the index of the origin 
   r = g.indexOf(origin)
   
   #Build the list of indexes, as we'll work with them
   v = [k for k in range(0,g.n)]
   
   # Next node considered 
   pivot = r
   
   # Liste qui contiendra les sommets ayant été considérés comme pivot
   v2 = []
   v2.append(r)
   
   # Initialisation de la liste des prédecesseurs (cest fait un peu brutalement)
   pred = [0] * g.n
   
   # Initialisation du tableau des distances des sommets à r
   # Les distances entre r et les autres sommets sont initialement infinies
   pi = [sys.float_info.max] * g.n
   pi[r] = 0
     
   ############### ALGORITHME ###############
   
   for i in range(1,g.n):                                           # Sélection des n-1 pivots du chemin
       for node in (list(set(v) - set(v2))):                        # Sommets pas encore pivots (Attention, on travaille en index !)
           # On renomme les variables pour plus de lisibilité
           weight = g.adjacency[pivot,node]
           
           #Actualisation de pi et de pred
           if weight != 0.0 and pi[pivot] + weight < pi[node]:     # Sommets reliés au pivot avec nouveau chemin détecté
              pi[node] = pi[pivot] + weight                        # On acutalise le nouveau meilleur chemin
              pred[node] = pivot                                   # On actualise aussi le parent
        
       # Choix du meilleur pivot en codant notre propre fonction argmin, avec les indices uniquement dans v-v2
       pi_min = sys.float_info.max  
       for index in list(set(v) - set(v2)):
           if pi[index] <pi_min:
               pi_min = pi[index]
       
       # Traitement des villes ayant la même distance à l'origine : On les prend une par une
       occurences  = [k for (k, item) in enumerate(pi) if item == pi_min]  # On récupère les indices des villes à distances égales
       if len(occurences)!=1:                                              # Si il y a plusieurs occurences, on récupère les indices un par un
           k=0
           while(occurences[k] in v2):    #On fait la récupération "un par un" avec une boucle while
               k+=1
           pivot = occurences[k]
       else:
           pivot = occurences[0]                                           # Sinon, tout va bien et on prend le seul indice dans "occurences"
      
       v2.append(pivot)                                                    # Ajout du nouveau pivot
       
   #Construction de l'arborescence et affichage de l'abre (on affiche aussi le poids)
   total_weight = 0
   for i in range(0,g.n):
       weight = g.adjacency[pred[i],i] 
       tree.addArcByIndex(pred[i], i, weight)       #On ajoute, pour chaque node, sa node parente trouvée par l'algorithme
       total_weight += weight

   if total_weight == 0:
       return None
   
   print(f"Poids du chemin : {total_weight} \n")
   return tree
     
if __name__ == '__main__':
    main()
