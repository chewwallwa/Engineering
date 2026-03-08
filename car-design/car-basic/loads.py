import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.lines import Line2D

class Dynamics:
    def __init__(self, excel_path='CG.xlsx'):
        # INPUT
        self.power = 120 # [hp]
        self.df = pd.read_excel(excel_path)
        self.df = self.df.dropna(subset=['massa_kg', 'posicao_L_mm', 'posicao_h_mm'])
        self.g = 9.81 # [m/s^2] gravity accel
        self.L = 3215 # [mm] distance between axles
        self.T = 1500 # [mm] distance between tyres
        self.mi = 1.5 # [~] fricion coefficient tyre/road
        self.r_r = 275 # [mm] rear tyre rolling radius

        # CG calculation 
        self.m_m = self.df['massa_kg'].sum()
        self.l_m = (self.df['massa_kg'] * self.df['posicao_L_mm']).sum() / self.m_m
        self.h_m = (self.df['massa_kg'] * self.df['posicao_h_mm']).sum() / self.m_m

        self.W = self.m_m * self.g
        self.W_r = self.W * (self.l_m / self.L)
        self.W_f = self.W - self.W_r

    def static_loads(self):
        print(f"\n[CG]\n")
        print(f"> Combined mass (m_m) = {self.m_m:.1f} kg\n")
        print(f"> L position of CG: {self.l_m:.2f} mm")
        print(f"> h position of CG: {self.h_m:.2f} mm")

        W_r_ratio = (self.W_r / self.W) * 100
        W_f_ratio = (self.W_f / self.W) * 100
        
        print(f"\n[Static Wheel loads + F/R balance]\n")
        print(f"> Static axle load: F: {self.W_f:.2f} N; R: {self.W_r:.2f} N")
        print(f"> F/R ratio: {W_f_ratio:.1f}/{W_r_ratio:.1f} [%]")
        print(f"\n> W_rl = {self.W_r/2:.2f}; W_rr = {self.W_r/2:.2f}; [N]")
        print(f"> W_fl = {self.W_f/2:.2f}; W_fr = {self.W_f/2:.2f}; [N]")

    def _calculate_dynamics(self, longitudinal_force):
        # longitudinal load transfer
        DWx = longitudinal_force * self.h_m / self.L

        # per wheel loads, considering DWx
        W_rl = (self.W_r + DWx) / 2
        W_rr = W_rl
        W_fl = (self.W_f - DWx) / 2
        W_fr = W_fl

        # acceleration considering Dwx
        a = longitudinal_force / self.m_m
        a_g = a / self.g

        print(f"> Longitudinal load transfer (DWx) = {abs(DWx):.2f} N")
        print("per wheel loads:")
        print(f"> W_rl = {W_rl:.2f}; W_rr = {W_rr:.2f}; [N]")
        print(f"> W_fl = {W_fl:.2f}; W_fr = {W_fr:.2f}; [N]")
        print(f"> Acceleration = {a:.2f} m/s^2 = {a_g:.3f}g")
        
        return W_rl, W_rr, W_fl, W_fr, a, a_g, DWx

    def traction_limited_accel(self):
        # traction force
        T_f = (self.W_r * self.mi) / (1 - (self.h_m * self.mi / self.L))
        print("\n[Considering longitudinal load transfer on Traction-limited accel]")

