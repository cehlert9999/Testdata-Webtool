from flask import Flask, render_template, request, Response, jsonify
from flask_restx import Api, Resource, fields
import random
import string
import faker
import json
import csv
import dicttoxml
from io import StringIO

app = Flask(__name__)

fake = faker.Faker()

def generate_sap_business_partner():
    return ''.join(random.choices(string.digits, k=10))

def generate_sap_account():
    return ''.join(random.choices(string.digits, k=12))


def generate_name(locale):
    fake = faker.Faker(locale)
    return fake.name()

def generate_address(locale):
    fake = faker.Faker(locale)
    return fake.address().replace('\n', ', ')

def generate_email():
    fake = faker.Faker('de_DE')
    return fake.email()

def generate_phone_number(locale):
    fake = faker.Faker(locale)
    return fake.phone_number()

def generate_iban():
    fake = faker.Faker('de_DE')
    return fake.iban()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        num_entries = int(request.form.get('num_entries'))
        data_types = request.form.getlist('data_type')
        output_format = request.form.get('output_format')
        locale = request.form.get('locale')
        data = []
        for _ in range(num_entries):
            entry = {}
            if 'name' in data_types:
                entry['name'] = generate_name(locale)
            if 'address' in data_types:
                entry['address'] = generate_address(locale)
            if 'email' in data_types:
                entry['email'] = generate_email()
            if 'phone_number' in data_types:
                entry['phone_number'] = generate_phone_number(locale)
            if 'iban' in data_types:
                entry['iban'] = generate_iban()
            if 'sap_business_partner' in data_types:
                entry['sap_business_partner'] = generate_sap_business_partner()
            if 'sap_account' in data_types:
                entry['sap_account'] = generate_sap_account()
            data.append(entry)
        
        if output_format == 'json':
            return Response(json.dumps(data, indent=4), mimetype='application/json')
        elif output_format == 'csv':
            si = StringIO()
            cw = csv.DictWriter(si, fieldnames=data_types)
            cw.writeheader()
            cw.writerows(data)
            output = si.getvalue().encode('utf-8')  # Encode in UTF-8
            return Response(output, mimetype='text/csv; charset=utf-8')  # Specify UTF-8 charset in MIME type
        elif output_format == 'xml':
            return Response(dicttoxml.dicttoxml(data).decode(), mimetype='application/xml')
        
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_data():
    data_types = request.json.get('data_types', [])
    num_entries = request.json.get('num_entries', 1)



    data = []
    for _ in range(num_entries):
        entry = {}
        if 'name' in data_types:
            entry['name'] = generate_name(locale)
        if 'address' in data_types:
            entry['address'] = generate_address(locale)
        if 'email' in data_types:
            entry['email'] = generate_email()
        if 'phone_number' in data_types:
            entry['phone_number'] = generate_phone_number(locale)
        if 'iban' in data_types:
            entry['iban'] = generate_iban()
        if 'sap_business_partner' in data_types:
            entry['sap_business_partner'] = generate_sap_business_partner()
        if 'sap_account' in data_types:
            entry['sap_account'] = generate_sap_account()
        data.append(entry)

    return jsonify(data)

@app.route('/swagger')
def swagger_json():
    return redirect(url_for('api.specs', _external=True))

if __name__ == '__main__':
    app.run(debug=True)