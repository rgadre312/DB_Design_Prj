from flask import Flask,request,jsonify 
from flask_cors import CORS,cross_origin
import mysql.connector
import datetime

app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS']="Content-Type"

dataBase = mysql.connector.connect(
host ="localhost",
user ="root",
passwd ="",
database = "HMS_prj",
connection_timeout = 500
)

cursorObject = dataBase.cursor(dictionary=True)

email_in_use = ""
password_in_use = ""
who = ""

@app.route('/checkIfPatientExists', methods=['GET'])
def check_if_patient_exists():
    email = request.args.get('email')
    cursorObject = dataBase.cursor(dictionary=True)
    statement = f"SELECT * FROM Patient WHERE email = '{email}'"
    cursorObject.execute(statement)
    results = cursorObject.fetchall()
    dataBase.commit()
    cursorObject.close()
    return jsonify(data=results)

@app.route('/checkIfDocExists', methods=['GET'])
def check_if_doc_exists():
    email = request.args.get('email')
    cursorObject = dataBase.cursor(dictionary=True)
    statement = f"SELECT * FROM Doctor WHERE email = '{email}'"
    cursorObject.execute(statement)
    results = cursorObject.fetchall()
    dataBase.commit()
    cursorObject.close()
    return jsonify(data=results)

@app.route('/makeAccount', methods=['GET'])
def make_account():
    query = request.args
    name = f"{query['name']} {query['lastname']}"
    email = query['email']
    password = query['password']
    address = query['address']
    gender = query['gender']
    medications = query.get('medications', 'none')
    conditions = query.get('conditions', 'none')
    surgeries = query.get('surgeries', 'none')
    statement = f"INSERT INTO Patient (email, password, name, address, gender) VALUES ({email}, {password}, {name}, {address}, {gender})"
    
    cursorObject = dataBase.cursor(dictionary=True)
    cursorObject.execute(statement)
    results = cursorObject.fetchall()
    dataBase.commit()
    cursorObject.close()

    global email_in_use
    global password_in_use
    global who

    email_in_use = email
    password_in_use = password
    who = "pat"
    
    return jsonify(data="Account created successfully")


@app.route('/makeDocAccount', methods=['GET'])
def make_doc_account():
    query = request.args
    name = f"{query['name']} {query['lastname']}"
    email = query['email']
    password = query['password']
    gender = query['gender']
    schedule_no= query['schedule']
    
    cursorObject = dataBase.cursor(dictionary=True)
    statement = f"INSERT INTO Doctor(email, gender, password, name) VALUES ({email},{gender}, {password}, {name})"
    cursorObject.execute(statement)
    dataBase.commit()
    cursorObject.close()

    cursorObject = dataBase.cursor(dictionary=True)
    statement = f"INSERT INTO DocsHaveSchedules(sched,doctor) VALUES ({schedule_no},{email})"
    cursorObject.execute(statement)
    dataBase.commit()
    cursorObject.close()

    global email_in_use
    global password_in_use
    global who

    email_in_use = email
    password_in_use = password
    who = "doc"
    
    return jsonify(data="Account created successfully")


@app.route('/checklogin', methods=['GET'])
def pat_login():
    query=request.args
    email = query['email']
    password = query['password']

    cursorObject = dataBase.cursor(dictionary=True)
    statement=f"SELECT password from Patient where email='{email}'"
    cursorObject.execute(statement)
    results = cursorObject.fetchall()
    dataBase.commit()
    cursorObject.close()

    global email_in_use
    global password_in_use
    global who
    
    if(bool(results)):
        if(results[0]['password']==password):
            email_in_use = email
            password_in_use = password
            who = "pat"
            return jsonify(data=True)
        else:
            return jsonify(data='')
    else:
        return jsonify(data='')

@app.route('/checkDoclogin', methods=['GET'])
def doc_login():
    query=request.args
    email = query['email']
    password = query['password']

    cursorObject = dataBase.cursor(dictionary=True)
    statement=f"SELECT password from Doctor where email='{email}'"
    cursorObject.execute(statement)
    results = cursorObject.fetchall()
    dataBase.commit()
    cursorObject.close()
    
    global email_in_use
    global password_in_use
    global who

    if(bool(results)):
        if(results[0]['password']==password):
            email_in_use = email
            password_in_use = password
            who = "doc"
            return jsonify(data=True)
        else:
            return jsonify(data='')
    else:
        return jsonify(data='')


