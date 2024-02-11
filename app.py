from flask import Flask, render_template, jsonify
from flask_cors import CORS

# Beispiel für die Definition von Datenschemata in app.py

data_schemas = {
    'Namen': {
        'format': 'string',
        'beispiel': 'Max Mustermann'
    },
    'E-Mails': {
        'format': 'email',
        'beispiel': 'max.mustermann@example.com'
    },
    'Telefonnummern': {
        'format': 'telefon',
        'beispiel': '+49123456789'
    }
}

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schemas')
def get_schemas():
    return jsonify(data_schemas)

if __name__ == '__main__':
    app.run(debug=True)
