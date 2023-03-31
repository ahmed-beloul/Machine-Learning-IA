# -*- coding: utf-8 -*-
"""
Created on Tue May 13 13:42:47 2021

@author: Ahmed
"""


import numpy as np
import random

#choix de la profondeur apres plusieurs tests
p1 = 2
INF =np.inf
taille = 12


#%%
def Maxi(a, b): 
    max=b
    if a> b: 
        max=a
    return max
    
def Min(a,b):
    min=b
    if a < b: 
        min=a
    return min



# %%
#parametrage du jeu de l'ia
def jeuIA(grillee):
    
    sol=[[False for i in range(taille)] for j in range(taille)]
    
    for i in range(taille):
        for j in range(taille):
            if(grillee[i][j]==0) :
                for vhoriz in range(i-1,i+2): 
                    for vvert in range(j-1,j+2):
                        if (vhoriz >=0 and vhoriz <taille and vvert >=0 and vvert<taille):
                            if(grillee[vhoriz][vvert]!=0): 
                                sol[i][j] = True                              
    return sol




# %%

#nous prenons les cases possible pour le joueur
def jeujoueur(grillee):
    
    sol=[[False for i in range(taille)] for j in range(taille)]
    
    for i in range(taille):
        for j in range(taille):
            if(grillee[i][j]==0) :
                sol[i][j]=True
    return sol




#verification de l'alignement le plus grand
def alignement_jeu(grillee, i , j):
    balayage = 1
    if grillee[i][j] != 0:
        case = grillee[i][j]
        
        
        joueur1 = 1 
        joueur2 = 1
        lignesens1=i
        colonnesens1=j+1
        #premier sens
        while (abs(lignesens1) < taille) and (abs(colonnesens1) < taille) and (grillee[lignesens1][colonnesens1] == case):
            joueur1 +=1
            colonnesens1 += 1
        
        #sens opposé
        lignesens2=i
        colonnesens2=j-1
        while (abs(lignesens2) < taille) and (abs(colonnesens2) < taille) and (grillee[lignesens2][colonnesens2] == case):
            joueur2 +=1
            colonnesens2 -= 1
        sol=[joueur1,joueur2]
        c=sol[0]+sol[1]-1
        balayage= Maxi(balayage, c) #ligne 
        
        
        joueur1 = 1 
        joueur2 = 1
        lignesens1=i+1
        colonnesens1=j
        #premier sens
        while (abs(lignesens1) < taille) and (abs(colonnesens1) < taille) and (grillee[lignesens1][colonnesens1] == case):
            joueur1 +=1
            lignesens1 += 1
        
        #sens opposé
        lignesens2=i-1
        colonnesens2=j
        while (abs(lignesens2) < taille) and (abs(colonnesens2) < taille) and (grillee[lignesens2][colonnesens2] == case):
            joueur2 +=1
            lignesens2 -= 1
        sol=[joueur1,joueur2]
        c=sol[0]+sol[1]-1
        balayage= Maxi(balayage, c) #colonne
        
        joueur1 = 1 
        joueur2 = 1
    
        lignesens1=i+1
        colonnesens1=j+1
        #premier sens
        while (abs(lignesens1) < taille) and (abs(colonnesens1) < taille) and (grillee[lignesens1][colonnesens1] == case):
            joueur1 +=1
            lignesens1 += 1
            colonnesens1 += 1
        
        #sens opposé
        lignesens2=i-1
        colonnesens2=j-1
        while (abs(lignesens2) < taille) and (abs(colonnesens2) < taille) and (grillee[lignesens2][colonnesens2] == case):
            joueur2 +=1
            lignesens2 -= 1
            colonnesens2 -= 1
        sol=[joueur1,joueur2]
        c=sol[0]+sol[1]-1
        balayage= Maxi(balayage, c) # balaye diag1
        
        joueur1 = 1 
        joueur2 = 1
        lignesens1=i-1
        colonnesens1=j+1
        #premier sens
        while (abs(lignesens1) < taille) and (abs(colonnesens1) < taille) and (grillee[lignesens1][colonnesens1] == case):
            joueur1 +=1
            lignesens1 += -1
            colonnesens1 += 1
        
        #sens opposé
        lignesens2=i+1
        colonnesens2=j-1
        while (abs(lignesens2) < taille) and (abs(colonnesens2) < taille) and (grillee[lignesens2][colonnesens2] == case):
            joueur2 +=1
            lignesens2 -= -1
            colonnesens2 -= 1
        sol=[joueur1,joueur2]
        c=sol[0]+sol[1]-1
        balayage= Maxi(balayage, c) # balaye diag2
        
    return balayage #si balayage vaut 4 le jeu est fini.



