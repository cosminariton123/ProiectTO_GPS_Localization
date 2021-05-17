from functii_ajutatoare import *





def GPS_SLS(x,a,d,pasi_acuratete):
    STANGA, DREAPTA = -300, 300
    assert verificare_asumption_matrice(a) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(a) >= len(x) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"

    B = generare_B(a, d)
    b =generare_b(a, d)
    D = generare_D(len(x))
    g = generare_g(len(x))
    A_caciula = generare_A_caciula(a)
    E = generare_E(len(x))
    w = generare_w(A_caciula, d, len(x))

    beta = generare_beta(A_caciula, d, E)                             #Folosit pentru verificarea unor existente prin assert-uri
    lambda_caciula = cautare_lambda_caciula(B, D, A_caciula, d, w)    #Folosit pentru verificarea unor existente
    lambda_star, puncte_pentru_convergenta = metoda_bisectiei(fi, B, D, b, g, STANGA, DREAPTA, pasi_acuratete)
    xsls = y(lambda_star, B, D, b, g)[0:len(x)]
    return xsls


def GPS_SLS_afisare_convergenta(x, a, d, pasi_acuratete, x_true, nr_figura):

    STANGA, DREAPTA, DISCRETIZARE = -100, 100, 10**3

    assert verificare_asumption_matrice(a) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(a) >= len(x) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"
    
    B = generare_B(a, d)
    b =generare_b(a, d)
    D = generare_D(len(x))
    g = generare_g(len(x))
    A_caciula = generare_A_caciula(a)
    E = generare_E(len(x))
    w = generare_w(A_caciula, d, len(x))

    x_discretizare = np.linspace(STANGA, DREAPTA, DISCRETIZARE)

    y_discretizare = list()
    for elem in x_discretizare:
        y_discretizare.append( fi(elem, B, D, b, g))
        

    plt.figure(nr_figura)
    plt.plot(x_discretizare, y_discretizare, label = 'fi(x)')
    plt.hlines(xmin = STANGA, xmax = DREAPTA, y=0, color = 'black')
    plt.title('Descresterea funtiei fi(x)')
    nr_figura +=1

    metoda_bisectiei_grafica(fi, B, D, b, g, STANGA, DREAPTA, pasi_acuratete)
    #nr_figura += 1

    lambda_star, puncte_pentru_convergenta = metoda_bisectiei(fi, B, D, b, g, STANGA, DREAPTA, pasi_acuratete)

    puncte_convergenta_plotare = list()
    for punct in puncte_pentru_convergenta:
        puncte_convergenta_plotare.append(y(punct, B, D, b, g)[0:len(x)])

    plt.figure(nr_figura)

    nr_sateliti = len(a)
    n_spatiu = len(x)

    plt.title("Convergenta metodei GPS_SLS pentru o rulare la intamplare\n" + "Numarul satelitilor: " + str(nr_sateliti) + "\nSpatiul n = "+ str(n_spatiu))
    lista_pt_plot = list()
    for elem in puncte_convergenta_plotare:
        lista_pt_plot.append(np.linalg.norm(elem - x_true) )

    plt.plot(range(len(lista_pt_plot)) , lista_pt_plot, linewidth = 3, label = "evolutia diferentei fata de x-ul real", color = 'magenta')
    plt.legend()

    nr_figura +=1


    return nr_figura


def GPS_SLS_histograma_erorilor(x, a,  pasi_acuratete, x_true):
    generari = 50
    B = list()


    assert verificare_asumption_matrice(a) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(a) >= len(x) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"

    for i in range(generari):
        #x_true = [random.random() * (10 - (-10)) + -10 , random.random() * (10 - (-10)) + -10 ]
        #x_true = np.array(x_true)

        d = generare_di(x_true, a)
        B.append(np.linalg.norm(GPS_SLS(x, a, d, pasi_acuratete) - x_true))


    nr_sateliti = len(a)
    n_spatiu = len(x)
    
    plt.hist(B, bins = 13, ec='black', color='magenta')
    plt.title("Histograma erorilor GPS_SLS\n" + "Numarul satelitilor: " + str(nr_sateliti) + "\nSpatiul n = "+ str(n_spatiu))


def GPS_SLS_random(nr_figura):

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


    contor = 0
    for contor in range(1, 300):
        print(str(contor)+' Incercari convergenta')
        try:
            nr_figura = GPS_SLS_afisare_convergenta(x, a, d, pasi_acuratete, x_true, nr_figura)
        except AssertionError:
            continue
        break


    nr_figura +=1
    plt.figure(nr_figura)
   
    contor = 0
    for contor in range(1, 15):
        print(str(contor)+' Incercari histograma')
        try:
            GPS_SLS_histograma_erorilor(x, a, pasi_acuratete, x_true)
        except AssertionError:
            continue
        break

    print("################REZULTATE PENTRU SPATIU SI SATELITI GENERATI RANDOM GPS_SLS#############")
    print("Nr sateliti: " + str(nr_sateliti))
    print("Spatiul n = " + str(n))

    return nr_figura
    