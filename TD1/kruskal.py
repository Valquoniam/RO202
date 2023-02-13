import numpy as np
import graph
import sys

def main():
    
    # Créer un graphe contenant les sommets a, b, c, d, e, f, g 
    g = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g"]))

    # Ajouter les arêtes
    g.addEdge("a", "b",  1.0)
    g.addEdge("a", "c",  3.0)
    g.addEdge("b", "c",  2.0)
    g.addEdge("b", "d",  5.0)
    g.addEdge("b", "e",  7.0)
    g.addEdge("b", "f",  9.0)
    g.addEdge("c", "d",  4.0)
    g.addEdge("d", "e",  6.0)
    g.addEdge("d", "g", 12.0)
    g.addEdge("e", "f",  8.0)
    g.addEdge("e", "g", 11.0)
    g.addEdge("f", "g", 10.0)
    
    """
    Le résulat pour computeMin = True:
                Le poids total de l'abre est : 31.0
                Voici l'arbre :

                'a' - 'b' (1.0)
                'b' - 'c' (2.0)
                'c' - 'd' (4.0)
                'd' - 'e' (6.0)
                'e' - 'f' (8.0)
                'f' - 'g' (10.0)
    """
    
    """
    Le résultat pour computeMin = False:
                Le poids total de l'abre est : 49.0
                Voici l'arbre :

                'a' - 'c' (3.0)
                'b' - 'f' (9.0)
                'c' - 'd' (4.0)
                'd' - 'g' (12.0)
                'e' - 'g' (11.0)
                'f' - 'g' (10.0)
    """
    
    ####### EXERCICE 3 - QUESTION 4 ET 5#####
    
    #1er arbre de test :
    fig1a = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g","h"]))
    fig1a.addEdge("a", "b",  9.0)
    fig1a.addEdge("a", "f",  6.0)
    fig1a.addEdge("a", "h",  9.0)
    fig1a.addEdge("f", "e",  1.0)
    fig1a.addEdge("b", "e",  5.0)
    fig1a.addEdge("e", "g",  3.0)
    fig1a.addEdge("g", "c",  5.0)
    fig1a.addEdge("g", "d",  9.0)
    fig1a.addEdge("g", "h",  5.0)
    fig1a.addEdge("d", "h",  7.0)
    fig1a.addEdge("c", "d",  2.0)
    fig1a.addEdge("b", "d",  8.0)
    fig1a.addEdge("b", "c",  5.0)
    
    """ 
    Le résultat pour ComputeMin = True: 
                    Le poids total de l'abre est : 27.0
                    Voici l'arbre :

                    'a' - 'f' (6.0)
                    'b' - 'e' (5.0)
                    'c' - 'd' (2.0)
                    'c' - 'g' (5.0)
                    'e' - 'f' (1.0)
                    'e' - 'g' (3.0)
                    'g' - 'h' (5.0)
    """
    
    #2ème arbre de test 
    fig1b = graph.Graph(np.array(["A", "B", "C", "D", "E", "F"]))
    fig1b.addEdge("A", "B",  4.0)
    fig1b.addEdge("A", "C",  3.0)
    fig1b.addEdge("B", "C",  5.0)
    fig1b.addEdge("B", "F",  2.0)
    fig1b.addEdge("C", "F",  5.0)
    fig1b.addEdge("C", "D",  2.0)
    fig1b.addEdge("F", "D",  3.0)
    fig1b.addEdge("D", "E",  4.0)
    fig1b.addEdge("F", "E",  3.0)
    
    """
    Le résultat pour computeMin = True :
                Le poids total de l'abre est : 13.0
                Voici l'arbre :

                'A' - 'C' (3.0)
                'B' - 'F' (2.0)
                'C' - 'D' (2.0)
                'D' - 'F' (3.0)
                'E' - 'F' (3.0)
    """ 
    #####################################
    # Obtenir un arbre couvrant de poids minimal du graphe
    tree = kruskalCC(g)
    
    # S'il existe un tel arbre (i.e., si le graphe est connexe)
    if tree != None:
        
        # L'afficher
        print(tree)
    
    else:
        print("Pas d'arbre couvrant")

# Applique l'algorithme de Kruskal pour trouver un arbre couvrant de poids minimal d'un graphe
# Retourne: Un arbre couvrant de poids minimal du graphe ou None s'il n'en existe pas
def kruskal(g, computeMin):
    
    if type(computeMin)!=bool:
        print("Error : 2nd argument computeMin has to be a boolean")
        return 0
    ############### INITIALISATION ###############
    
    # Créer un nouveau graphe contenant les mêmes sommets que g
    tree = graph.Graph(g.nodes)
    
    # Récupérer toutes les arêtes de g
    edges = g.getEdges()
    
    # Trier les arêtes par poids croissant si computeMin est vrai, sinon on a juste à trier dans l'autre sens ! 
    if computeMin == False:
        edges.sort(reverse = True) #Tri dans l'ordre décroissant
    else:
        edges.sort()

    # Compter le poids de l'arbre
    addedWeights = 0
      
    ################ ALGORITHME #####################
    
    # On utilise l'implémentation Union-Find pour détecter les cycles dans le graphe
    for edge in edges:
       if tree.createACycle(edge) == False:  #On ajoute le chemin à l'arbre si il ne forme pas encore de cycle avec ce dernier
           tree.addCopyOfEdge(edge)
           addedWeights+=edge.weight         #On ajoute également son poids
    
    print(f"\nLe poids total de l'abre est : {addedWeights}")
    print("\nVoici l'arbre :\n")
    
    if addedWeights ==0:                     #Si il n'y a aucun arbre possible, on retourne None
        return None
    
    return tree
    
    
##################### EXERCICE 3 - Q6 #################
 
def kruskalCC(g):
    
    # Créer un nouveau graphe contenant les mêmes sommets que g
    tree = graph.Graph(g.nodes)
    
    # Récupérer toutes les arêtes de g
    edges = g.getEdges()
    edges.sort()
    # Compter le poids de l'arbre
    addedWeights = 0
      
    # Liste des composantes connexes
    component = [k for k in range(0,g.n)]
    
    ################ ALGORITHME #####################
    
    # On utilise l'implémentation Union-Find pour détecter les cycles dans le graphe
    
    for edge in edges:
        if component[edge.id1] != component[edge.id2]:       #Si les 2 noeuds sont des des composantes connexes différentes, c'est good
            tree.addCopyOfEdge(edge)
            addedWeights += edge.weight
            component[edge.id2] = component[edge.id1]        #On met le dernier noeud visité dans la composante connexe de la racine et ainsi de suite

                   
    print(f"\nLe poids total de l'abre est : {addedWeights}")
    print("\nVoici l'arbre :\n")
    
    if addedWeights ==0:                     #Si il n'y a aucun arbre possible, on retourne None
        return None        
    return tree

if __name__ == '__main__':
    main()