# %%
#afin de savoir si la partie est fini
def Jeutermine(grillee):

    resultat=[False,None]
    case=True
    for i in range (taille):
        for j in range (taille):
            if grillee[i][j] != 0:
                if alignement_jeu(grillee,i,j) >= 4:
                    resultat= [True,grillee[i][j]]
            else:
                case=False
    
    if case:
        resultat= [False,0]
    
    return resultat
    
    
                  
# je dis que la case est occupé
def caseprise(grillee):
    ligne=-1
    colonne=-1
    
    caseok=False
    jeuj=jeujoueur(grillee)
    while(caseok == False):
        while(ligne<0 or ligne>=taille or colonne<0 or colonne>=taille):
            
            try:
                colonne=int(input("Numero colonne : "))-1
            except :
                colonne=taille
            try :
                ligne= int((input("Numero ligne : ")))-1
            except :
                ligne=taille
            print("case occupe")
        caseok = jeuj[ligne][colonne]
        if (caseok): 
            grillee[ligne][colonne]=-1
        else :
            ligne=-1
            colonne=-1
    return grillee




# %%
def sousheurcolonne(grillee,sol,a1,b1): 
    
    if(grillee[a1][b1]!=0):
        
        
        c1=0
        ch1=0
        c2=0
        ch2=0
        case=grillee[a1][b1]
        verifch=True
        casegagnee=0
        for compteur in range(4):
            
            a2=a1+compteur
            if(a2<taille):
                casegagnee+=1
                if(grillee[a2][b1]==case):
                    c2+=1 
                    if(verifch==True):
                        ch2+=1
                    elif(grillee[a2][b1]!=0):
                        casegagnee-=1 
                        break
                    else:
                        verifch=False
        verifch=True
        casegagnee-=1
        for compteur in range(4): 
            a3=a1-compteur
            if(a3>=0):
                casegagnee+=1
                if(grillee[a3][b1]==case):
                    c1+=1
                    if(verifch==True):
                        ch1+=1
                    elif(grillee[a3][b1]!=0):
                        casegagnee-=1
                        break
                    else:
                        verifch=False
                        
        if(casegagnee<4): 
           c1=0  
           c2=0
           
        if(case==-1):
            if(c2!=0):
                sol-= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol-= 100**(ch1-2)+c1-2   
        if(case==1):
            if(c2!=0):
                sol+= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol+= 100**(ch1-2)+c1-2
        
def sousheurligne(grillee,sol,a1,b1): 
    
    if(grillee[a1][b1]!=0):
        
        
        c1=0
        ch1=0
        c2=0
        ch2=0
        case=grillee[a1][b1]
        verifch=True
        casegagnee=0
        for compteur in range(4):
            
            b2=b1+compteur
            if(b2<taille):
                casegagnee+=1
                if(grillee[a1][b2]==case):
                    c2+=1 
                    if(verifch==True):
                        ch2+=1
                    elif(grillee[a1][b2]!=0):
                        casegagnee-=1 
                        break
                    else:
                        verifch=False
        verifch=True
        casegagnee-=1
        for compteur in range(4): 
            b3=b1-compteur
            if(b3>=0):
                casegagnee+=1
                if(grillee[a1][b3]==case):
                    c1+=1
                    if(verifch==True):
                        ch1+=1
                    elif(grillee[a1][b3]!=0):
                        casegagnee-=1
                        break
                    else:
                        verifch=False
                        
        if(casegagnee<4): 
           c1=0  
           c2=0
           
        if(case==-1):
            if(c2!=0):
                sol-= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol-= 100**(ch1-2)+c1-2   
        if(case==1):
            if(c2!=0):
                sol+= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol+= 100**(ch1-2)+c1-2

