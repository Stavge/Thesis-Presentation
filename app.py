from flask import Flask, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

EXCEL_FILE = os.path.join(os.path.dirname(__file__), "KATANOMH_KATANAL.xlsx")

# Δυαδικοί κωδικοί για κάθε σενάριο (1-32)
BINARY_CODES = {
    "1": "00000",
    "2": "00001",
    "3": "00010",
    "4": "00011",
    "5": "00100",
    "6": "00101",
    "7": "00110",
    "8": "00111",
    "9": "01000",
    "10": "01001",
    "11": "01010",
    "12": "01011",
    "13": "01100",
    "14": "01101",
    "15": "01110",
    "16": "01111",
    "17": "10000",
    "18": "10001",
    "19": "10010",
    "20": "10011",
    "21": "10100",
    "22": "10101",
    "23": "10110",
    "24": "10111",
    "25": "11000",
    "26": "11001",
    "27": "11010",
    "28": "11011",
    "29": "11100",
    "30": "11101",
    "31": "11110",
    "32": "11111"
}

def get_parameters_from_binary(binary_code):
    parameters = {
        "Θερμομόνωση Οροφής": "Όχι" if binary_code[0] == '0' else "Ναι",
        "Θερμομόνωση Τοίχων": "Όχι" if binary_code[1] == '0' else "Ναι",
        "Αντικατάσταση Κουφωμάτων": "Όχι" if binary_code[2] == '0' else "Ναι",
        "Ανανέωση Θέρμανσης": "Όχι" if binary_code[3] == '0' else "Ναι",
        "Ανανέωση Ψύξης": "Όχι" if binary_code[4] == '0' else "Ναι",
        "Δυαδικός Κώδικας": binary_code
    }
    return parameters

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