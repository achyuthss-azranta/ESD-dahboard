import json
import csv
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Load data from CSV into a dictionary
def load_csv_data(file_path):
    devices = {}
    with open(file_path, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            device_id = row['Device']
            devices[device_id] = {
                'MAT_STATUS': int(row['MAT_STATUS']),
                'BAND_STATUS': int(row['BAND_STATUS']),
                'ESD_STATUS': row['ESD_STATUS']
            }
    return devices

# Load initial data from a test CSV file
devices = load_csv_data('test_devices.csv')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    return jsonify(devices)

if __name__ == '__main__':
    app.run(debug=True)
