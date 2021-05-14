from functii_ajutatoare import *



if __name__ == '__main__':

    x = np.array([-10, 5])
    a = np.array([[-29, -18], [7, -24], [-19, -27], [10, -27], [-9, 3], [-33, -34]])
    x_true = np.array([-8, -2])
    pasi_acuratete = 10**2
    d, r = generare_di_ce_reurneaza_si_r(x_true, a)


    assert verificare_asumption_matrice(a) == True , "a1...an se afla intr-un spatiu dimensional afin mai mic[de exmplu: lucram in plan(2D) si satelitii sunt coliniari]"
    assert len(a) >= len(x) + 1, "Consecinta directa a faptului ca a1...an nu se afla intr-un spatiu dimensional afin mai mic nu este satisfacuta"

    B = generare_B(a, d)
    b =generare_b(a, d)

    D = generare_D(len(x))
    g = generare_g(len(x))


    generare_beta(len(x), a)

    
    #lambda_caciula = cautare_lambda_caciula(B,D)

    #print(lambda_caciula)