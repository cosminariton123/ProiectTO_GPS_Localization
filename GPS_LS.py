from functii_ajutatoare import *
import numpy as np
import matplotlib.pyplot as plt
import random



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


def fixed_point_GPS_LS_histograma_erorilor_influentat_de_x_initial(x, a,d,  pasi_acuratete, x_true, INTERVAL_STANGA, INTERVAL_DREAPTA, n):
    generari = 10**3
    B = list()

    for i in range(generari):
        B.append(np.linalg.norm(fixed_point_GPS_LS(x, a, d, pasi_acuratete) - x_true))
        x = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])


    
    plt.hist(B, bins = 13, ec='black', color='magenta')
    plt.title("Histograma erorilor GPS_LS in functie de x-ul initial")



def exemplul_5_2():

    nr_figura = 0

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



def fixed_point_GPS_LS_random():
    nr_figura = 0

    NR_MAXIM_DIMENSIUNI = 10
    NR_MAXIM_SATELITI = 20
    INTERVAL_STANGA = -10
    INTERVAL_DREAPTA = 10

    n = random.randint(2, NR_MAXIM_DIMENSIUNI)

    nr_sateliti = 0

    while nr_sateliti < n+1:
        nr_sateliti = random.randint(0,NR_MAXIM_SATELITI)

    x = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])

    a = list()
    for elem in range(nr_sateliti):
        a.append(np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)]))
    
    a= np.array(a)

    x_true = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])
    pasi_acuratete = 10**2
    d = generare_di(x_true, a)


    plt.figure(nr_figura)
    fixed_point_GPS_LS_histograma_erorilor(x, a, pasi_acuratete, x_true)
    nr_figura +=1
    plt.figure(nr_figura)
    fixed_point_GPS_LS_afisare_convergenta(x, a, d, pasi_acuratete, x_true)

    print("################REZULTATE PENTRU SPATIU SI SATELITI GENERATI RANDOM#############")
    print("Nr sateliti: " + str(nr_sateliti))
    print("Spatiul n = " + str(n))
    
    plt.legend()
    plt.show()



def fixed_point_GPS_LS_random_influenta_punctului_de_start():

    nr_figura = 0

    NR_MAXIM_DIMENSIUNI = 10
    NR_MAXIM_SATELITI = 20
    INTERVAL_STANGA = -10
    INTERVAL_DREAPTA = 10

    n = random.randint(2, NR_MAXIM_DIMENSIUNI)

    nr_sateliti = 0

    while nr_sateliti < n+1:
        nr_sateliti = random.randint(0,NR_MAXIM_SATELITI)

    x = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])

    a = list()
    for elem in range(nr_sateliti):
        a.append(np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)]))
    
    a= np.array(a)

    x_true = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])
    pasi_acuratete = 10**2
    d = generare_di(x_true, a)


    plt.figure(nr_figura)
    fixed_point_GPS_LS_histograma_erorilor_influentat_de_x_initial(x, a, d, pasi_acuratete, x_true, INTERVAL_STANGA, INTERVAL_DREAPTA, n)

    print("################REZULTATE PENTRU SPATIU SI SATELITI GENERATI RANDOM AVAND IN VEDERE SCOATEREA IN EVIDENTA A RELEVANTEI ALEGERII PUNCTULUI INITIAL#############")
    print("Nr sateliti: " + str(nr_sateliti))
    print("Spatiul n = " + str(n))


    plt.show()