import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import multiprocessing

######## FUNCTII PT GENERARE DI ##########

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
        
        r = norm(0, 10)
        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
        di = np.array(di)

    return di

#def generare_di_ce_returneaza_si_r(x, ai):
#
#    r = norm(0, 10)
#
#    di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
#    di = np.array(di)
#
#    while verificare_vector_di(di) == False or r < 0:
#        
#        r = norm(0, 10)
#        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
#        di = np.array(di)
#
#    return di, r



######### FUNCTII PT GPS_LS si CF_LS ##########


def r(x, ai, di):
    m = len(ai)
    
    vec = [np.linalg.norm(x - a) for a in ai]

    vec = vec - di

    rez = 1/m * sum(vec)
    

    #rez = np.abs(rez)
    #rez = np.floor(rez)
    rez = max(0, rez)

    return rez


def T(x, ai, di):
    
    m = len(ai)

    vec = [np.linalg.norm(x - a) for a in ai]

    vec = [ix / a for ix,a in zip(x-ai, vec)]

    factor_stang = r(x,ai,di) + di

    vec = [a * b for a,b in zip(factor_stang,vec)]

    return 1/m * sum(ai) + 1/m * sum(vec)



def generare_A_caciula(a):

    A_caciula = list()

    for elem in a:    
        linie = list()
        for pozitie in elem:
            linie.append(2*pozitie)
        linie.append(-1)

        linie = np.array(linie)
        A_caciula.append(linie)

    A_caciula = np.array(A_caciula)
    return A_caciula



def verificare_asumption_matrice(a):

    A_caciula = generare_A_caciula(a)

    A_caciula = np.transpose(A_caciula)

    iter1 = -1

    for linie1 in A_caciula:
        iter1 += 1

        iter2 = -1
        for linie2 in A_caciula:
            iter2 += 1

            if iter1 != iter2:
                
                aux = linie1 / linie2

                flag = True
                for elem1 in aux:
                    for elem2 in aux:
                        if elem1 != elem2:
                            flag = False

                if flag == True:
                    return False
    
    return True




############ FUNCTII PT GPS_SLS #############



def generare_B(a, d):

    B = list()

    for ai, di in zip(a, d):
        
        aux = list()
        for elem in ai:
            aux.append(2*elem)
        
        aux.append(-1)
        aux.append(2*di)

        B.append(aux)
    
    B= np.array(B)

    return B


def generare_b(a, d):
    
    b = list()

    b = [np.linalg.norm(ai)**2 - di**2 for ai, di in zip(a,d)]
    b = np.array(b)

    return b



def generare_In(n):

    In = generare_On(n)

    for i in range(n):
        for j in range(n):
            if i == j:
                In[i][j] = 1

    return In

def generare_On(n):
    
    return [[0 for i in range(n)] for i in range(n)]


def generare_D(n):
    
    D = generare_In(n)

    for linie in D:
        linie.append(0)
        linie.append(0)

    D.append([0 for i in range(n+2)])
    D.append([0 if i < n+1 else -1 for i in range(n+2)])

    D = np.array(D)

    return D

def generare_g(n):
    

    linie = [0 for i in range(n)]
    linie.append(1)
    linie.append(0)

    linie = np.array(linie)
    linie = 1/2 * linie
    
    return linie





def generare_E(n):

    E = generare_In(n)

    for linie in E:
        linie.append(0)
    
    E.append([0 for i in range(n+1)])
    
    E = np.array(E)

    return E



def verificare_apartinere_range(matrice, b):

    m = len(matrice)
    n = len(matrice[0])

    for i in range(m - n + 2):
        aux = [liniuta for liniuta in matrice[i:i+n-1]]

        indice_linie_curenta = -1
        for linie in matrice:
            indice_linie_curenta += 1

            if indice_linie_curenta not in range(i, i+n-1):
                aux.append(linie)

                rang = np.linalg.matrix_rank(aux)
                be = copy.deepcopy(b[i: i+n-1])
                be = list(be)
                be.append(b[indice_linie_curenta])

                flag = False
                for coloana in range(n):
                    extinsa = copy.deepcopy(aux)
                    extinsa = np.array(extinsa)
                    
                    extinsa[:,coloana] = np.array(be)

                    if np.linalg.matrix_rank(extinsa) == rang :
                        flag = True
                
                if flag == False:
                    return False

                aux.pop(len(aux)-1)

    return True



