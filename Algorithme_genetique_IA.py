# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 18:23:12 2021

@author: ahmed
"""


import csv
import random
import math

i1=[]
ti1=[]

with open(r'C:\Users\ahmed\OneDrive\Bureau\temperature_sample.csv') as fichier:
    lecturefichier=csv.reader(fichier,delimiter=';')
    compteur=0
    for ligne in lecturefichier:
        for element in ligne:
            compteur=compteur+1
            if(compteur%2!=0):
                i1.append(element)
            else:
                ti1.append(element)
                
del i1[0]
del ti1[0]
i=[]
ti=[]
for k in range(len(i1)):
    i.append(float(i1[k]))
    ti.append(float(ti1[k]))
    
    
    
def Weierstrass(a,b,c,i):
        
        t_exp=[]
        for j in i:
            res=0
            for n in range(c):
                res+=(a**n)*math.cos(math.pi*(b**n)*j)
            t_exp.append(res)
        return t_exp

class individu:
    
    def __init__(self,a=None,b=None,c=None,d=None):
        if(a==None and b==None and c==None and d==None):
            self.a=int(random.uniform(0,1)*100)/100.
            self.b=random.randint(1,20)
            self.c=random.randint(1,20)
        else:
            self.a=a
            self.b=b
            self.c=c
        
        self.d=fitness(self,ti,i)
        
    def __str__(self):
        return f"{self.a,self.b,self.c}"
    

def fitness(indiv,ti,i):
    texp=Weierstrass(indiv.a,indiv.b,indiv.c,i)
    res=0
    for k in range(len(ti)):
        res=res+abs(ti[k]-texp[k])
    return res/len(ti)  
    
            
    
def creation_population(taille):
    population=[]
    for i in range(taille):
        population.append(individu())
    return population
    
def evaluation(population):
    return sorted(population,key=lambda x:x.d)

def selection(population, meilleur, pire):
    a=population[:meilleur]
    b=population[-pire:]
    return a+b

def croisement(indiv1,indiv2):
    e1=individu(indiv1.a,indiv1.b,indiv2.c)
    e2=individu(indiv2.a,indiv2.b,indiv1.c)
    return [e1,e2]

def mutation(indiv):
    indiv.a=random.uniform(0, 1)
    indiv.c=random.randint(1,20)
    return indiv

def algo():
    population=creation_population(80) #population de 80 individu
    for k in range(25):
        population[k].d=fitness(population[k],ti,i)
    compte=0
    d1=False
    while d1==False: 
        print ("it n° : ", compte)
        compte+=1
        eval=evaluation(population) #retourne liste trié du meilleur au pire
        if eval[0].d<0.04: #j'ai remarqué que meme avec une boucle, ca stagnait vers 0.3
            d1=True
        else:
            sel=selection(eval, 10,5) # selection : 10 meilleurs 5 pires
            croises=[] 
            for p in range (0, len(sel)-1,2 ): 
                croises+=croisement(sel [p], sel [p+1])
            mutes=[]
            for p in sel: 
                mutes.append(mutation(p))
            newalea=creation_population(5) # ajout de 5 individus
            for k in range(5):
                newalea[k].d=fitness(newalea[k],ti,i)
            population=sel[:]+croises[:]+mutes[:]+newalea[:] #nouvelle population avec les anciens
    print(eval[0])
    print(eval[0].d)
    
algo()
