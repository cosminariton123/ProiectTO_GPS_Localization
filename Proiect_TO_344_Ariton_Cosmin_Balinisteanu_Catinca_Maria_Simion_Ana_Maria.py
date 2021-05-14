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



if __name__ == '__main__':

    exemplul_5_2()
    exemplul_5_3()
    fixed_point_GPS_LS_random()
    fixed_point_GPS_LS_random_influenta_punctului_de_start()