def sousheurdiag1(grillee,sol,a1,b1): 
    
    if(grillee[a1][b1]!=0):
        
        
        c1=0
        ch1=0
        c2=0
        ch2=0
        case=grillee[a1][b1]
        verifch=True
        casegagnee=0
        for compteur in range(4):
            a2=b1+compteur
            b2=b1+compteur
            if(a2<taille and b2<taille):
                casegagnee+=1
                if(grillee[a2][b2]==case):
                    c2+=1 
                    if(verifch==True):
                        ch2+=1
                    elif(grillee[a2][b2]!=0):
                        casegagnee-=1 
                        break
                    else:
                        verifch=False
        verifch=True
        casegagnee-=1
        for compteur in range(4): 
            a3=a1-compteur
            b3=b1-compteur
            if(a3>=0 and b3>=0):
                casegagnee+=1
                if(grillee[a3][b3]==case):
                    c1+=1
                    if(verifch==True):
                        ch1+=1
                    elif(grillee[a3][b3]!=0):
                        casegagnee-=1
                        break
                    else:
                        verifch=False
                        
        if(casegagnee<4): 
           c1=0  
           c2=0
           
        if(case==-1):
            if(c2!=0):
                sol-= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol-= 100**(ch1-2)+c1-2   
        if(case==1):
            if(c2!=0):
                sol+= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol+= 100**(ch1-2)+c1-2


def sousheurdiag2(grillee,sol,a1,b1): 
    
    if(grillee[a1][b1]!=0):
        
        
        c1=0
        ch1=0
        c2=0
        ch2=0
        case=grillee[a1][b1]
        verifch=True
        casegagnee=0
        for compteur in range(4):
            a2=b1+compteur
            b2=b1-compteur
            if(a2<taille and b2>=0):
                casegagnee+=1
                if(grillee[a2][b2]==case):
                    c2+=1 
                    if(verifch==True):
                        ch2+=1
                    elif(grillee[a2][b2]!=0):
                        casegagnee-=1 
                        break
                    else:
                        verifch=False
        verifch=True
        casegagnee-=1
        for compteur in range(4): 
            a3=a1-compteur
            b3=b1+compteur
            if(a3>=0 and b3<taille):
                casegagnee+=1
                if(grillee[a3][b3]==case):
                    c1+=1
                    if(verifch==True):
                        ch1+=1
                    elif(grillee[a3][b3]!=0):
                        casegagnee-=1
                        break
                    else:
                        verifch=False
                        
        if(casegagnee<4): 
           c1=0  
           c2=0
           
        if(case==-1):
            if(c2!=0):
                sol-= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol-= 100**(ch1-2)+c1-2   
        if(case==1):
            if(c2!=0):
                sol+= 100**(ch2-2)+c2-2
            if(c1!=0):
                sol+= 100**(ch1-2)+c1-2


def heur(grillee):
    sol=0
    if (Jeutermine(grillee)[0]): 
        sol=10000000000*Jeutermine(grillee)[1]
    else:
    
        
        for i in range (taille):
            for j in range (taille):
                sousheurligne(grillee,sol,i,j)
                
        for j in range (taille):
            for i in range (taille):
                sousheurcolonne(grillee, sol, i, j)
                
   
        for i in range (taille):
            for j in range (taille):
                sousheurdiag1(grillee, sol, i, j)
                         
    
        for i in range (taille):
            for j in range (taille):
                sousheurdiag2(grillee, sol, i, j)
                        
    return sol


def MeilleursolutionIA(grillee,p,alpha,beta):
    
    if (Jeutermine(grillee)[0]): 
        return Jeutermine(grillee)[1]
    
    elif (p==0) :
        return heur(grillee)
    
    else :
        meilleursol=-INF 
        pos=jeuIA(grillee)
        for i in range(12):
            for j in range(12):
                if(pos[i][j]):
                    grillee[i][j]=1
                    meilleursolutionjoueur=Meilleursolutionjoueur(grillee,p-1,alpha,beta)
                    if(meilleursolutionjoueur>meilleursol):
                        meilleursol=meilleursolutionjoueur 
                        alpha=max(alpha,meilleursolutionjoueur)
                    grillee[i][j]=0
                    
                    if alpha>=beta : 
                        break
        resultat=meilleursol
        
        return resultat

