from functii_ajutatoare import *


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




def exemplul_5_3():
    x = np.array([3, -7])
    a = np.array([[1, 9], [ 2, 7], [5, 8], [7, 7], [9, 5], [3, 7]])
    x_true = np.array([0, -8])
    pasi_acuratete = 30
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

    draw_circle = plt.Circle((x_gasit_optim[0], x_gasit_optim[1]), np.mean([np.linalg.norm(x_gasit_optim - ai) for ai in a]) ,fill=False, lw = 3)
    axes.add_artist(draw_circle)

    plt.title('Circle fitting LS\n ' + 'distanta fata de punctul de optim :' + str( np.linalg.norm( fixed_point_CF_LS(x, a, d, pasi_acuratete)- x_true)))

    plt.legend()
    plt.show()