import numpy as np
import graph
import sys

def main():

    # Le poids des arcs de ce graphe correspondent aux capacités
    g = example1()
    h = example2()
    i = example3()
    
    # Le poids des arcs de ce graphe correspondent au flot
    flow1 = fordFulkerson(g, "s", "t")
    flow2 = fordFulkerson(h, "s", "t")
    flow3 = fordFulkerson(i, "s", "t")
    
    print(f"\n Voici le flot du premier graphe : \n{flow1}")
    print(f"\n Voici le flot du deuxième graphe : \n{flow2}")
    print(f"\n Voici le flot du troisième graphe : \n{flow3}")
 
 
###################### EXEMPLES ##########################################   
# Fonction créant un graphe sur lequel sera appliqué l'algorithme de Ford-Fulkerson
def example1():
        
    g = graph.Graph(np.array(["s", "a", "b", "c", "d", "e", "t"]))

    g.addArc("s", "a", 8)
    g.addArc("s", "c", 4)
    g.addArc("s", "e", 6)
    g.addArc("a", "b", 10)
    g.addArc("a", "d", 4)
    g.addArc("b", "t", 8)
    g.addArc("c", "b", 2)
    g.addArc("c", "d", 1)
    g.addArc("d", "t", 6)
    g.addArc("e", "b", 4)
    g.addArc("e", "t", 2)
    
    return g

def example2():
        
    g = graph.Graph(np.array(["s", "1", "2", "3", "4","t"]))

    g.addArc("s", "1", 16)
    g.addArc("s", "2", 13)
    g.addArc("1", "3", 12)
    g.addArc("3", "t", 20)
    g.addArc("2", "4", 14)
    g.addArc("4", "t", 4)
    g.addArc("4", "3", 7)
    g.addArc("3", "2", 9)
    g.addArc("2", "1", 4)
    g.addArc("1", "2", 10)
    
    return g

def example3():
        
    g = graph.Graph(np.array(["s", "A", "B", "C", "D","E","F","t"]))

    g.addArc("s", "A", 10)
    g.addArc("s", "C", 12)
    g.addArc("s", "E", 15)
    g.addArc("A", "C", 4)
    g.addArc("C", "E", 4)
    g.addArc("A", "B", 9)
    g.addArc("A", "D", 15)
    g.addArc("C", "D", 8)
    g.addArc("E", "F", 16)
    g.addArc("B", "D", 15)
    g.addArc("D", "F", 15)
    g.addArc("B", "t", 10)
    g.addArc("D", "t", 10)
    g.addArc("F", "t", 10)
    g.addArc("F", "C", 6)
    
    
    return g

############################## RESULTATS ########################################

"""Résultats obtenus :
  Voici le flot du premier graphe :
's' - 'a' (8.0)
's' - 'c' (3.0)
's' - 'e' (4.0)
'a' - 'b' (4.0)
'a' - 'd' (4.0)
'b' - 't' (8.0)
'c' - 'b' (2.0)
'c' - 'd' (1.0)
'd' - 't' (5.0)
'e' - 'b' (2.0)
'e' - 't' (2.0)


  Voici le flot du deuxième graphe :
's' - '1' (16.0)
's' - '2' (7.0)
'1' - '2' (4.0)
'1' - '3' (12.0)
'2' - '4' (11.0)
'3' - 't' (19.0)
'4' - '3' (7.0)
'4' - 't' (4.0)


  Voici le flot du troisième graphe :
's' - 'A' (10.0)
's' - 'C' (12.0)
's' - 'E' (6.0)
'A' - 'B' (9.0)
'A' - 'D' (1.0)
'B' - 't' (9.0)
'C' - 'D' (8.0)
'C' - 'E' (4.0)
'D' - 't' (9.0)
'E' - 'F' (10.0)
'F' - 't' (10.0)
"""
# Pour parcourir le graphe et suivre un chemin vers t, il nous faut une fonction récursive
def parcours_intermédiaire(g,capa_mat, flow_mat, current_node, t, chemin,mark):
    
    liste_arcs = [(arc.id1,arc.id2) for arc in g.getArcs()]
    
    # Vérification des conditions de terminaison :
    # Si la node actuelle est reliée à t ET que l'on n'a pas atteint sa capacité maximale
    if ((current_node,t) in liste_arcs) and flow_mat[current_node, t] != capa_mat[current_node, t] :
        
        #On marque t dans mu+
        mark[t]=+current_node
        
        # On l'ajoute à la liste des changements
        # Cette liste contient les arêtes du chemin et :
        #   -> capa - flow si l'arête est dans mu+
        #   -> capa si l'arête est dans mu-
        chemin.append([current_node, t, capa_mat[current_node, t]-flow_mat[current_node, t]])
        
        # On retourne True car on est bien arrivé à t
        return [chemin, True]  
    
    # Pour tous les autres noeuds (ie les noeuds non terminaux)
    else :
        
        for i in range(g.n) :
            
            # Itération sur les noeuds du graphe de mu+, ie :
            # Si le noeud est voisin au noeud actuel, que le chemin entre les 2 n'est pas saturé et que i n'est pas encore marqué
            if (current_node,i) in liste_arcs and (capa_mat[current_node, i]-flow_mat[current_node, i])>0 and mark[i] == sys.float_info.max :
                
                # On visite le noeud 
                temp_mark = mark.copy()             # Copie de la liste mark
                temp_mark[i] = +current_node        # Ajout temporaire du noeud i à mu+
                [chemin_temp, end] = parcours_intermédiaire(g, capa_mat, flow_mat, i, t, chemin, temp_mark)
                
                # Si on a atteint t (Qu'on a une chaîne optimisante), on renvoie tempchanges et True
                if end == True :
                    mark[i] = current_node
                    chemin_temp.append(([current_node, i, capa_mat[current_node, i]-flow_mat[current_node, i]]))
                    return ([chemin_temp, end])

            # Itération sur les noeuds du graphe de mu- ie:
            # Si l'arc i->noeud_actuel existe ET que l'arc est non nul Et que i est non marqué
            elif (i,current_node) in liste_arcs and flow_mat[i, current_node]!=0 and mark[i] == sys.float_info.max :
                
                temp_mark = mark
                temp_mark[i] = -current_node              # On ajoute i à mu- temporairement
                [chemin_temp, end] = parcours_intermédiaire(g, capa_mat, flow_mat, i, t, chemin, temp_mark)
                
                # Si on peut trouver une chaîne optimisante à partir de lui, on revoie ce cas
                if end == True :
                    mark[i] = -current_node   # On ajoute i à mu- pour de vrai
                    chemin_temp.append([i, current_node, -flow_mat[i, current_node]])
                    return ([chemin_temp, end])
    
        #Sinon on renvoie qu'on reste sur place avec impossibilité de trouver une chaîne depuis l'état actuel
        return ([chemin, False])
            
