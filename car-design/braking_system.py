import numpy as np
import sys

class BrakingSystem:
    def __init__(self, vehicle_dynamics):
        self.dyn = vehicle_dynamics
        self.specs = vehicle_dynamics.specs

    def mastercylinder_n_pedal(self):
        # based on Race Car Design - Seward
        b = self.specs['brakes']
        t = self.specs['tyres']
        
        W = self.dyn.W
        L = self.dyn.L
        cg_z = self.dyn.cg_z
        mi = self.dyn.mi
        
        mi_b = b.get('mi_b')
        r_r = t['r_r']
        r_b = b['r_b']
        A_sf = b['A_sf']
        A_sr = b['A_sr']
        B1nB2 = b.get('B1nB2')
        F_driver = b['F_driver']
        
        W_r = self.dyn.W_r
        W_f = self.dyn.W_f

        # breaking force
        F_breaking = W * mi
        
        # longitudinal weight transfer
        DW_x = (F_breaking * cg_z)/L
        
        # wheel loads
        W_fl = (W_f + DW_x)/2
        W_fr = W_fl
        W_rl = (W_r - DW_x)/2
        W_rl = W_rl
        
        # wheel brake forces
        F_fb = mi * W_fl
        F_rb = mi * W_rl
        
        # wheel brake torques
        T_bf = F_fb * r_r
        T_br = F_rb * r_r
        
        # calliper clamping forces
        F_cf = T_bf /(2 * r_b * mi_b) 
        F_cr = T_br /(2 * r_b * mi_b) 
        
        # fluid system pessure
        P_bf = F_cf /A_sf 
        P_br = F_cr /A_sr

        if P_bf >= 7.00 or P_br >= 7.00:
            print("\n[ERROR] Fluid system pressure > 7.00 N/mm^2")
            print("To fix:")
            print("  1. Increase the caliper piston area (A_s).")
            print("  2. Increase the brake disc effective radius (r_b).")
            print("  3. Use brake pads with a higher friction coefficient (mi_b).")
#            sys.exit("Execution stopped: Redesign hydraulic system before proceeding.\n")

        # master cylinder standard dimensions (wildwood)
        st_D_m = [1/2, 5/8, 0.7, 3/4, 13/16, 7/8, 15/16, 1, 17/16, 9/8]

        for D_mf in st_D_m:
            for D_mr in st_D_m:
                # Area of master cylinder pistonss
                A_mf = np.pi * ((D_mf/2) * 25.4)**2
                A_mr = np.pi * ((D_mr/2) * 25.4)**2

                # force on master cylinders
                F_f = P_bf * A_mf
                F_r = P_br * A_mr

                # force applied to bias bar
                F_b = F_f + F_r

                # minimum pedal ratio
                P1dP2 = F_b / F_driver

                if P1dP2 >= 4.9 and abs(F_f - F_r) < 100:
                    break
            if P1dP2 >= 4.9 and abs(F_f - F_r) < 100:
                break

        
        # Bias distance 1
        B1 = B1nB2 * (F_f/F_b)
        off = B1 - (B1nB2/2) # offset from central position
        # print
        if off < 0:
            offlr = 'left'
        else:
            offlr = 'right'
            
        print("\n[RESULT] ============================================== ")
        print(f"> Brake Pedal ratio (P1/P2) = {P1dP2:.1f}")
        print(f"> Bore diameter: F = {D_mf}; R = {D_mr}")
        print(f"> B1 = {B1:.4f} mm")
        print(f"> offset from central position: {off:.4f} mm to the {offlr}")
        print("======================================================= ")
