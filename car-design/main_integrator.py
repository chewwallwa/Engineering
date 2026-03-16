import sys
import os
from car_specs_reader import CarSpecsReader
from vehicle_dynamics import VehicleDynamics
from braking_system import BrakingSystem
from suspension_kinematics import SuspensionKinematics2D
from structural_analysis import StructuralTrussAnalysis

def run_complete_project():
    print("="*60)
    print("Race Car Design")
    print("="*60)

    results = {}

    specs = CarSpecsReader()
    print(f"[STATUS] Rodando versão do projeto: {specs.get_version()}")
    results['specs'] = specs

    try:
        dynamics = VehicleDynamics(specs)
        dynamics.calculate_cg()
        dynamics.static_loads()
        dynamics.traction_limited_accel()
        dynamics.power_limited_accel()
        dynamics.cornering(100)
        #dynamics.plot_gg_diagram(40)
        results['dynamics'] = dynamics
    except Exception as e:
        print(f"[CRITICAL ERROR] Dynamics module failed: {e}")
        return results

    try:
        brakes = BrakingSystem(dynamics)
        brakes.mastercylinder_n_pedal()
        results['brakes'] = brakes
    except Exception as e:
        print(f"[WARNING] Braking module bypassed due to error: {e}")

    try:
        suspension = SuspensionKinematics2D(specs)
        suspension.front_plane()
        results['suspension'] = suspension
    except Exception as e:
        print(f"[WARNING] Suspension module bypassed due to error: {e}")

    try:
        structure = StructuralTrussAnalysis(specs)
        structure.assemble_and_solve()
        #structure.plot_3d()
        results['structure'] = structure
    except Exception as e:
        print(f"[WARNING] Structural module bypassed due to error: {e}")

    print("\n"+"="*60)
    print("End")
    print("="*60)

    return results

if __name__ == "__main__":
    if not os.path.exists('1_variables.xlsx'):
            print("[ERROR] '1_variables.xlsx' not found in the root folder.")
    else:
        run_complete_project()