@app.route('/checkIfApptExists', methods=['GET'])
def check_if_appointment_exists():
        query=request.args
        email = query.get('email')
        doc_email = query.get('docEmail')
        start_time = query.get('startTime')
        date = query.get('date')

        date_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        ndate = date_obj.strftime('%Y-%m-%d')
    
        sql_date = f"STR_TO_DATE('{ndate}', '%d/%m/%Y')"
        sql_start = f"CONVERT('{start_time}', TIME)"

        cursor = dataBase.cursor()

        statement = f'SELECT * FROM PatientsAttendAppointments, Appointment WHERE patient = "{email}" AND appt = id AND date = {sql_date} AND starttime = {sql_start}'
        cursor.execute(statement)
        cond1 = cursor.fetchall()
       
        statement = f'SELECT * FROM Diagnose d INNER JOIN Appointment a ON d.appt=a.id WHERE doctor="{doc_email}" AND date={sql_date} AND status="NotDone" AND {sql_start} >= starttime AND {sql_start} < endtime'
        cursor.execute(statement)
        cond2 = cursor.fetchall()

        
        statement = f'SELECT doctor, starttime, endtime, breaktime, day FROM DocsHaveSchedules INNER JOIN Schedule ON DocsHaveSchedules.sched=Schedule.id WHERE doctor="{doc_email}" AND day=DAYNAME({sql_date}) AND (DATE_ADD({sql_start},INTERVAL +1 HOUR) <= breaktime OR {sql_start} >= DATE_ADD(breaktime,INTERVAL +1 HOUR))'
        cursor.execute(statement)
        cond3 = cursor.fetchall()
        dataBase.commit()
        cursor.close()
        return jsonify(data=cond1 + cond2 + cond3)

@app.route('/genApptUID', methods=['GET'])
def gen_appt_UID():
        cursor = dataBase.cursor()
        statement = 'SELECT id FROM Appointment ORDER BY id DESC LIMIT 1;'
        cursor.execute(statement)
        results = cursor.fetchall()
        dataBase.commit()
        cursor.close()

        return jsonify(data={'id': results[0][0]+1})

@app.route('/schedule', methods=['GET'])
def schedule():
    query=request.args

    time = query.get('time')
    endTime = query.get('endTime')
    date = query.get('date')
    concerns = query.get('concerns')
    symptoms = query.get('symptoms')
    query_id = query.get('id')
    doc = query.get('doc')

    ndate = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
    
    sql_date = f"STR_TO_DATE('{ndate}', '%Y-%m-%d')"
    sql_start = f"CONVERT('{time}', TIME)"
    sql_end = f"CONVERT('{endTime}', TIME)"

    cursor = dataBase.cursor()
    statement1 = f'INSERT INTO Appointment (id, `date`, starttime, endtime, `status`) VALUES ({query_id}, {sql_date}, {sql_start}, {sql_end}, "NotDone")'
    cursor.execute(statement1)
    results1 = cursor.fetchall()

    statement2 = f'INSERT INTO Diagnose (appt, doctor, diagnosis, prescription) VALUES ({query_id}, "{doc}", "Not Yet Diagnosed" , "Not Yet Diagnosed")'
    cursor.execute(statement2)
    results2 = cursor.fetchall()

    dataBase.commit()
    cursor.close()

    return (jsonify(data=results2))

@app.route('/addToPatientSeeAppt', methods=['GET'])
def add_patient_attnd_appt():
    query=request.args

    email = query.get('email')
    concerns = query.get('concerns')
    symptoms = query.get('symptoms')
    appt_id = query.get('id')
   
    cursor = dataBase.cursor()
    statement = f'INSERT INTO PatientsAttendAppointments (patient, appt, concerns, symptoms) VALUES ("{email}", {appt_id}, "{concerns}", "{symptoms}")'
    cursor.execute(statement)
    results = cursor.fetchall()

    dataBase.commit()
    cursor.close()

    return (jsonify(data=results))


@app.route('/resetPasswordPatient', methods=['POST'])
def reset_password_patient():

        query=request.args
        email = query.get('email')
        old_password = str(query.get('oldPassword', ''))
        new_password = str(query.get('newPassword', ''))

        cursor = dataBase.cursor()
        statement = f"UPDATE Patient SET password = '{new_password}' WHERE email = '{email}' AND password = '{old_password}';"
        cursor.execute(statement)
        dataBase.commit()
        cursor.close()

        return jsonify(data="Password updated successfully")

@app.route('/resetPasswordDoctor', methods=['POST'])
def reset_password_doctor():

        query=request.args
        email = query.get('email')
        old_password = str(query.get('oldPassword', ''))
        new_password = str(query.get('newPassword', ''))

        cursor = dataBase.cursor()
        statement = f"UPDATE Doctor SET password = '{new_password}' WHERE email = '{email}' AND password = '{old_password}';"
        cursor.execute(statement)
        dataBase.commit()
        cursor.close()

        return jsonify(data="Password updated successfully")


@app.route('/docInfo', methods=['GET'])
def get_doctor_info():

        cursor = dataBase.cursor()
        statement = 'SELECT * FROM Doctor'
        cursor.execute(statement)
        results = cursor.fetchall()
        dataBase.commit()
        cursor.close()

        return jsonify(data=results)

