from GPS_LS import *
from CF_LS import *


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




    vector1 = np.linspace(-30, 20, 10**1)
    vector2 = np.linspace(-30, 20, 10**1)

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
    ax.scatter(x_true[0], x_true[1], 0, color='red', label='Punctul de minim x_true')

    x_gasit =  fixed_point_GPS_LS(x, a, d, pasi_acuratete)

    aux = [[x_gasit[0], x_gasit[1]], [0, 0]]
    daux = generare_di(x_true, aux)
    daux = np.array(daux)
    ax.scatter(x_gasit[0], x_gasit[1], daux[0], color='blue', label= 'Punctul de optim estimat')
    plt.title("Functia care trebuie minimizata GPS_LS\n" + "Eroarea este de: " + str(np.linalg.norm(x_true - x_gasit)))
    plt.legend()
    plt.show()



if __name__ == '__main__':

    exemplul_5_2()
    exemplul_5_3()
    fixed_point_GPS_LS_random()
    fixed_point_GPS_LS_random_x0_ales()
    fixed_point_GPS_LS_random_influenta_punctului_de_start()