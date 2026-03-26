"""Based on and validated with Vsusp.com"""
import math

class SuspensionKinematics2D:
    def __init__(self, specs_reader):
        self.specs = specs_reader.data
        
        # Get the dictionary corresponding to the suspension tab in Excel
        s = self.specs.get('suspension', {})
        t = self.specs.get('tyres', {})

        self.roll = s['roll']
        self.fby = s['fby']
        
        self.fclx = s['fclx']
        self.fbly = s['fbly']
        self.fcux = s['fcux']
        self.fbuy = s['fbuy']
        
        self.caul = s['caul']
        self.call = s['call']
        
        self.khux = s['khux']
        self.khuy = s['khuy']
        self.khlx = s['khlx']
        self.khly = s['khly']
        
        self.sthotr_x = s['sthotr_x']
        self.sthotr_y = s['sthotr_y']
        self.wo = s['wo']
        
        self.tsw = t['tsw']
        self.tar = t['tar']
        self.wd = t['wd']
        self.tscmp = t['tscmp']

        print("\n[MODULE] Starting Suspension Kinematics (VSUSP Direct Mapping)...")

    def _eval_alpha(self, alpha, wms_y, IL_x, IL_y, IU_x, IU_y, sign):
        cos_a = math.cos(alpha)
        sin_a = math.sin(alpha)

        # Applying the short variables to the nodes rotation
        loc_lbj_x = -sign * self.khlx
        loc_lbj_y = -self.khly
        loc_ubj_x = -sign * self.khux
        loc_ubj_y = self.khuy

        rot_lbj_x = loc_lbj_x * cos_a - loc_lbj_y * sin_a
        rot_lbj_y = loc_lbj_x * sin_a + loc_lbj_y * cos_a
        rot_ubj_x = loc_ubj_x * cos_a - loc_ubj_y * sin_a
        rot_ubj_y = loc_ubj_x * sin_a + loc_ubj_y * cos_a

        global_lbj_y = wms_y + rot_lbj_y
        dy_lca = global_lbj_y - IL_y

        if abs(dy_lca) > self.call:
            return None 

        dx_lca = math.sqrt(self.call**2 - dy_lca**2)
        global_lbj_x = IL_x + sign * dx_lca
        wms_x = global_lbj_x - rot_lbj_x

        global_ubj_x = wms_x + rot_ubj_x
        global_ubj_y = wms_y + rot_ubj_y

        calc_uca = math.sqrt((global_ubj_x - IU_x)**2 + (global_ubj_y - IU_y)**2)
        return calc_uca - self.caul, wms_x, global_lbj_x, global_lbj_y, global_ubj_x, global_ubj_y

    def _solve_side(self, sign, wms_y, IL_x, IL_y, IU_x, IU_y):
        a_min = math.radians(-25)
        a_max = math.radians(25)
        
        for _ in range(60):
            a_mid = (a_min + a_max) / 2.0
            res_mid = self._eval_alpha(a_mid, wms_y, IL_x, IL_y, IU_x, IU_y, sign)
            res_min = self._eval_alpha(a_min, wms_y, IL_x, IL_y, IU_x, IU_y, sign)
            
            if res_mid is None: break
            if res_min is None: 
                a_min = a_mid
                continue
                
            if res_mid[0] * res_min[0] < 0:
                a_max = a_mid
            else:
                a_min = a_mid
                
        alpha = (a_min + a_max) / 2.0
        camber = -math.degrees(alpha) if sign == 1 else math.degrees(alpha)
        
        try:
            _, wms_x, lbj_x, lbj_y, ubj_x, ubj_y = self._eval_alpha(alpha, wms_y, IL_x, IL_y, IU_x, IU_y, sign)
        except TypeError:
            return {'camber': 0, 'ic_angle': 0, 'scrub': 0}
            
        dy_lca = lbj_y - IL_y
        dx_lca = lbj_x - IL_x
        lower_inclination = math.degrees(math.atan2(dy_lca, abs(dx_lca)))
        
        dy_uca = ubj_y - IU_y
        dx_uca = ubj_x - IU_x
        upper_inclination = math.degrees(math.atan2(dy_uca, abs(dx_uca)))
        
        dx_kpi = ubj_x - lbj_x
        dy_kpi = ubj_y - lbj_y
        sai_kpi = math.degrees(math.atan2(abs(dx_kpi), abs(dy_kpi)))
        
        m_kpi_inv = dx_kpi / dy_kpi if dy_kpi != 0 else 0
        b_kpi_inv = lbj_x - (m_kpi_inv * lbj_y)
        
        loc_cp_x = -sign * self.wo
        loc_cp_y = -self.rolling_radius
        rot_cp_x = loc_cp_x * math.cos(alpha) - loc_cp_y * math.sin(alpha)
        contact_patch_x = wms_x + rot_cp_x
        
        sa_x_at_ground = m_kpi_inv * 0.0 + b_kpi_inv
        scrub_radius = abs(contact_patch_x - sa_x_at_ground)
        
        m_uca_line = dy_uca / dx_uca if dx_uca != 0 else 0
        b_uca_line = IU_y - (m_uca_line * IU_x)
        m_lca_line = dy_lca / dx_lca if dx_lca != 0 else 0
        b_lca_line = IL_y - (m_lca_line * IL_x)
        
        if abs(m_uca_line - m_lca_line) > 1e-6:
            ic_x = (b_lca_line - b_uca_line) / (m_uca_line - m_lca_line)
            ic_y = m_uca_line * ic_x + b_uca_line
            dy_rc = ic_y - 0.0
            dx_rc = abs(ic_x - contact_patch_x)
            ic_inclination_angle = abs(math.degrees(math.atan2(dy_rc, dx_rc)))
        else:
            ic_x, ic_y = float('inf'), float('inf')
            ic_inclination_angle = 0.0
            
        loc_otr_x = -sign * self.sthotr_x
        loc_otr_y = -self.sthotr_y 
        
        rot_otr_x = loc_otr_x * math.cos(alpha) - loc_otr_y * math.sin(alpha)
        rot_otr_y = loc_otr_x * math.sin(alpha) + loc_otr_y * math.cos(alpha)
        
        otr_x = wms_x + rot_otr_x
        otr_y = wms_y + rot_otr_y
        
        return {
            'camber': camber, 'lower_incl': lower_inclination, 'upper_incl': upper_inclination,
            'sai': sai_kpi, 'scrub': scrub_radius, 'ic_angle': ic_inclination_angle,
            'otr_x': otr_x, 'otr_y': otr_y
        }

    def front_plane(self):
        # Tire calculations updated for short variables
        self.wheel_radius = (self.wd * 25.4) / 2.0
        self.tire_section_height = self.tsw * (self.tar / 100.0)
        self.tire_diameter = (self.wheel_radius + self.tire_section_height) * 2.0
        self.rolling_radius = (self.tire_diameter / 2.0) - self.tscmp
        self.tire_circumference = math.pi * self.tire_diameter
        self.tire_revs_per_km = 1000000.0 / self.tire_circumference if self.tire_circumference > 0 else 0
        
        # Upright Geometry (Kingpin and Spindle)
        x1, y1 = -self.khlx, -self.khly
        x2, y2 = -self.khux, self.khuy
        x0, y0 = -self.wo, 0
        
        num = abs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1)
        den = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        self.spindle_length = num / den if den != 0 else 0
        self.kingpin_length = den

        # Chassis mount geometry evaluation
        dx_m = self.fcux - self.fclx
        dy_m = self.fbuy - self.fbly
        self.dist_mounts = math.sqrt(dx_m**2 + dy_m**2)
        self.incl_mounts = math.degrees(math.atan2(dy_m, dx_m))

        # Application of chassis Roll
        t = -math.radians(self.roll)
        chassis_y = self.fby
        
        def rotate_pt(x, y):
            return x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)

        IL_x_R, IL_y_R = rotate_pt(self.fclx, chassis_y + self.fbly)
        IU_x_R, IU_y_R = rotate_pt(self.fcux, chassis_y + self.fbuy)
        
        IL_x_L, IL_y_L = rotate_pt(-self.fclx, chassis_y + self.fbly)
        IU_x_L, IU_y_L = rotate_pt(-self.fcux, chassis_y + self.fbuy)

        self.right = self._solve_side(1, self.rolling_radius, IL_x_R, IL_y_R, IU_x_R, IU_y_R)
        self.left = self._solve_side(-1, self.rolling_radius, IL_x_L, IL_y_L, IU_x_L, IU_y_L)
        
        # Rack and Tie Rod calculations
        s = self.specs.get('suspension', {})
        self.rack_width = s.get('rack_w', 376.0) # Uses fallback if not provided in Excel
        self.rack_height = s.get('rack_h', 58.0)
        
        itr_x_r, itr_y_r = rotate_pt(self.rack_width / 2.0, chassis_y + self.rack_height)
        itr_x_l, itr_y_l = rotate_pt(-self.rack_width / 2.0, chassis_y + self.rack_height)
        
        self.right['tie_rod'] = math.sqrt((self.right['otr_x'] - itr_x_r)**2 + (self.right['otr_y'] - itr_y_r)**2)
        self.left['tie_rod'] = math.sqrt((self.left['otr_x'] - itr_x_l)**2 + (self.left['otr_y'] - itr_y_l)**2)

        print("> Static geometry calculations completed.")
        return self._print_results()

    def _print_results(self):
        """ Prints the formatted dictionary output to the terminal """
        results = {
            'Distance between upper and lower mounts (mm)': round(self.dist_mounts, 3),
            'Inclination angle from lower to upper mounts (deg)': round(self.incl_mounts, 3),
            'Upper Right inclination (deg)': round(self.right['upper_incl'], 3),
            'Upper Left inclination (deg)': round(self.left['upper_incl'], 3),
            'Lower Right inclination (deg)': round(self.right['lower_incl'], 3),
            'Lower Left inclination (deg)': round(self.left['lower_incl'], 3),
            'Distance between upper and lower ball joints (kingpin length) (mm)': round(self.kingpin_length, 3),
            'Right Steering Axis Inclination (SAI/KPI) (deg)': round(self.right['sai'], 3),
            'Left Steering Axis Inclination (SAI/KPI) (deg)': round(self.left['sai'], 3),
            'Spindle length (mm)': round(self.spindle_length, 3),
            'Right knuckle rotation from perpendicular (deg)': round(-self.right['camber'], 3),
            'Left knuckle rotation from perpendicular (deg)': round(-self.left['camber'], 3),
            'Rack width (mm)': round(self.rack_width, 3),
            'Rack height (mm)': round(self.rack_height, 3),
            'Right tie rod length (mm)': round(self.right['tie_rod'], 3),
            'Left tie rod length (mm)': round(self.left['tie_rod'], 3),
            'Right tire camber (deg)': round(self.right['camber'], 3),
            'Left tire camber (deg)': round(self.left['camber'], 3),
            'Tire diameter (mm)': round(self.tire_diameter, 3),
            'Rolling radius (mm)': round(self.rolling_radius, 3),
            'Wheel radius (mm)': round(self.wheel_radius, 3),
            'Tire circumference (mm)': round(self.tire_circumference, 3),
            'Tire section height (sidewall thickness) (mm)': round(self.tire_section_height, 3),
            'Tire revs per kilometer': round(self.tire_revs_per_km, 3),
            'Left scrub radius (mm)': round(self.left['scrub'], 3),
            'Right scrub radius (mm)': round(self.right['scrub'], 3),
            'Left IC inclination angle (deg)': round(self.left['ic_angle'], 3),
            'Right IC inclination angle (deg)': round(self.right['ic_angle'], 3)
        }

        print("\n[SUSPENSION KINEMATICS RESULTS]")
        print("="*60)
        for key, value in results.items():
            print(f"> {key}: {value}")
        print("="*60)
        
        return results
