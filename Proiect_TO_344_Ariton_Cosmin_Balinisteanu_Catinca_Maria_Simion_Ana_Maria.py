import numpy as np
import matplotlib.pyplot as plt

def r(x, ai, di):
    m = len(x)
    
    vec = [np.linalg.norm(x - a) for a in ai]

    vec = vec - di

    rez = 1/m * sum(vec)
    
    return rez


def T(x, ai, di):
    
    m = len(x)

    vec = [np.linalg.norm(x - a) for a in ai]

    vec = [ix / a for ix,a in zip(x-ai, vec)]

    factor_stang = r(x,ai,di) + di

    vec = [a * b for a,b in zip(factor_stang,vec)]

    return 1/m * sum(ai) + 1/m * sum(vec)

def fixed_point_GPS_LS(xk, ai, di):

    for i in range(2):
        xk = T(xk, ai, di)
    return xk

def x_a_pe_norm(xk, ai):
    
    rez = list()
    for a in ai:
        rez.append(xk-a / np.linalg.norm(xk-a))
    
    return rez

def CF_LS_step(xk, ai, di):
    m = len(x)
    vec = [np.linalg.norm(x - a) for a in ai]


    
    rez = 1/m * sum(ai + r(xk, ai, di)) *  ( 1/m   *  sum(x_a_pe_norm(xk, ai))  )
    return rez

def fixed_point_CF_LS(xk, ai , di):
    
    for i in range(2):

        xk = CF_LS_step(xk, ai, di)
    
    return xk

def verificare_asumption_matrice(a):
    for elem in a:
        if (np.transpose(elem) * 2 - 1).all() == 0:
            return False
    
    return True

if __name__ == '__main__':

    a = np.array([[-0.89, 1.00], [-0.62, -0.04], [-0.87, 0.63], [1.21, -0.42], [-1.86, 1.00]])
    x = np.array([3, 3])


    assert verificare_asumption_matrice(a) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(a) >= len(x) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"
    #Ecuatia lui di, in cazul nostru di este stiut, trebuie aflat x-ul
    #r = 1.4
    #di = [np.linalg.norm(x-ai)- r for ai in a]

    #pentru exemplul nostru
    d = np.array([2.90, 1.70, 1.76, 1.77, 2.71])



    #print(fixed_point_CF_LS(x,a,d))
    #print(fixed_point_GPS_LS(x, a, d))


    a = np.array([[10, 10], [20, 30], [40, 55]])
    x = np.array([0, 0])
    d = np.array([2, 3, 5])
    assert verificare_asumption_matrice(a) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(a) >= len(x) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"