def generare_w(A_caciula, d, n):
    rez = np.linalg.inv((np.transpose(A_caciula) @ A_caciula)) @ np.transpose(A_caciula) @ d
    
    return rez[0:n]


def generare_beta(A_caciula, d,  E):
    rez = E @ np.linalg.inv((np.transpose(A_caciula) @ A_caciula)) @ np.transpose(A_caciula) @ d
    
    return rez


def cautare_lambda_caciula(B, D, A_caciula, d, w):

    lambda_caciula = None

    conditie = np.linalg.norm(w) - 1/2

    assert  verificare_apartinere_range(A_caciula, d) == False or conditie != 0 , "Nu se poate afla lambda deoarece d apartine range(A_caciula) si ||w|| = 1/2"

    if verificare_apartinere_range(A_caciula, d) == False:
        return 0


    conditie = np.linalg.norm(w) - 1/2

    if conditie > 0:
        lambda_caciula = 1
    elif conditie < 0 :
        lambda_caciula = -1
    
    while True:
        G = np.transpose(B)@B + lambda_caciula * D

        flag = True
        for elem in np.linalg.eigvals(G):
            if elem <= 0:
                flag = False
        
        if flag == True:
            return lambda_caciula
        
        lambda_caciula = lambda_caciula / 2


def y(lamb, B, D, b, g):
    
    return np.linalg.inv( np.transpose(B) @ B + lamb * D )    @   (np.transpose(B)@b + lamb * g)


def fi(lamb, B, D, b, g):
    return np.transpose(y(lamb, B, D, b, g)) @ D @ y(lamb, B, D, b, g) - 2 * np.transpose(g) @ y(lamb, B, D, b, g)



def metoda_bisectiei_grafica(f, B, D, b, g, stanga, dreapta, pasi_acuratete):

    N = pasi_acuratete

    plt.plot(stanga, f(stanga, B, D, b, g), 'o', color = 'green', label = 'punctele de start ale metodei bisectiei')
    plt.plot(dreapta, f(dreapta, B, D, b, g), 'o', color = 'green')

    flag_afisare_label = True


    if f(stanga, B, D, b, g) == 0:   #verificam capetele intervalului
        plt.plot(stanga, f(stanga, B, D, b, g), 'bo', label ='radacina unica gasita')
        return stanga
    elif f(dreapta, B, D, b, g) == 0:
        plt.plot(dreapta, f(dreapta, B, D, b, g), 'bo', label ='radacina unica gasita')
        return dreapta
    else:

        assert f(stanga, B, D, b, g) * f(dreapta, B, D, b, g) <= 0 , "Eroare, nu exista radacina la care sa convearga metoda bisectiei"

        for i in range(0,N):        #implementarea metodei bisectiei
            xk = (stanga+dreapta)/2

            if f(xk, B, D, b, g)==0: 
                plt.plot(xk, f(xk, B, D, b, g), 'bo', label ='radacina unica gasita')
                return xk

            elif f(xk, B, D, b, g) * f(dreapta, B, D, b, g) < 0:      #restrangem intervalul a si b in care cautam. verificam ce jumatate a intervalului initial sa pastram cu
                stanga = xk                  #Teorema valorilor intermediare (Darboux) din care scoatem f(t)*f(u)<0 => exista o radacina in intervalul [t,u]
                
                if flag_afisare_label == True:
                    plt.plot(xk, f(xk, B, D, b, g),'o', color='red', label='Pasii metodei bisectiei')
                    flag_afisare_label = False
                else:
                    plt.plot(xk, f(xk, B, D, b, g),'o', color='red')

            elif f(xk, B, D, b, g) * f(stanga, B, D, b, g) < 0 :
                dreapta= xk
                if flag_afisare_label == True:
                    plt.plot(xk, f(xk, B, D, b, g), 'o', color='red', label='Pasii metodei bisectiei')
                    flag_afisare_label = False
                else:
                    plt.plot(xk, f(xk, B, D, b, g), 'o', color='red')

        plt.plot((stanga+dreapta)/2, f((stanga+dreapta)/2, B, D, b, g), 'bo', label ='radacina unica gasita')
        return    (stanga+dreapta)/2