# Fonction appliquant l'algorithme de Ford-Fulkerson à un graphe
# Les noms des sommets sources est puits sont fournis en entrée
def fordFulkerson(g, sName, tName):

    """
    Marquage des sommets du graphe:
     - mark[i] est égal à +j si le sommet d'indice i peut être atteint en augmentant le flot sur l'arc ji
     - mark[i] est égal à  -j si le sommet d'indice i peut être atteint en diminuant le flot de l'arc ji
     - mark[i] est égal à sys.float_info.max si le sommet n'est pas marqué
    """
    
    # Initialisation de mark
    mark = [sys.float_info.max] * g.n
    
    # Récupérer l'indice de la source et du puits.
    s = g.indexOf(sName)
    t = g.indexOf(tName)

    #déclaration d'un noeud courant de travail, initialisation à la source.
    current_node = s
    
    # Créer un nouveau graphe contenant les même sommets que g
    # Initialiser le flot à 0
    
    flow = graph.Graph(g.nodes)
    
    ############## POUR PLUS DE LISIBILITE ##############
    
    # Liste des sommets voisins
    liste_arcs = [(arc.id1,arc.id2) for arc in g.getArcs()]
                  
    # Matrice des capacités du graphe
    capa_mat = g.adjacency

    # Matrice du flot
    flow_mat = np.full(np.shape(capa_mat),0)
    
    # Indicateur de fin de l'algorithme
    # On verra plus loin quand est ce que end est Vrai ou Non
    end = True

    ################# BOUCLE DE L'ALGORITHME ###########
    while end :
        
        # Réinitialisation des paramètres
        end = False 
        mark = [sys.float_info.max] * g.n
        chemin = []
        
        # récupération du chemin
        [chemin, end] = parcours_intermédiaire(g,capa_mat, flow_mat, s, t, chemin ,mark)    # end est True si t a été atteint
        
        # Si t est atteint, on met à jour le flot
        if end == True:
            fluxchanges = [0] * len(chemin)
            
            for i in range(len(chemin)) :
                fluxchanges[i] = chemin[i][2]  #Liste des amélioration possibles sur chaque arête du chemin (qui dépend si elles sont dans mu+ ou mu-)
            
            alpha = np.min(np.abs(fluxchanges))   #Calcul de l'amélioration maximale du flot dans ce chemin
           
            for arc in chemin :
                flow_mat[arc[0], arc[1]] += alpha * np.sign(arc[2])   # Mise à jour du flot (on ajoute ou diminue selon mu+ ou mu-)
                
        # Et c'est reparti jusqu'à que end devienne False, ie qu'on n'arrive pas à atteindre t

    # Retour de l'arc résultat
    
    for i in range(g.n):
        for j in range(g.n):
            flow.adjacency[i,j] = flow_mat[i,j]
    
    return flow
   

if __name__ == '__main__':
    main()
