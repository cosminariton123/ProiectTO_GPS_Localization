from matplotlib.markers import MarkerStyle
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
        
        r = norm(0, 10)
        di = [np.linalg.norm(x-a) - r + norm(0, 1) for a in ai]
        di = np.array(di)

    return di

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

def fixed_point_GPS_LS(xk, ai, di, pasi_acuratete):

    assert verificare_asumption_matrice(ai) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(ai) >= len(xk) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"


    for i in range(pasi_acuratete):
        xk = T(xk, ai, di)
    return xk


def fixed_point_GPS_LS_afisare_convergenta(xk, ai, di, pasi_acuratete, x_true):

    plt.title("Convergenta metodei GPS_LS pentru o rulare la intamplare")
    lista_pt_plot = list()
    for i in range(pasi_acuratete):
        xk = T(xk, ai, di)
        lista_pt_plot.append(np.linalg.norm(xk - x_true) )

    plt.plot(range(pasi_acuratete) , lista_pt_plot, linewidth = 3, label = "evolutia diferentei fata de x-ul real", color = 'magenta')
    plt.legend()

def fixed_point_GPS_LS_histograma_erorilor(x, a,  pasi_acuratete, x_true):
    generari = 10**3
    B = list()

    for i in range(generari):
        #x_true = [random.random() * (10 - (-10)) + -10 , random.random() * (10 - (-10)) + -10 ]
        #x_true = np.array(x_true)

        d = generare_di(x_true, a)
        B.append(np.linalg.norm(fixed_point_GPS_LS(x, a, d, pasi_acuratete) - x_true))


    
    plt.hist(B, bins = 13, ec='black', color='magenta')
    plt.title("Histograma erorilor GPS_LS")



def CF_LS_step(xk, ai, di):
    m = len(ai)
    vec = [np.linalg.norm(xk - a) for a in ai]


    vec = [elem / elemvec for elem, elemvec in zip(xk-ai, vec)]

    vec = sum(vec)

    vec = 1/m * vec

    vec = np.floor(vec)

    vec = vec * r(xk, ai, di)

    vec = vec + sum(ai) * 1/m
   
    return vec

def fixed_point_CF_LS(xk, ai , di, pasi_acuratete):
    
    for i in range(pasi_acuratete):

        xk = CF_LS_step(xk, ai, di)
    
    return xk

def verificare_asumption_matrice(a):
    for elem in a:
        for elem2 in (np.transpose(elem) * 2 - 1):
            if elem2 == 0 :
                return False
    
    return True


def exemplul_5_2(nr_figura):

    x = np.array([-10, 5])
    a = np.array([[-29, -18], [7, -24], [-19, -27], [10, -27], [-9, 3], [-33, -34]])
    x_true = np.array([-8, -2])
    pasi_acuratete = 10**2
    d = generare_di(x_true, a)
    

 

    plt.figure(nr_figura)
    nr_figura += 1
    fixed_point_GPS_LS_afisare_convergenta(x, a, d, pasi_acuratete, x_true)
    plt.figure(nr_figura)
    nr_figura += 1
    fixed_point_GPS_LS_histograma_erorilor(x, a, pasi_acuratete, x_true)




    a = np.linspace(-30, 20, 10**1)
    b = np.linspace(-30, 20, 10**1)

    x, y = np.meshgrid(a,b)

    z = list()
    for liniex, liniey in zip(x,y):
        aux = list()
        for elemx, elemy in zip (liniex, liniey):
            aux.append([elemx, elemy])
        
        daux = generare_di(x_true, aux)

        z.append(daux)
    z= np.array(z)


    plt.figure(nr_figura)
    nr_figura += 1
    ax = plt.axes(projection = '3d')
    plt.contour(x,y,z, 50)
    ax.scatter(x_true[0], x_true[1], 0, color='red', label='Punctul de minim x_true')
    plt.title("Functia care trebuie minimizata GPS_LS")
    plt.legend()
    plt.show()
    
    

def exemplul_5_3():
    x = np.array([3, -7])
    a = np.array([[1, 9], [ 2, 7], [5, 8], [7, 7], [9, 5], [3, 7]])
    x_true = np.array([0, -8])
    pasi_acuratete = 5
    d = generare_di(x_true, a)
    #d = [0 for i in a]
    #d = np.array(d)


    fig, axes = plt.subplots()
    axes.set_aspect(1)

    axes.set_xlim([-50, 50])
    axes.set_ylim([-50, 50])

    for satelit in a:
        plt.plot(satelit[0], satelit[1], 'ro')


    x_gasit_optim = fixed_point_CF_LS(x, a, d, pasi_acuratete)


    plt.plot(x_gasit_optim[0], x_gasit_optim[1],'bo',  label = 'Centrul cercului gasit prin CF_LS' ,markersize = 3)
    plt.plot(x_true[0], x_true[1], 'mo', label = 'Centrul real al cercului', markersize = 5)

    draw_circle = plt.Circle((x_gasit_optim[0], x_gasit_optim[1]), r(x_gasit_optim, a, d),fill=False, lw = 3)
    axes.add_artist(draw_circle)

    plt.title('Circle fitting LS\n ' + 'distanta fata de punctul de optim :' + str( np.linalg.norm( fixed_point_CF_LS(x, a, d, pasi_acuratete)- x_true)))

    plt.legend()
    plt.show()


if __name__ == '__main__':

    nr_figura = 0

    exemplul_5_2(nr_figura)

    exemplul_5_3()