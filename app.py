from flask import Flask, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = os.path.join(os.path.dirname(__file__), "KATANOMH_KATANAL.xlsx")

# Δυαδικοί κωδικοί για κάθε σενάριο (1-32)
BINARY_CODES = { ... }  # (όπως το έχεις)

def get_parameters_from_binary(binary_code):
    return { ... }  # (όπως το έχεις)

def load_scenarios():
    try:
        print("Excel file exists:", os.path.exists(EXCEL_FILE))
        df = pd.read_excel(EXCEL_FILE, header=None)
        scenarios = {}
        for col in range(1, 33):
            scenario_num = str(col)
            binary_code = BINARY_CODES[scenario_num]
            scenarios[scenario_num] = {
                "energy": float(df.iloc[1, col]),
                "cost": float(df.iloc[2, col]),
                "binary": binary_code,
                "params": get_parameters_from_binary(binary_code)
            }
        return scenarios
    except Exception as e:
        print(f"Σφάλμα Excel: {e}")
        return {}

SCENARIOS = load_scenarios()

ENERGY_MIN = min(s["energy"] for s in SCENARIOS.values())
ENERGY_MAX = max(s["energy"] for s in SCENARIOS.values())
COST_MIN = min(s["cost"] for s in SCENARIOS.values())
COST_MAX = max(s["cost"] for s in SCENARIOS.values())

@app.route('/')
def home():
    return render_template('index.html', 
                         total_scenarios=len(SCENARIOS),
                         energy_min=ENERGY_MIN,
                         energy_max=ENERGY_MAX,
                         cost_min=COST_MIN,
                         cost_max=COST_MAX)

@app.route('/api/scenario/<num>')
def get_scenario(num):
    return jsonify(SCENARIOS.get(num, {}))

if __name__ == '__main__':
    app.run(debug=True)
else:
    api = app
