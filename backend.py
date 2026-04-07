# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# In-memory database (replace with real DB in production)
patients = {}
appointments = {}
medical_records = {}

class Patient:
    def __init__(self, patient_id, name, dob, email, phone):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.email = email
        self.phone = phone
        self.created_at = datetime.now()

class Appointment:
    def __init__(self, apt_id, patient_id, doctor, date_time, reason):
        self.apt_id = apt_id
        self.patient_id = patient_id
        self.doctor = doctor
        self.date_time = date_time
        self.reason = reason
        self.status = "scheduled"

class MedicalRecord:
    def __init__(self, record_id, patient_id, diagnosis, treatment, date):
        self.record_id = record_id
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.date = date

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['GET', 'POST'])
def handle_patients():
    if request.method == 'POST':
        data = request.json
        patient_id = f"P{len(patients) + 1:04d}"
        patient = Patient(patient_id, data['name'], data['dob'], data['email'], data['phone'])
        patients[patient_id] = patient
        return jsonify({
            'status': 'success',
            'patient_id': patient_id,
            'message': 'Patient registered successfully'
        }), 201
    
    patient_list = [{
        'patient_id': p.patient_id,
        'name': p.name,
        'dob': p.dob,
        'email': p.email,
        'phone': p.phone
    } for p in patients.values()]
    return jsonify(patient_list), 200

@app.route('/api/patients/<patient_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_patient(patient_id):
    if patient_id not in patients:
        return jsonify({'error': 'Patient not found'}), 404
    
    if request.method == 'GET':
        p = patients[patient_id]
        return jsonify({
            'patient_id': p.patient_id,
            'name': p.name,
            'dob': p.dob,
            'email': p.email,
            'phone': p.phone
        }), 200
    
    elif request.method == 'PUT':
        data = request.json
        p = patients[patient_id]
        p.name = data.get('name', p.name)
        p.dob = data.get('dob', p.dob)
        p.email = data.get('email', p.email)
        p.phone = data.get('phone', p.phone)
        return jsonify({'status': 'success', 'message': 'Patient updated'}), 200
    
    elif request.method == 'DELETE':
        del patients[patient_id]
        return jsonify({'status': 'success', 'message': 'Patient deleted'}), 200

@app.route('/api/appointments', methods=['GET', 'POST'])
def handle_appointments():
    if request.method == 'POST':
        data = request.json
        apt_id = f"A{len(appointments) + 1:04d}"
        appointment = Appointment(apt_id, data['patient_id'], data['doctor'], 
                                 data['date_time'], data['reason'])
        appointments[apt_id] = appointment
        return jsonify({
            'status': 'success',
            'appointment_id': apt_id,
            'message': 'Appointment scheduled successfully'
        }), 201
    
    apt_list = [{
        'apt_id': a.apt_id,
        'patient_id': a.patient_id,
        'doctor': a.doctor,
        'date_time': a.date_time,
        'reason': a.reason,
        'status': a.status
    } for a in appointments.values()]
    return jsonify(apt_list), 200

@app.route('/api/appointments/<apt_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_appointment(apt_id):
    if apt_id not in appointments:
        return jsonify({'error': 'Appointment not found'}), 404
    
    if request.method == 'GET':
        a = appointments[apt_id]
        return jsonify({
            'apt_id': a.apt_id,
            'patient_id': a.patient_id,
            'doctor': a.doctor,
            'date_time': a.date_time,
            'reason': a.reason,
            'status': a.status
        }), 200
    
    elif request.method == 'PUT':
        data = request.json
        a = appointments[apt_id]
        a.status = data.get('status', a.status)
        a.doctor = data.get('doctor', a.doctor)
        a.date_time = data.get('date_time', a.date_time)
        return jsonify({'status': 'success', 'message': 'Appointment updated'}), 200
    
    elif request.method == 'DELETE':
        del appointments[apt_id]
        return jsonify({'status': 'success', 'message': 'Appointment cancelled'}), 200

@app.route('/api/medical-records', methods=['GET', 'POST'])
def handle_medical_records():
    if request.method == 'POST':
        data = request.json
        record_id = f"R{len(medical_records) + 1:04d}"
        record = MedicalRecord(record_id, data['patient_id'], data['diagnosis'], 
                              data['treatment'], data['date'])
        medical_records[record_id] = record
        return jsonify({
            'status': 'success',
            'record_id': record_id,
            'message': 'Medical record created successfully'
        }), 201
    
    records_list = [{
        'record_id': r.record_id,
        'patient_id': r.patient_id,
        'diagnosis': r.diagnosis,
        'treatment': r.treatment,
        'date': r.date
    } for r in medical_records.values()]
    return jsonify(records_list), 200

@app.route('/api/medical-records/<record_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_medical_record(record_id):
    if record_id not in medical_records:
        return jsonify({'error': 'Medical record not found'}), 404
    
    if request.method == 'GET':
        r = medical_records[record_id]
        return jsonify({
            'record_id': r.record_id,
            'patient_id': r.patient_id,
            'diagnosis': r.diagnosis,
            'treatment': r.treatment,
            'date': r.date
        }), 200
    
    elif request.method == 'PUT':
        data = request.json
        r = medical_records[record_id]
        r.diagnosis = data.get('diagnosis', r.diagnosis)
        r.treatment = data.get('treatment', r.treatment)
        return jsonify({'status': 'success', 'message': 'Medical record updated'}), 200
    
    elif request.method == 'DELETE':
        del medical_records[record_id]
        return jsonify({'status': 'success', 'message': 'Medical record deleted'}), 200

@app.route('/api/dashboard-stats')
def dashboard_stats():
    return jsonify({
        'total_patients': len(patients),
        'total_appointments': len(appointments),
        'total_records': len(medical_records),
        'upcoming_appointments': sum(1 for a in appointments.values() if a.status == 'scheduled')
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