@app.route('/patientViewAppt', methods=['GET'])
def patient_view_appointments():
        data = request.args
        email = data.get('email', '')

        cursor = dataBase.cursor()
        statement = f"SELECT PatientsAttendAppointments.appt as ID,PatientsAttendAppointments.patient as user,PatientsAttendAppointments.concerns as theConcerns,PatientsAttendAppointments.symptoms as theSymptoms, Appointment.date as theDate,Appointment.starttime as theStart,Appointment.endtime as theEnd,Appointment.status as status FROM PatientsAttendAppointments,Appointment WHERE PatientsAttendAppointments.patient = '{email}' AND PatientsAttendAppointments.appt = Appointment.id;"
        cursor.execute(statement)
        results = cursor.fetchall()
        dataBase.commit()
        cursor.close()

        serialized_results = []
        for result in results:
            serialized_result = {
                'ID': result[0],
                'user': result[1],
                'theConcerns': result[2],
                'theSymptoms': result[3],
                'theDate': result[4].strftime('%Y-%m-%d'), 
                'theStart': str(result[5]),   
                'theEnd': str(result[6]),      
                'status': result[7]
            }
            serialized_results.append(serialized_result)

        return jsonify(data=serialized_results)

@app.route('/doctorViewAppt', methods=['GET'])
def get_doc_appointments():
    statement = f'SELECT a.id,a.date, a.starttime, a.status, p.name, psa.concerns, psa.symptoms FROM Appointment a, PatientsAttendAppointments psa, Patient p WHERE a.id = psa.appt AND psa.patient = p.email AND a.id IN (SELECT appt FROM Diagnose WHERE doctor="{email_in_use}")'
    
    cursorObject = dataBase.cursor(dictionary=True)
    cursorObject.execute(statement)
    results = cursorObject.fetchall()
    dataBase.commit()
    cursorObject.close()

    for result in results:
        result['date'] = str(result['date'])
        result['starttime'] = str(result['starttime'])

    return jsonify({"data": results})

@app.route('/showDiagnoses', methods=['GET'])
def show_diagnoses():
        data = request.args
        appointment_id = data.get('id', '')

        cursor = dataBase.cursor()
        statement = f"SELECT * FROM Diagnose WHERE appt='{appointment_id}';"
        cursor.execute(statement)
        results = cursor.fetchall()
        dataBase.commit()
        cursor.close()

        return jsonify(data=results)

@app.route('/OneHistory', methods=['GET'])
def get_one_history():
        data = request.args
        patient_email = data.get('patientEmail', '')
        cursor = dataBase.cursor()

        statement = f"SELECT gender, name, email, address, conditions, surgeries, medication FROM PatientsFillHistory, Patient, MedicalHistory WHERE PatientsFillHistory.history = id AND email = '{patient_email}' AND patient = email"
        # if(who == 'doc'):
        #     statement = f"SELECT gender, name, email, address, conditions, surgeries, medication FROM PatientsFillHistory, Patient, MedicalHistory WHERE PatientsFillHistory.history = id AND email = '{patient_email}' AND patient = email"
        # else:
        #     statement = f"SELECT gender, name, email, address, conditions, surgeries, medication FROM PatientsFillHistory, Patient, MedicalHistory WHERE PatientsFillHistory.history = id AND email = '{patient_email}' AND patient = email"
        print(f'statement --------> {statement}')
        cursor.execute(statement)
        results = cursor.fetchall()
        dataBase.commit()
        cursor.close()

        return jsonify(data=results)

@app.route('/allDiagnoses', methods=['GET'])
def get_all_diagnoses():

        data = request.args
        patient_email = data.get('patientEmail', '')
        cursor = dataBase.cursor()
        if(who == 'doc'):
            statement = f"SELECT A.date,D.doctor,PAA.concerns,PAA.symptoms,D.diagnosis,D.prescription FROM Appointment A INNER JOIN PatientsAttendAppointments PAA ON A.id = PAA.appt AND PAA.patient = '{patient_email}' INNER JOIN Diagnose D ON PAA.appt = D.appt;"
        else:
            statement = f"SELECT A.date,D.doctor,PAA.concerns,PAA.symptoms,D.diagnosis,D.prescription FROM Appointment A INNER JOIN PatientsAttendAppointments PAA ON A.id = PAA.appt AND PAA.patient = '{patient_email[1:-1]}' INNER JOIN Diagnose D ON PAA.appt = D.appt;"
            
        cursor.execute(statement)
        results = cursor.fetchall()
        dataBase.commit()
        cursor.close()
        return jsonify(data=results)

@app.route('/MedHistView', methods=['GET'])
def view_medical_history():
    data = request.args
    name = data.get('name')

    statement = f"SELECT name AS Name, PatientsFillHistory.history AS ID, email FROM Patient,PatientsFillHistory WHERE Patient.email = PatientsFillHistory.patient AND Patient.email IN (SELECT patient from PatientsAttendAppointments NATURAL JOIN Diagnose WHERE doctor='{email_in_use}')"
    if (name!=""):
        statement += f" AND Patient.name LIKE '{name}'"

    cursor = dataBase.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    dataBase.commit()
    cursor.close()

    return (jsonify(data=results))

@app.route('/userInSession', methods=['GET'])
def get_user_in_session():
    user_data = {"email": email_in_use, 'who': who}
    return jsonify(user_data)

@app.route('/endSession', methods=['GET'])
def signout():
    global email_in_use
    global password_in_use
    global who

    email_in_use = ''
    password_in_use = ''
    who = ''

    return jsonify({'data': 'Ended'})

if __name__ == " __main__":
    app.run(debug=True, host='0.0.0.0', port=3001)
