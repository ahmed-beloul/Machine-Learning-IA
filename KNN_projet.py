# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:09:59 2021

@author: ahmed
"""

import unicodecsv
import random
import operator
import math


def lecture_fichier(fichier):
    with open(fichier,'rb') as f:
        reader = unicodecsv.reader(f)
        return list(reader)


def division_fichier(f):         
    random.shuffle(f)
    f_entrainement = f[:int(len(f)*0.7)]
    f_test = f[int(len(f)*0.3):]
    return f_entrainement, f_test

def Distance_euclidienne(a, b):
    d = 0.0
    for i in range(len(a)-1):
        d += pow((float(a[i])-float(b[i])),2)  
    d = math.sqrt(d)     #distance euclidienne
    return d


def prediction(f_test, f_entrainement, k):
    for i in f_test:
        liste_Distance =[]
        knn = []
        mat=[['classA',0],['classB',0],['classC',0],['classD',0],['classE',0]]
        for j in f_entrainement:
            distance= Distance_euclidienne(i, j)
            liste_Distance.append((j[6], distance))
            #print(j[6])
        
        liste_Distance.sort(key = operator.itemgetter(1))
        #print(eu_Distance)
        knn = liste_Distance[:k]
        for el in knn:
            if el[0]=='classA':
                mat[0][1]+=1
            elif el[0]=='classB':
                mat[1][1]+=1
            elif el[0]=='classC':
                mat[2][1]+=1
            elif el[0]=='classD':
                mat[3][1]+=1
            elif el[0]=='classE':
                mat[4][1]+=1
        #print(mat)
        maxi=mat[0][1]
        classe=""
        for y in range(5):
            if(mat[y][1]>=maxi):
                maxi=mat[y][1]
                classe=mat[y][0]
        i.append(classe)
        
            
            


def ressemblance(f_test):
    good = 0
    for i in f_test:
        if i[6] == i[7]:
            good += 1  #compte le nombre de test reussi
    pourcentage_ressemblance = float(good)*100/len(f_test) 
    return pourcentage_ressemblance

fichierdata = lecture_fichier(r'C:\Users\Ahmed\Downloads\preTest.csv') 
f_entrainement, f_test = division_fichier(fichierdata)   #division du fichier de base en un test et un entrainement
                                
K=5
#prediction(f_test, f_entrainement, K)      #ajout des prediction au fichier test
#print("Pourcentage de ressemblance : ",ressemblance(f_test))   #test des differents K et leur proximité en % avec la realité

finalTest=lecture_fichier(r'C:\Users\Ahmed\Downloads\finalTest.csv')
data=lecture_fichier(r'C:\Users\Ahmed\Downloads\data.csv')
prediction(finalTest,data, K)
#print(finalTest)

def ecriture_fichier(f_test):
    with open(r'C:\Users\ahmed\OneDrive\Bureau\beloul.txt','w') as fichier:
        for el in f_test:
            fichier.write(el[6]+ "\n")
            
ecriture_fichier(finalTest)    #creation du fichier texte avec reponse