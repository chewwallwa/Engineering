import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class StructuralTrussAnalysis:
    def __init__(self, specs_reader):
        print("\n[MÓDULE] 3D Truss FEA (imcomplete)...")
        
        self.specs = specs_reader.data.get('chassis', {})
        
        self.nodes = None
        self.conn = None
        self.U = None
        self.axial_forces = None

    def assemble_and_solve(self):
        A = float(self.specs.get('A_1'))
        E = float(self.specs.get('E_1'))
        rho = float(self.specs.get('rho_1')) 

        # --- 2. GEOMETRY (NODES) ---
        nodes = np.array([
            [0.0, 0.0, 0.0],         
            [0, 1000.0, 0.0],      
            [1000.0, 0.0, 0.0],     
            [0.0, 0.0, 1000.0]   
        ])

        # --- 3. CONNECTIVITY (ELEMENTS) ---
        conn = np.array([
            [0, 1],  
            [1, 2],  
            [2, 0],  
            [1, 3],  
            [2, 3],  
            [0, 3]   
        ])

        num_nodes = nodes.shape[0]
        num_elements = conn.shape[0]
        num_dof = 3 * num_nodes

        input_forces = np.array([
            [3, 1e3, 2e3, 0]
        ])
    
        # BC Format: [Node, Free_X, Free_Y, Free_Z] (0 = Fixed, 1 = Free)
        input_bcs = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 0],
            [2, 1, 0, 0]
        ])

        K = np.zeros((num_dof, num_dof))
        M = np.zeros((num_dof, num_dof))
        F = np.zeros(num_dof)

        for row in input_forces:
            node = int(row[0])
            F[3 * node + 0] += row[1]  # Force in X
            F[3 * node + 1] += row[2]  # Force in Y
            F[3 * node + 2] += row[3]  # Force in Z

        fixed_dofs_list = []
        for row in input_bcs:
            node = int(row[0])
            if row[1] == 0: fixed_dofs_list.append(3 * node + 0) # Fixed X
            if row[2] == 0: fixed_dofs_list.append(3 * node + 1) # Fixed Y
            if row[3] == 0: fixed_dofs_list.append(3 * node + 2) # Fixed Z
            
        fixed_dofs = np.array(fixed_dofs_list, dtype=int)
        free_dofs = np.setdiff1d(np.arange(num_dof), fixed_dofs)

        # --- 4. CALCULATION ENGINE ---


        # Global Assembly
        for i in range(num_elements):
            n = conn[i, :]
            d_vec = nodes[n[1], :] - nodes[n[0], :]
            L = np.linalg.norm(d_vec)
            d = d_vec / L
            
            tau = np.zeros((2, 6))
            tau[0, 0:3] = d
            tau[1, 3:6] = d
            
            k_el = (E * A / L) * np.array([[1, -1], [-1, 1]])
            idx = np.concatenate((np.arange(3*n[0], 3*n[0]+3), np.arange(3*n[1], 3*n[1]+3)))
            
            K[np.ix_(idx, idx)] += tau.T @ k_el @ tau
            
            # Stable Lumped Mass Matrix for EIG
            m_half = (rho * A * L) / 2.0
            M[3*n[0]:3*n[0]+3, 3*n[0]:3*n[0]+3] += np.eye(3) * m_half
            M[3*n[1]:3*n[1]+3, 3*n[1]:3*n[1]+3] += np.eye(3) * m_half

        # Boundary Conditions 
        fixed_dofs = np.arange(0, 9)
        free_dofs = np.setdiff1d(np.arange(num_dof), fixed_dofs)

        # Displacement Solution
        U = np.zeros(num_dof)
        U[free_dofs] = np.linalg.solve(K[np.ix_(free_dofs, free_dofs)], F[free_dofs])

        # Frequency Analysis
        D, V = la.eigh(K[np.ix_(free_dofs, free_dofs)], M[np.ix_(free_dofs, free_dofs)])
        nat_freqs = np.sort(np.sqrt(np.abs(D))) / (2 * np.pi)

        # --- 5. VECTORIZED POST-PROCESSING ---
        n1 = conn[:, 0]
        n2 = conn[:, 1]
        d_vec = nodes[n2, :] - nodes[n1, :]
        L_vec = np.linalg.norm(d_vec, axis=1)
        dir_cosines = d_vec / L_vec[:, np.newaxis]

        U1 = np.vstack([U[3*n1], U[3*n1+1], U[3*n1+2]]).T
        U2 = np.vstack([U[3*n2], U[3*n2+1], U[3*n2+2]]).T

        # Internal Forces
        axial_stresses = (E / L_vec) * np.sum(dir_cosines * (U2 - U1), axis=1)
        axial_forces = axial_stresses * A

        # --- 6. TABLES ---
        print('\nTABLE 1: NODAL DISPLACEMENTS [mm]')
        for i in range(num_nodes):
            print(f"Nó {i:2d}   {U[3*i]:12.8f} {U[3*i+1]:12.8f} {U[3*i+2]:12.8f}")

        print('\nTABLE 2: INTERNAL AXIAL FORCES [N]')
        status = np.where(axial_forces < 0, 'C', 'T')
        for i in range(num_elements):
            print(f"El {i:2d}: {abs(axial_forces[i]):12.2f} [{status[i]}]")

        print('\nTABLE 3: NATURAL FREQUENCIES [Hz]')
        print(nat_freqs[:min(10, len(nat_freqs))])

        self.nodes = nodes 
        self.conn = conn   
        self.U = U         
        self.axial_forces = axial_forces 

    def plot_3d(self):
        """ Integrated plotting using data stored in self with proportional scale """
        if self.nodes is None or self.axial_forces is None:
            print("[ERROR] No data calculated to plot.")
            return

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('white')
        
        ax.set_box_aspect([1,1,1]) 
        ax.view_init(elev=25, azim=-37)
        
        force_limit = max(np.max(np.abs(self.axial_forces)), 1)
        norm = plt.Normalize(-force_limit, force_limit)
        cmap = plt.get_cmap('bwr')

        scale = 0.1 * np.max(np.ptp(self.nodes, axis=0)) / np.max(np.abs(self.U)) if np.max(np.abs(self.U)) > 0 else 1

        for i in range(self.conn.shape[0]):
            n = self.conn[i, :] 
            p = self.nodes[n, :] 
            
            u = np.array([[self.U[3*n[0]], self.U[3*n[0]+1], self.U[3*n[0]+2]],
                          [self.U[3*n[1]], self.U[3*n[1]+1], self.U[3*n[1]+2]]]) * scale
            
            c_val = cmap(norm(self.axial_forces[i]))
            
            ax.plot(p[:, 0], p[:, 1], p[:, 2], '-.', color=[0.8, 0.8, 0.8], alpha=0.4)
            ax.plot(p[:, 0] + u[:, 0], p[:, 1] + u[:, 1], p[:, 2] + u[:, 2], color=c_val, linewidth=2.5)

        X, Y, Z = self.nodes[:, 0], self.nodes[:, 1], self.nodes[:, 2]
        max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
        mid_x, mid_y, mid_z = (X.max()+X.min())/2, (Y.max()+Y.min())/2, (Z.max()+Z.min())/2
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([]) 
        cb = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.04)
        cb.set_label('Axial Force (N) [Blue: Comp | Red: Tens]')
        
        ax.set_title('3D Structural Analysis - 3d View')
        plt.show()
