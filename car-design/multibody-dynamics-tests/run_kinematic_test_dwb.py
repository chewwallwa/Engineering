"""
This script defines a double-wishbone suspension geometry and calculates 
some things
by jeremybk21: https://github.com/jeremybk21/suspension-kinematics

# Modified by chewwallwa 2026
- Refactored to OOP
- added kpi calculation

# ROADMAP
- tie/track rod (steer angle, toe change, bump steer)
- add chassis (Euler angles to chassis; roll, pitch, yaw, heave;)
- 2nd front wheel 
- Instant centers, Roll center and anti-geometries
- 4 wheels
- Pushrod, Rocker, Spring, Dampers (Motion ratio)

Guide to validate with lotus shark: 
roll angle = weight/sprung mass = Braking/Drive % = 0
Wheel vertical stiffness = 10^9
"""

import numpy as np
import matplotlib.pyplot as plt

class DoubleWishboneSuspension:
    """
    Class to define, solve, and plot a double-wishbone suspension mechanism.
    All length units are in millimeters (mm) and angles in degrees.
    """
    
    def __init__(self, bump_mm=0):
        # =========================================================
        # 1. SETUP & CONSTANTS (All inputs in mm)
        # =========================================================
        self.bump_mm = bump_mm                # Input: Vertical travel in mm (Positive = Bump)
        self.roll_rad = 225                   # Rolling radius (ground to wheel center)
        # self.roll_angle = 0
        # self.clr = np.array([0, 0, 0])       # Ground clearance vector
        # self.scbh = 240                        # Chassis body height
        # self.cbwl = 170 * 2                   # Chassis body width lower
        # self.cbwu = 285 * 2                   # Chassis body width upper
        # self.cbh = 240
        # self.track = 1400                     # Track width
        # self.tyw = 150                        # Tyre width
        # self.offset = 40                      # Wheel offset
        
        # # --- Relative points ---
        # # Hub absolute location (X=0 reference, Y=track setup, Z=hub height)
        # self.HUB = np.array([0, (self.track/2) + self.tyw - self.offset, self.roll_rad]) 
        # # Ball joints relative to HUB center
        # self.HUBlb = np.array([-130, 0, -130]) # Lower ball joint relative to hub
        # self.HUBub = np.array([-150, 0, 130])  # Upper ball joint relative to hub
        # self.ROD_hub = np.array([0, -76.2, -76.2]) # Push/Pull rod joint on LCA relative to hub
        # # Strut chassis mount absolute position (X, Y, Z)
        # self.ROD_cb = np.array([-53, 170, 350]) 
        
        # =========================================================
        # 2. HARDPOINTS GENERATION
        # =========================================================
        self.suspension = {}

        # # Chassis Mounts (Fixed)
        # self.suspension['p_LCA_chassis_fwd'] = np.array([47, self.cbwl/2, 0]) + self.clr
        # self.suspension['p_LCA_chassis_aft'] = np.array([-246, self.cbwl/2, 0]) + self.clr
        # self.suspension['p_UCA_chassis_fwd'] = np.array([161, self.cbwu/2, self.cbh]) + self.clr
        # self.suspension['p_UCA_chassis_aft'] = np.array([-87, self.cbwu/2, self.cbh]) + self.clr
        # # Moving points (Design/Static position)
        # self.suspension['p_LCA_upright_design'] = self.HUB + self.HUBlb
        # self.suspension['p_UCA_upright_design'] = self.HUB + self.HUBub
        # self.suspension['p_strut_mount_lca_design'] = self.HUB + self.ROD_hub
        # self.suspension['p_strut_mount_chassis'] = self.ROD_cb + self.clr
        
        # Chassis Mounts (Fixed)
        self.suspension['p_LCA_chassis_fwd'] = np.array([-21.5, 75, 163]) 
        self.suspension['p_LCA_chassis_aft'] = np.array([588, 75, 165]) 
        self.suspension['p_UCA_chassis_fwd'] = np.array([19.7, 148.39, 377]) 
        self.suspension['p_UCA_chassis_aft'] = np.array([588, 148.39, 377 ]) 
        # Moving points (Design/Static position)
        self.suspension['p_LCA_upright_design'] = np.array([156.6, 805.5, 189]) 
        self.suspension['p_UCA_upright_design'] = np.array([162,772.5,408.5]) 
        self.suspension['p_strut_mount_lca_design'] = np.array([150, 700, 225]) 
        self.suspension['p_strut_mount_chassis'] = np.array([175, 200, 475])         
        
        # =========================================================
        # 3. CONSTRAINTS (Link Lengths)
        # =========================================================
        s = self.suspension
        s['L_LCA'] = np.linalg.norm(s['p_LCA_upright_design'] - s['p_LCA_chassis_fwd'])
        s['L_UCA_fwd'] = np.linalg.norm(s['p_UCA_upright_design'] - s['p_UCA_chassis_fwd'])
        s['L_UCA_aft'] = np.linalg.norm(s['p_UCA_upright_design'] - s['p_UCA_chassis_aft'])
        s['L_upright'] = np.linalg.norm(s['p_UCA_upright_design'] - s['p_LCA_upright_design'])
        
        # Pre-calculating LCA swing radius for linear-to-angular conversion
        p1 = s['p_LCA_chassis_fwd']
        p2 = s['p_LCA_chassis_aft']
        v_lca = s['p_LCA_upright_design'] - p1
        axis_lca = (p2 - p1) / np.linalg.norm(p2 - p1)
        self.LCA_radius = np.linalg.norm(np.cross(v_lca, axis_lca))

        self.results = {}
        self.solved_angle_deg = 0

    def solve_kinematics(self):
        """ Calculates 3D positions based on self.bump_mm """
        s = self.suspension
        
        # Linear bump to angular rotation conversion
        theta_LCA = np.arcsin(self.bump_mm / self.LCA_radius)
        self.solved_angle_deg = np.degrees(theta_LCA)
        
        # Define rotation axis
        p1 = s['p_LCA_chassis_fwd']
        p2 = s['p_LCA_chassis_aft']
        axis_vec = (p2 - p1) / np.linalg.norm(p2 - p1)
        angle = -theta_LCA  
        
        # LCA Ball Joint Rotation
        p_to_rotate_bj = s['p_LCA_upright_design']
        v_bj = p_to_rotate_bj - p1
        v_rot_bj = (v_bj * np.cos(angle) + 
                    np.cross(axis_vec, v_bj) * np.sin(angle) + 
                    axis_vec * np.dot(axis_vec, v_bj) * (1 - np.cos(angle)))
        self.results['p_LCA_upright'] = p1 + v_rot_bj

        # Strut Mount Rotation
        p_to_rotate_strut = s['p_strut_mount_lca_design']
        v_strut = p_to_rotate_strut - p1
        v_rot_strut = (v_strut * np.cos(angle) + 
                       np.cross(axis_vec, v_strut) * np.sin(angle) + 
                       axis_vec * np.dot(axis_vec, v_strut) * (1 - np.cos(angle)))
        self.results['p_strut_mount_lca'] = p1 + v_rot_strut

        # Upper Ball Joint (Three-sphere intersection)
        C1 = s['p_UCA_chassis_fwd']
        R1 = s['L_UCA_fwd']
        C2 = s['p_UCA_chassis_aft']
        R2 = s['L_UCA_aft']
        C3 = self.results['p_LCA_upright']
        R3 = s['L_upright']
        
        e_x = (C2 - C1) / np.linalg.norm(C2 - C1)
        temp2 = C3 - C1
        i = np.dot(e_x, temp2)
        e_y = (temp2 - i * e_x) / np.linalg.norm(temp2 - i * e_x)
        e_z = np.cross(e_x, e_y)
        d = np.linalg.norm(C2 - C1)
        j = np.dot(e_y, temp2)
        
        x = (R1**2 - R2**2 + d**2) / (2 * d)
        y = (R1**2 - R3**2 + i**2 + j**2) / (2 * j) - (i/j) * x
        z_arg = R1**2 - x**2 - y**2
        
        z = np.sqrt(max(0, z_arg))
        sol1 = C1 + x * e_x + y * e_y + z * e_z
        sol2 = C1 + x * e_x + y * e_y - z * e_z
        
        self.results['p_UCA_upright'] = sol1 if sol1[2] > sol2[2] else sol2
        return self.results

    def calculate_kpis(self):
        """ Calculates Kingpin Inclination (KPI) and Arm Inclinations """
        if not self.results:
            raise ValueError("Run solve_kinematics() first.")
            
        lbj = self.results['p_LCA_upright']
        ubj = self.results['p_UCA_upright']
        
        # 1. KINGPIN INCLINATION (KPI)
        # Angle of the upright line relative to vertical Z axis in front view
        v_upright = ubj - lbj
        kpi_deg = np.degrees(np.arctan2(v_upright[1], v_upright[2]))
        
        # 2. ARM INCLINATIONS
        # LCA Front View Angle
        p_lca_ch = self.suspension['p_LCA_chassis_fwd']
        incl_lca = np.degrees(np.arctan2(lbj[2] - p_lca_ch[2], lbj[1] - p_lca_ch[1]))
        
        # UCA Front View Angle
        p_uca_ch = self.suspension['p_UCA_chassis_fwd']
        incl_uca = np.degrees(np.arctan2(ubj[2] - p_uca_ch[2], ubj[1] - p_uca_ch[1]))

        kpis = {
            'kingpin_incl_deg': kpi_deg,
            'lca_incl_deg': incl_lca,
            'uca_incl_deg': incl_uca
        }
        
        print("\n--- Key Performance Indicators ---")
        for key, val in kpis.items():
            print(f"> {key}: {val:.2f}")
        return kpis

    def draw_suspension(self):
        """ 3D Plot focused on Front View (Ortho) """
        if not self.results:
            self.solve_kinematics()
            
        s, r = self.suspension, self.results
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(f'Front View | Bump: {self.bump_mm}mm')

        # Nodes
        ch_pts = np.array([s['p_LCA_chassis_fwd'], s['p_LCA_chassis_aft'], s['p_UCA_chassis_fwd'], s['p_UCA_chassis_aft']])
        ax.scatter(ch_pts[:, 0], ch_pts[:, 1], ch_pts[:, 2], s=80, c='blue')
        up_pts = np.array([r['p_LCA_upright'], r['p_UCA_upright']])
        ax.scatter(up_pts[:, 0], up_pts[:, 1], up_pts[:, 2], s=80, c='red')

        # Arms
        ax.plot([s['p_LCA_chassis_fwd'][0], r['p_LCA_upright'][0]], [s['p_LCA_chassis_fwd'][1], r['p_LCA_upright'][1]], [s['p_LCA_chassis_fwd'][2], r['p_LCA_upright'][2]], 'g-')
        ax.plot([s['p_LCA_chassis_aft'][0], r['p_LCA_upright'][0]], [s['p_LCA_chassis_aft'][1], r['p_LCA_upright'][1]], [s['p_LCA_chassis_aft'][2], r['p_LCA_upright'][2]], 'g-')
        ax.plot([s['p_UCA_chassis_fwd'][0], r['p_UCA_upright'][0]], [s['p_UCA_chassis_fwd'][1], r['p_UCA_upright'][1]], [s['p_UCA_chassis_fwd'][2], r['p_UCA_upright'][2]], 'm-')
        ax.plot([s['p_UCA_chassis_aft'][0], r['p_UCA_upright'][0]], [s['p_UCA_chassis_aft'][1], r['p_UCA_upright'][1]], [s['p_UCA_chassis_aft'][2], r['p_UCA_upright'][2]], 'm-')
        ax.plot([r['p_LCA_upright'][0], r['p_UCA_upright'][0]], [r['p_LCA_upright'][1], r['p_UCA_upright'][1]], [r['p_LCA_upright'][2], r['p_UCA_upright'][2]], 'r-', linewidth=3)
        ax.plot([s['p_strut_mount_chassis'][0], r['p_strut_mount_lca'][0]], [s['p_strut_mount_chassis'][1], r['p_strut_mount_lca'][1]], [s['p_strut_mount_chassis'][2], r['p_strut_mount_lca'][2]], 'c-', linewidth=2)

        # Aspect and View
        limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
        radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
        mean = np.mean(limits, axis=1)
        ax.set_xlim3d([mean[0] - radius, mean[0] + radius]); ax.set_ylim3d([mean[1] - radius, mean[1] + radius]); ax.set_zlim3d([mean[2] - radius, mean[2] + radius])
        ax.view_init(elev=0, azim=0) # Pure Front View
        ax.set_proj_type('ortho')
        plt.show()

if __name__ == "__main__":
    car = DoubleWishboneSuspension(bump_mm=50) # Lotus validation (Static)
    car.solve_kinematics()
    car.calculate_kpis()
    car.draw_suspension()
