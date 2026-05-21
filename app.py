from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = 'teme.json'

def load_teme():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_teme(teme):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(teme, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    teme = load_teme()
    return render_template('index.html', teme=teme)

@app.route('/adauga', methods=['POST'])
def adauga():
    teme = load_teme()
    tema_noua = {
        'id': len(teme) + 1,
        'materie': request.form['materie'],
        'descriere': request.form['descriere'],
        'termen': request.form['termen'],
        'rezolvata': False
    }
    teme.append(tema_noua)
    save_teme(teme)
    return redirect(url_for('index'))

@app.route('/rezolvata/<int:id>')
def rezolvata(id):
    teme = load_teme()
    for t in teme:
        if t['id'] == id:
            t['rezolvata'] = not t['rezolvata']
    save_teme(teme)
    return redirect(url_for('index'))

@app.route('/sterge/<int:id>')
def sterge(id):
    teme = load_teme()
    teme = [t for t in teme if t['id'] != id]
    save_teme(teme)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)