def metoda_bisectiei(f, B, D, b, g, stanga, dreapta, pasi_acuratete):

    N = pasi_acuratete 

    puncte_pentru_convergenta = list()

    #poate sterg
    puncte_pentru_convergenta.append(stanga)
    puncte_pentru_convergenta.append(dreapta)
    #end-poate sterg

    if f(stanga, B, D, b, g) == 0:   #verificam capetele intervalului
        return stanga, puncte_pentru_convergenta
    elif f(dreapta, B, D, b, g) == 0:
        return dreapta, puncte_pentru_convergenta
    else:

        assert f(stanga, B, D, b, g) * f(dreapta, B, D, b, g) <= 0 , "Eroare, nu exista radacina la care sa convearga metoda bisectiei"

        for i in range(0,N):        #implementarea metodei bisectiei
            xk = (stanga+dreapta)/2

            if f(xk, B, D, b, g)==0: 
                puncte_pentru_convergenta.append(xk)
                return xk, puncte_pentru_convergenta

            elif f(xk, B, D, b, g) * f(dreapta, B, D, b, g) < 0:      #restrangem intervalul a si b in care cautam. verificam ce jumatate a intervalului initial sa pastram cu
                stanga = xk                  #Teorema valorilor intermediare (Darboux) din care scoatem f(t)*f(u)<0 => exista o radacina in intervalul [t,u]
                
                puncte_pentru_convergenta.append(xk)

            elif f(xk, B, D, b, g) * f(stanga, B, D, b, g) < 0 :
                dreapta= xk
                puncte_pentru_convergenta.append(xk)

        puncte_pentru_convergenta.append((stanga+dreapta)/2)
        return    (stanga+dreapta)/2, puncte_pentru_convergenta

############### FUNCTII PT x0 OPTIM PENTRU GPS_LS FOLOSIND GPS_SLS ##################

"""alg pag 22 +  lema 5.1 pagina 21 
Find x0 satisfying : f(x0) < min {f(a1), ..f(an), fliminf }
f_liminf = np.
"""

def h(x,ai,di,j):
    m = len(ai) -1
    copy_ai = ai
    copy_ai= np.delete(ai,j)
    vec = [np.linalg.norm(x - a) for a in copy_ai]
    vec = sum(vec)
    vec = vec/m
    return m

def g(x,ai,di,j):
    m = len(ai) -1
    copy_ai = ai
    copy_ai= np.delete(ai,j)
    copy_di = di
    copy_di = np.delete(di,j)
    vec = [np.linalg.norm(x-a) for a in copy_ai]
    vec = vec - copy_di
    vec =  vec^2
    vec = sum(vec)
    return vec

def f(x,ai,di):
    m = len(ai)
    
    vec = [np.linalg.norm(x - a) for a in ai]

    vec = (vec - di)
    vec = np.square(vec)
    vec = sum(vec)

    vec = vec - m * r(x,ai,di)**2
   
    return vec


"""Gaseste x0 optim pentru GSP LS : """

def find_x0(ai,di):
    m = len(ai)
    f_liminf = np.zeros_like(ai[0])  ## gresit!!! nu stiu cum 
    vec = [f(a,ai,di) for a in ai]
    minn = min(vec)
    if np.less(f_liminf,minn).all():
        x0 = f_liminf  ### gresit !!!!  x0 = x_sls  => nu stiu cine e 
        return x0
    
    p = vec.index(minn)
    a_p = vec[p]
    if r(ai[p]) > 0 :
        z1 =  - np.gradient(g(a_p,ai,di,p)) + 2 * m * r(a_p) * np.gradiend(h(a_p,ai,di,p))
        if z1 != 0:
            v = z1/np.linalg.norm(z1)
        else:
            v = np.random.randn(*z1.shape)
            norm = np.linalg.norm(v)
            v = v/norm # v = any normalized vector
    else:
        z = np.gradient(g(a_p,ai,di,p))
        if z != 0 :
            v= - z/np.linalg.norm(z)
        else:
            v = np.random.randn(*z.shape)
            norm = np.linalg.norm(v)
            v = v/norm # v = any normalized vector
    
    s = 1 
    while f(a_p + s*v) >= f(a_p):
        s = s/2
    
    xo = a_p + s*v
    return x0