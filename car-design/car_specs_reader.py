import pandas as pd
import os

class CarSpecsReader:
    def __init__(self, excel_filename='1_variables.xlsx'):
        self.excel_path = excel_filename
        self.data = {}
        
        if not os.path.exists(self.excel_path):
            print(f"[CRITICAL ERROR] File not found: {os.path.abspath(self.excel_path)}")
            return

        print(f"[SYSTEM] Starting read process: {self.excel_path}")
        self._load_all_data()

    def _load_sheet_to_dict(self, sheet_name):
        """Reads Key-Value sheets and converts them to a Python dictionary."""
        try:
            # engine='openpyxl' prevents conflicts depending on the OS environment
            df = pd.read_excel(self.excel_path, sheet_name=sheet_name, engine='openpyxl')
            
            # Drops rows where the first column (Key) is empty
            df = df.dropna(subset=[df.columns[0]])
            
            # Converts the first two columns into a {Key: Value} dictionary
            # .astype(str).str.strip() ensures no trailing spaces cause KeyErrors
            keys = df.iloc[:, 0].astype(str).str.strip()
            values = df.iloc[:, 1]
            result_dict = dict(zip(keys, values))
            
            print(f"  [OK] Sheet '{sheet_name}' loaded ({len(result_dict)} parameters).")
            return result_dict
            
        except ValueError:
            print(f"  [FAIL] Sheet not found: '{sheet_name}'")
            return {}
        except Exception as e:
            print(f"  [ERROR] Unexpected failure in sheet '{sheet_name}': {e}")
            return {}

    def _load_inventory_sheet(self, sheet_name):
        """Reads Table sheets (e.g., CG Coordinates) and returns a DataFrame."""
        try:
            df = pd.read_excel(self.excel_path, sheet_name=sheet_name, engine='openpyxl')
            df = df.dropna(how='all')
            print(f"  [OK] Table '{sheet_name}' loaded ({df.shape[0]} rows).")
            return df
        except ValueError:
            print(f"  [FAIL] Table sheet not found: '{sheet_name}'")
            return pd.DataFrame()

    def _load_all_data(self):
        """Orchestrates the loading of all vehicle information."""
        
        # 1. Simple Parameters (Key-Value)
        # FIX: Added 'suspension' here since it is now a parameter list, not a table.
        sheets_to_load = {
            'global': 'GLOBAL_PARAMS',
            'brakes': 'BRAKES',
            'tyres': 'TYRES',
            'chassis': 'CHASSIS',
            'engine': 'ENGINE',
            'aero': 'AERO',
            'eletrics': 'ELETRICS',
            'suspension': 'SUSPENSION'
        }

        for key, sheet in sheets_to_load.items():
            self.data[key] = self._load_sheet_to_dict(sheet)

        # 2. Tables (DataFrames)
        self.data['cg_inventory'] = self._load_inventory_sheet('CG')
        
        print("[SYSTEM] Reading process finished.")

    def get_version(self):
        # Fallback protection if GLOBAL_PARAMS lacks the 'version' key
        global_data = self.data.get('global', {})
        return global_data.get('version', 'Undefined version')

# Execution test
if __name__ == "__main__":
    reader = CarSpecsReader()
