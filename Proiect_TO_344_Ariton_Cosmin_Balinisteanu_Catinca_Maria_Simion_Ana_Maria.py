import numpy as np
from GPS_LS import *
from CF_LS import *
from GPS_SLS import *





def exemplul_5_2():

    nr_figura = 0
    NR_PROCESOARE = 12
    STANGA, DREAPTA = -50, 40

    x = np.array([-10, 5])
    a = np.array([[-29, -18], [7, -24], [-19, -27], [10, -27], [-9, 3], [-33, -34]])
    x_true = np.array([-8, -2])
    pasi_acuratete = 10**2
    d = generare_di(x_true, a)
    

    x_gasit =  fixed_point_GPS_LS(x, a, d, pasi_acuratete)
    x_gasit_sls = GPS_SLS(x, a, d, pasi_acuratete)

    print("x-ul gasit prin metoda GPS_LS: " +str(x_gasit))
    print("x-ul gasit prin metoda GPS_SLS: " +str(x_gasit_sls))
 

    plt.figure(nr_figura)
    nr_figura += 1
    fixed_point_GPS_LS_afisare_convergenta(x, a, d, pasi_acuratete, x_true)
    plt.figure(nr_figura)
    nr_figura += 1
    fixed_point_GPS_LS_histograma_erorilor(x, a, pasi_acuratete, x_true)


    plt.figure(nr_figura)
    nr_figura = GPS_SLS_afisare_convergenta(x, a, d, pasi_acuratete, x_true, nr_figura)
    nr_figura += 1
    plt.figure(nr_figura)


    while True:
        try:
            GPS_SLS_histograma_erorilor(x, a, pasi_acuratete, x_true)
        except AssertionError:
            continue
        break
    
    nr_figura += 1
    


    vector1 = np.linspace(STANGA, DREAPTA, 10**1)
    vector2 = np.linspace(STANGA, DREAPTA, 10**1)

    vector1, vector2 = np.meshgrid(vector1,vector2)

    z = list()
    for liniex, liniey in zip(vector1,vector2):
        aux = list()
        for elemx, elemy in zip (liniex, liniey):
            aux.append([elemx, elemy])
        
        daux = generare_di(x_true, aux)

        z.append(daux)
    z= np.array(z)


    plt.figure(nr_figura)
    nr_figura += 1
    ax = plt.axes(projection = '3d')
    plt.contour(vector1,vector2,z, 50)
    ax.scatter(x_true[0], x_true[1], 0, color='green', label='Punctul de minim x_true')

    ax.scatter(a[0][0], a[0][1], d[0], color='red', label = 'Satelitii')
    for ai, di in zip(a[1:], d[1:]):
        ax.scatter(ai[0], ai[1], di , color = 'red')

    

    aux = [[x_gasit[0], x_gasit[1]], [0, 0]]
    daux = generare_di(x_true, aux)
    daux = np.array(daux)
    ax.scatter(x_gasit[0], x_gasit[1], daux[0], color='blue', label= 'Punctul de optim estimat GPS_LS')
    ax.scatter(x_gasit_sls[0], x_gasit_sls[1], daux[0], color='magenta', label= 'Punctul de optim estimat GPS_SLS')
    plt.title("Reprezentare 3D a minimizarii\n" + "Eroarea pentru GPS_LS este de: " + str(np.linalg.norm(x_true - x_gasit)) + "\nEroarea pentru GPS_SLS este de: " +str(np.linalg.norm(x_true - x_gasit_sls)))
    plt.legend()
    plt.show()



if __name__ == '__main__':

    print("########     Exemplul 5_2    ##########")
    exemplul_5_2()
    exemplul_5_3()


    print('\n')
    nr_figura = 0
    nr_figura = fixed_point_GPS_LS_random(nr_figura)
    nr_figura = nr_figura + 1
    print('')
    nr_figura = GPS_SLS_random(nr_figura)
    nr_figura = nr_figura + 1
    plt.legend()
    plt.show()


    fixed_point_GPS_LS_random_x0_ales()
    nr_figura = nr_figura + 1
    fixed_point_GPS_LS_random_influenta_punctului_de_start()

