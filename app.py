from flask import Flask, jsonify, request, send_from_directory
import json, os, datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_DIR, 'rules.json')
HISTORY_PATH = os.path.join(BASE_DIR, 'history.json')

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'index.html')

@app.route('/rules')
def get_rules():
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    return jsonify(rules)

@app.route('/history', methods=['GET', 'POST'])
def manage_history():
    if request.method == 'GET':
        if not os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f)
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    elif request.method == 'POST':
        data = request.json
        entry = {"timestamp": datetime.datetime.now().isoformat(), "data": data}
        with open(HISTORY_PATH, 'r+', encoding='utf-8') as f:
            history = json.load(f)
            history.append(entry)
            f.seek(0)
            json.dump(history, f, indent=2, ensure_ascii=False)
        return jsonify({"status": "ok", "message": "Histórico atualizado com sucesso"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
