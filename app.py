from flask import Flask, render_template, request
import random
import string
import faker

app = Flask(__name__)
fake = faker.Faker()

def generate_name():
    return fake.name()

def generate_address():
    return fake.address().replace('\n', ', ')

def generate_email():
    return fake.email()

def generate_phone_number():
    return fake.phone_number()

def generate_iban():
    return fake.iban()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        num_entries = int(request.form.get('num_entries'))
        data_types = request.form.getlist('data_type')
        data = []
        for _ in range(num_entries):
            entry = {}
            if 'name' in data_types:
                entry['name'] = generate_name()
            if 'address' in data_types:
                entry['address'] = generate_address()
            if 'email' in data_types:
                entry['email'] = generate_email()
            if 'phone_number' in data_types:
                entry['phone_number'] = generate_phone_number()
            if 'iban' in data_types:
                entry['iban'] = generate_iban()
            data.append(entry)
        return render_template('test_data.html', data=data, data_types=data_types)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)