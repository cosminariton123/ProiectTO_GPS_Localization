from functii_ajutatoare import *
from GPS_SLS import *
from scipy.optimize import basinhopping, approx_fprime

def fixed_point_GPS_LS(xk, ai, di, pasi_acuratete):

    assert verificare_asumption_matrice(ai) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(ai) >= len(xk) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"


    for i in range(pasi_acuratete):
        xk = T(xk, ai, di)
    return xk


def fixed_point_GPS_LS_afisare_convergenta(xk, ai, di, pasi_acuratete, x_true):

    nr_sateliti = len(ai)
    n_spatiu = len(xk)

    plt.title("Convergenta metodei GPS_LS pentru o rulare la intamplare\n" + "Numarul satelitilor: " + str(nr_sateliti) + "\nSpatiul n = "+ str(n_spatiu))
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


    nr_sateliti = len(a)
    n_spatiu = len(x)
    
    plt.hist(B, bins = 13, ec='black', color='magenta')
    plt.title("Histograma erorilor GPS_LS\n" + "Numarul satelitilor: " + str(nr_sateliti) + "\nSpatiul n = "+ str(n_spatiu))


def fixed_point_GPS_LS_histograma_erorilor_influentat_de_x_initial(x, a,d,  pasi_acuratete, x_true, INTERVAL_STANGA, INTERVAL_DREAPTA, n):
    generari = 10**3
    B = list()

    for i in range(generari):
        B.append(np.linalg.norm(fixed_point_GPS_LS(x, a, d, pasi_acuratete) - x_true))
        x = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])


    nr_sateliti = len(a)
    n_spatiu = len(x)
    
    plt.hist(B, bins = 13, ec='black', color='magenta')
    plt.title("Histograma erorilor GPS_LS in functie de x-ul initial\n" + "Numarul satelitilor: " + str(nr_sateliti) + "\nSpatiul n = "+ str(n_spatiu))





def fixed_point_GPS_LS_random(nr_figura):

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

    print("################REZULTATE PENTRU SPATIU SI SATELITI GENERATI RANDOM GPS_SLS#############")
    print("Nr sateliti: " + str(nr_sateliti))
    print("Spatiul n = " + str(n))
    

    return nr_figura



def fixed_point_GPS_LS_random_x0_ales():
    nr_figura = 0

    NR_MAXIM_DIMENSIUNI = 10
    NR_MAXIM_SATELITI = 20
    INTERVAL_STANGA = -10
    INTERVAL_DREAPTA = 10

    n = random.randint(2, NR_MAXIM_DIMENSIUNI)

    nr_sateliti = 0

    while nr_sateliti < n+1:
        nr_sateliti = random.randint(0,NR_MAXIM_SATELITI)


    a = list()
    for elem in range(nr_sateliti):
        a.append(np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)]))
    
    a= np.array(a)

    x_true = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])
    pasi_acuratete = 10**2
    d = generare_di(x_true, a)

    
    x = find_x0(a, d)

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






    ############### FUNCTII PT x0 OPTIM PENTRU GPS_LS FOLOSIND GPS_SLS ##################

"""alg pag 22 +  lema 5.1 pagina 21 
Find x0 satisfying : f(x0) < min {f(a1), ..f(an), fliminf }
f_liminf = np.
"""
from scipy.optimize import minimize
 
def function_liminf(z, a,d):
    m = len(a)

    A = np.transpose(a[0])
    for i in range(1,m):
        aux = np.transpose(a[i])
        A = np.vstack([A,aux])
  

    id_m = [1]
    for i in range(1,m):
        id_m = np.vstack([id_m,[1]])
   
    t3 =  np.add(np.matmul(A,z) , d )
    t1 = np.transpose(t3)
    t2 = id_m - np.matmul(id_m, np.transpose(id_m))/m
    return np.matmul(np.matmul(t1,t2),t3)

def constraint_liminf(z):
    return np.linalg.norm(z) - 1 


def constraint_liminf(z):
    return np.linalg.norm(z) - 1

def h(x,ai,di):
    j = np.where(arr=x)
    j = j[0]
    copy_ai = np.copy(ai)
    copy_ai= np.delete(ai,j)

    m = len(copy_ai) - 1

    vec = [np.linalg.norm(x - a) for a in copy_ai]
    vec = np.array(vec)
    vec = sum(vec)
    vec = vec/m
    return vec

def g(x,ai,di):
    j = np.where(ai==x)
    j = j[0]
   
    copy_ai = np.copy(ai)
    copy_ai= np.delete(ai,j)
    copy_di = np.copy(di)
    copy_di = np.delete(di,j)

    vec = [(np.linalg.norm(x-a) - d)**2 for a,d in zip(copy_ai,copy_di)]
    vec = np.array(vec)
    vec = sum(vec)
    return vec

def f(x,ai,di):
    m = len(ai)
    
    vec = [np.linalg.norm(x - a) - d for a,d in zip(ai,di)]

  
    vec = np.square(vec)
    vec = sum(vec)

    vec = vec - m * r(x,ai,di)**2
   
    return vec

"""Gaseste x0 optim pentru GSP LS : """

def find_x0(ai,di):
    INTERVAL_STANGA = -10
    INTERVAL_DREAPTA = 10
    m = len(ai)
    
    z0 = np.random.randn(*ai[0].shape)
    norm = np.linalg.norm(z0)
    z0 = z0/norm 

    n= len(ai[0])
    x0 = np.array([random.random() * (INTERVAL_DREAPTA - INTERVAL_STANGA) + INTERVAL_STANGA for i in range(n)])

    x_sls  = GPS_SLS(x0,ai,di,30)


    cons = {'type':'eq', 'fun': constraint_liminf}
    minimizer_kwargs = {"args":(ai,di),"constraints":cons}
    #f_liminf = minimize(fun = function_liminf,x0 = z0,args = (ai,di), constraints = cons)
    #f_liminf = f_liminf.x
    # pentru functia nonconvexa gaseste toate minimele locale, apoi alege minimul global
    f_liminf = basinhopping(func = function_liminf,x0 = z0, minimizer_kwargs = minimizer_kwargs )
    f_liminf = f_liminf.fun
    vec = [f(a,ai,di) for a in ai]

    minn = min(vec)

    if f_liminf < minn:
        x0 = x_sls ### modifica x0 = x_sls 
        return x0
    
    p = vec.index(minn)
    a_p = ai[p]
    if r(ai[p],ai,di) > 0 :
      
        z1 =  np.multiply(approx_fprime(a_p,g,1e-6,ai,di), (-1)) + np.multiply(approx_fprime(a_p,g,1e-6,ai,di), 2 * m * r(a_p,ai,di) )
        zero  = np.zeros_like(z1)
        
        if (z1==zero).all():
            v = np.random.randn(*ai[0].shape)

            norm = np.linalg.norm(v)
            v = v/norm # v = any normalized vector
        else:
          
            v = z1/np.linalg.norm(z1)
    else:
        z = np.gradient(g(a_p,ai,di))
        z = np.array(z)

        zero = np.zeros_like(z)
        
        if (z==zero).all():
            v = np.random.randn(*ai[0].shape)
            norm = np.linalg.norm(v)
            v = v/norm # v = any normalized vector
        else:
            v= (-1) * z/np.linalg.norm(z)
    
    s = 1 

    while f(a_p + s*v , ai,di) >= f(a_p,ai,di):
        s = s/2
    
    x0 = a_p + s*v
    return x0