#        W_rl, W_rr = self._calculate_dynamics(T_f)
        W_rl, W_rr, W_fl, W_fr, a, a_g, DWx = self._calculate_dynamics(T_f)

        # peak torque at rear wheels [Nm]
        T_wheels = ((W_rl + W_rr) * self.r_r * self.mi) / 1000

        print(f"> Torque through transmission = {T_wheels:.2f} Nm")

    def power_limited_accel(self):
        # Breaking Force
        F_breaking = self.W * self.mi
        print("\n[Considering longitudinal load transfer on Power-limited accel (Braking)]")
        
        self._calculate_dynamics(-F_breaking)
        
        print(f"> Breaking force = {F_breaking:.2f} N")

    def cornering(self, R_c):
        # max cornering force
        F_cornering = self.W * self.mi

        # LATERAL load transfer (DWy)
        DWy = F_cornering * self.h_m / self.T

        # velocity
        v_mps = np.sqrt(F_cornering * R_c / self.m_m)
        v_kph = v_mps * 3.6 

        print('\n[Cornering and total lateral load transfer]')
        print(f'> Cornering Force = {F_cornering:.2f} N')
        print(f'> Total lateral load transfer (DWy) = {DWy:.2f} N')
        print(f'> Corner Speed = {v_mps:.2f} m/s = {v_kph:.2f} km/h')

    def plot_gg_with_tires(self, v_kph):
        # Limits in g's
        accel_tractive = (self.W_r * self.mi) / (1 - (self.h_m * self.mi / self.L))
        accel_engine = (self.power * 745.7) / max(v_kph / 3.6, 0.1)
        accel_g = min(accel_tractive, accel_engine) / self.W

        # Visual scale for tires
        r_f = self.mi * (self.W_f / self.W)
        r_r = self.mi * (self.W_r / self.W)
        cut_ratio = accel_g / self.mi

        # Parametric vectors
        t = np.linspace(0, 2 * np.pi, 200)
        cos_t = np.cos(t)
        sin_t = np.sin(t)

        # 3x3 Layout Matrix (Central axis is native Polar/Radar)
        fig = plot.figure(figsize=(7, 7))
        ax_fl = plot.subplot2grid((3, 3), (0, 0))
        ax_fr = plot.subplot2grid((3, 3), (0, 2))
        ax_c  = plot.subplot2grid((3, 3), (1, 1), projection='polar')
        ax_rl = plot.subplot2grid((3, 3), (2, 0))
        ax_rr = plot.subplot2grid((3, 3), (2, 2))

        # 1. Central Car Diagram (Converting Cartesian to Polar)
        x_center = self.mi * cos_t
        y_center = np.where(sin_t > 0, accel_g * sin_t, self.mi * sin_t)
        
        theta_center = np.arctan2(y_center, x_center)
        r_center = np.sqrt(x_center**2 + y_center**2)
        
        ax_c.plot(theta_center, r_center, 'k', lw=2)

        # 2. Front Tires
        ax_fl.plot(r_f * cos_t, r_f * sin_t, 'k', lw=1.5)
        ax_fr.plot(r_f * cos_t, r_f * sin_t, 'k', lw=1.5)

        # 3. Rear Tires with power limit cut
        y_rear = np.minimum(r_r * sin_t, r_r * cut_ratio)
        ax_rl.plot(r_r * cos_t, y_rear, 'k', lw=1.5)
        ax_rr.plot(r_r * cos_t, y_rear, 'k', lw=1.5)

        limite_folgado = self.mi * 1.2
        
        # Format Tire Subplots (Completely isolated, no grid/axes)
        for ax in [ax_fl, ax_fr, ax_rl, ax_rr]:
            ax.set_xlim(-limite_folgado, limite_folgado)
            ax.set_ylim(-limite_folgado, limite_folgado)
            ax.set_aspect('equal')
            ax.axis('off')

        # Format Central Radar Diagram
        ax_c.set_rmax(limite_folgado)
        
        # Setup circular grid steps
        ax_c.set_rticks(np.arange(0.5, limite_folgado, 0.5))
        
        # Position the '0.5', '1.0' labels cleanly on the vertical axis
        ax_c.set_rlabel_position(90)
        
        # Generate the internal cartesian crosshair
        ax_c.set_thetagrids([0, 90, 180, 270], labels=['', '', '', ''])

        plot.tight_layout()
        plot.show()


# Executando
car = Dynamics('CG.xlsx')
car.static_loads()
car.traction_limited_accel()
car.power_limited_accel()
car.cornering(100)
car.plot_gg_with_tires(40)
