import numpy as np
import numpy.linalg as alg

def treepoint(Ra, Rb, Rc, Rd_mod):
    Ka = Rd_mod[0]**2 - np.sum(Ra**2)
    Kb = Rd_mod[1]**2 - np.sum(Rb**2)
    Kc = Rd_mod[2]**2 - np.sum(Rc**2)

    Matriz_A = 2 * np.array([
        [Ra[1] - Rb[1], Ra[2] - Rb[2]],
        [Ra[1] - Rc[1], Ra[2] - Rc[2]]
    ])
    
    Vetor_B = np.array([Kb - Ka, Kc - Ka])
    Coefs_X = 2 * np.array([Ra[0] - Rb[0], Ra[0] - Rc[0]])

    inv_A = np.linalg.inv(Matriz_A)
    Constantes_yz = inv_A.dot(Vetor_B)
    Multiplicadores_yz = inv_A.dot(-Coefs_X)
    
    Cy, Cz = Constantes_yz[0], Constantes_yz[1]
    My, Mz = Multiplicadores_yz[0], Multiplicadores_yz[1]

    Yc = Cy - Ra[1]
    Zc = Cz - Ra[2]

    a = 1 + My**2 + Mz**2
    b = -2*Ra[0] + 2*My*Yc + 2*Mz*Zc
    c = Ra[0]**2 + Yc**2 + Zc**2 - Rd_mod[0]**2

    delta = b**2 - 4*a*c
    if delta < 0:
        print("impossible, bro")
        return None, None

    x1 = (-b + np.sqrt(delta)) / (2*a)
    x2 = (-b - np.sqrt(delta)) / (2*a)

    y1 = My * x1 + Cy
    z1 = Mz * x1 + Cz

    y2 = My * x2 + Cy
    z2 = Mz * x2 + Cz

    solucao1 = np.array([x1, y1, z1])
    solucao2 = np.array([x2, y2, z2])

    return solucao1, solucao2
    
def treepointswmod(a,b,c,d):
    Rc_mod = np.array([alg.norm(d-a), alg.norm(d-b), alg.norm(d-c)])
    D1,D2 = treepoint(a,b,c, Rc_mod)
    print(f'sol 1: {np.round(D1, 4)}')
    print(f'sol 2: {np.round(D2, 4)}')


if __name__ == '__main__':
    a = np.array([125, 350, -80])
    b = np.array([-115,350, -80])
    c = np.array([5,   625, -90])
    d = np.array([-15, 530, 545])
    e = np.array([155, 537, 250])
    f = np.array([25,  45, 270])
    g = np.array([-3,  545, 125])
    h = np.array([0,   670, -270])
    i = np.array([0,   65, 0])
    j = np.array([0,   730, 0])

    c = treepointswmod(a,b,d,c)
    e = treepointswmod(c,d,f,e)
    g = treepointswmod(c,d,e,g)
    e = treepointswmod(c,d,f,e)
    i = treepointswmod(c,e,g,i)
    j = treepointswmod(c,e,g,j)
    h = treepointswmod(c,g,j,h)

