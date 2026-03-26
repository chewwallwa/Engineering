import numpy as np
import numpy.linalg as alg

class treepoint:
    def tree_point(self, Ra, Rb, Rc, Rd_mod, chute_inicial):
        D = np.copy(chute_inicial) 

        error = 1e-9
        max_ite = 60

        for ite in range(max_ite):
            Phi = np.array([
                np.sum((D - Ra)**2) - (Rd_mod[0]**2),
                np.sum((D - Rb)**2) - (Rd_mod[1]**2),
                np.sum((D - Rc)**2) - (Rd_mod[2]**2)
            ])

            if alg.norm(Phi) < error:
                break

            J = 2 * np.array([
                D - Ra,
                D - Rb,
                D - Rc
            ])

            try:
                Delta_D = alg.solve(J, -Phi)
            except alg.LinAlgError:
                return D

            D = D + Delta_D
            
        return D
        
    def solve_select(self, a, b, c, Rd_mod, n, pos_before):
        vetor_ab = b - a
        vetor_ac = c - a
        normal = np.cross(vetor_ab, vetor_ac)
        
        norma = alg.norm(normal)
        if norma > 1e-6:
            normal = normal / norma
        else:
            normal = np.array([0.0, 0.0, 1.0])

        centroid = (a + b + c) / 3.0

        escala = np.mean(Rd_mod)
        chute_1 = centroid + normal * escala
        chute_2 = centroid - normal * escala

        sol_1 = self.tree_point(a, b, c, Rd_mod, chute_1)
        sol_2 = self.tree_point(a, b, c, Rd_mod, chute_2)

        dist_1 = alg.norm(sol_1 - pos_before)
        dist_2 = alg.norm(sol_2 - pos_before)

        # print(f"   Point {n}: Sol 1 {np.round(solucao_1, 2)} \n            Sol 2 {np.round(solucao_2, 2)}")

        if dist_1 < dist_2:
            return sol_1
        else:
            return sol_2

    def treepointswmod(self, a, b, c, d, n):
        Rc_mod = np.array([alg.norm(d-a), alg.norm(d-b), alg.norm(d-c)])
        
        D_correto = self.solve_select(a, b, c, Rc_mod,n, pos_before=d)
        print(f'point {n} {np.round(D_correto,2)}')
        return D_correto


if __name__ == '__main__':
    sus = treepoint()

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

    c = sus.treepointswmod(a,b,d,c,'c')
    e = sus.treepointswmod(c,d,f,e,'e')
    g = sus.treepointswmod(c,d,e,g,'g')
    e = sus.treepointswmod(c,d,f,e,'e')
    i = sus.treepointswmod(c,e,g,i,'i')
    j = sus.treepointswmod(c,e,g,j,'j')
    h = sus.treepointswmod(c,g,j,h,'h')
   
    
