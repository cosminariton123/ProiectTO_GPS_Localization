import numpy as np
import matplotlib.pyplot as plt
import random

def exponentiala(lamb):
    u = random.random()
    
    return - 1/lamb * np.log(u)


def norm(miu, sigma):

    while True:
        y = exponentiala(1)

        u1 = random.random()
        u2 = random.random()

        if u1 <= np.exp(- ((y-1)**2)/2 ): 
            x = y
            if u2 <= 1/2:
                x = -np.abs(x)
                return miu + sigma*x
            else:
                x = np.abs(x)
                return miu + sigma* x



def verificare_vector_di(di):

    for elem in di:
        if elem < 0:
            return False
    
    return True

def generare_di(x, ai):

    r = norm(0, 10)

    di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
    di = np.array(di)

    while verificare_vector_di(di) == False or r < 0:
        
        r = norm(0, 20)
        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
        di = np.array(di)

    return di

def generare_di_ce_reurneaza_si_r(x, ai):

    r = norm(0, 10)

    di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
    di = np.array(di)

    while verificare_vector_di(di) == False or r < 0:
        
        r = norm(0, 10)
        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
        di = np.array(di)

    return di, r


def r(x, ai, di):
    m = len(ai)
    
    vec = [np.linalg.norm(x - a) for a in ai]

    vec = vec - di

    rez = 1/m * sum(vec)
    

    rez = np.abs(rez)
    rez = np.floor(rez)

    return rez


def T(x, ai, di):
    
    m = len(ai)

    vec = [np.linalg.norm(x - a) for a in ai]

    vec = [ix / a for ix,a in zip(x-ai, vec)]

    factor_stang = r(x,ai,di) + di

    vec = [a * b for a,b in zip(factor_stang,vec)]

    return 1/m * sum(ai) + 1/m * sum(vec)



def verificare_asumption_matrice(a):
    for elem in a:
        for elem2 in (np.transpose(elem) * 2 ):
            if elem2 == 0 :
                return False
    
    return True




def generare_B(a, d):
    m = len(a)
    B = list()

    for i in range(m):
        aux = [2* np.transpose(a[i]) , -1 , 2* d[i]]
        B.append(aux)
    
    B= np.array(B)

    return B


def generare_b(a, d):
    
    m = len(a)
    b = list()

    b = [np.linalg.norm(ai)**2 - di**2 for ai, di in zip(a,d)]
    b = np.array(b)

    return b

#def generare_y(a, d):