def Meilleursolutionjoueur(grillee,p,alpha,beta):
    if (Jeutermine(grillee)[0]): 
        return Jeutermine(grillee)[1]
    
    elif (p==0) :
        return heur(grillee)
    
    else :
        plusnul=INF 
        pos=jeuIA(grillee)
        for i in range(12):
            for j in range(12):
                if(pos[i][j]):
                    grillee[i][j]=-1
                    meilleursolutionia=MeilleursolutionIA(grillee,p-1,alpha,beta)
                    if(meilleursolutionia<plusnul):
                        plusnul=meilleursolutionia 
                        beta=min(beta,meilleursolutionia)
                    grillee[i][j]=0
                    
                    if alpha>=beta : 
                        break
        resultat=plusnul        
        
        return resultat

   
 
    


def AlgoMinMax(grillee,p,alpha,beta):
    
    listemeilleursol=[]
    
    meilleursol=-INF 
    
    for i in range(taille):
        for j in range(taille):
            
            if(jeuIA(grillee)[i][j]):
                grillee[i][j]=1
                meilleursoljoueur=Meilleursolutionjoueur(grillee,p-1,alpha,beta)
                if(meilleursoljoueur==meilleursol):
                    
                    listemeilleursol.append([i,j]) 
                    
                elif(meilleursoljoueur>meilleursol):
                    listemeilleursol[:]=[] 
                    listemeilleursol.append([i,j]) 
                    meilleursol=meilleursoljoueur          
                grillee[i][j]=0
                
    meilleursolutionchoisi=random.randint(0,len(listemeilleursol)-1)
    
    grillee[listemeilleursol[meilleursolutionchoisi][0]][listemeilleursol[meilleursolutionchoisi][1]]=1


# %%
def interface(grillee): 
    
    print("\n     1    2   3   4   5  6   7   8   9   10   11  12 ")
    pos = 0
    for i in range(taille):
        pos += 1
        if(pos<10):
            print (pos, end='')
            print ("   ", end='|')
        else:
            print (pos, end='')
            print ("  ", end='|')
        for j in range(len(grillee[::][0])):
            if(grillee[i][j])==1: 
                print(' X ',end='')
            elif(grillee[i][j])==-1 : 
                print(' O ',end='')
            else : 
                print('   ',end='')
            print('|',end='')
        print()
    

def Debutjeu():
    
    grillee=[[0 for i in range(taille)] for j in range(taille)]
    
    
    commence=''
    while(commence!='1' and commence!='2'): 
        commence=input("Qui commence ?  1-IA  2-Vous \n")
        
    interface(grillee)
    
    if commence=='2':
        grillee = caseprise(grillee)
    else : 
        grillee[3][7]=1
    interface(grillee)
    
    if commence=='2':
        AlgoMinMax(grillee,p1,-INF,INF)
    else : 
        grillee=caseprise(grillee)
    interface(grillee)

    if commence=='2': 
        grillee=caseprise(grillee)
    else: 
        AlgoMinMax(grillee,p1,-INF,INF)
    interface(grillee)
    
    fin=[False,0]
    while(fin[0]==False) :
        if commence=='1' :
            grillee=caseprise(grillee)
            interface(grillee)
            fin=Jeutermine(grillee)
        if fin[0] : 
            break
        
        AlgoMinMax(grillee,p1,-INF,INF)
        interface(grillee)
        fin=Jeutermine(grillee)
        if fin[0] : 
            break

        if commence=='2' :
            grillee=caseprise(grillee)
            interface(grillee)        
    if(fin[1]==1) : 
        print("Vainqueur : IA")
    elif(fin[1]==-1) : 
        print("Vainqueur : joueur") 
    else : 
        print("Match nul")

Debutjeu()

