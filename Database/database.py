import mysql.connector
import pandas as pd
import os

mydb = mysql.connector.connect(
    host="localhost",
    port=os.environ["DBPort"],
    user="root",
    password=os.environ["DBP"],
    database="petclinic"
)

cursor = mydb.cursor()


def addOwner(ssn, fname, lname, dob, pnum=None, email=None):
    global mydb
    global cursor

    if pnum is None:
        pnum = 'NULL'

    if email is None:
        email = 'NULL'

    ownerTuple = (ssn, fname, lname, dob, pnum, email)

    sqlLine = 'INSERT INTO owners(SSN, fname, lname, date_of_birth, phone_number, email) ' \
              'VALUES (%s, %s, %s, %s, %s, %s)'

    cursor.execute(sqlLine, ownerTuple)
    mydb.commit()


def addPet(name, dob, pet_type, owner_ssn):
    global mydb
    global cursor
    petTuple = (name, dob, pet_type, owner_ssn)

    sqlLine = 'SELECT * FROM owners WHERE SSN = ' + str(owner_ssn)
    cursor.execute(sqlLine)
    check = cursor.fetchone()
    if check is None:
        print("No owner SSN found")
        return False

    sqlLine = 'INSERT INTO pets(pet_name, date_of_birth, pet_type, owner_SSN) ' \
              'VALUES (%s, %s, %s, %s)'

    cursor.execute(sqlLine, petTuple)
    mydb.commit()


def addDoctor(doctor_id, fname, lname, dob, pnum=None, email=None):
    global mydb
    global cursor

    if pnum is None:
        pnum = 'NULL'

    if email is None:
        email = 'NULL'

    doctorTuple = (doctor_id, fname, lname, dob, pnum, email)

    sqlLine = 'INSERT INTO doctors(doctorID, fname, lname, date_of_birth, phone_number, email) ' \
              'VALUES (%s, %s, %s, %s, %s, %s)'

    cursor.execute(sqlLine, doctorTuple)
    mydb.commit()


def addAppointment(expected_date, pet_id, doctor_id, status):
    global mydb
    global cursor

    sqlLine = 'SELECT * FROM pets WHERE petID = ' + str(pet_id)
    cursor.execute(sqlLine)
    check = cursor.fetchone()
    if check is None:
        print("No petID found")
        return False

    sqlLine = 'SELECT * FROM doctors WHERE doctorID = ' + str(doctor_id)
    cursor.execute(sqlLine)
    check = cursor.fetchone()
    if check is None:
        print("No doctorID found")
        return False

    apptTuple = (expected_date, pet_id, doctor_id, status)
    sqlLine = 'INSERT INTO appointments(expected_date, petID, doctorID, status) ' \
              'VALUES (%s, %s, %s, %s)'

    cursor.execute(sqlLine, apptTuple)
    mydb.commit()


def updateOwner(owner_ssn, new_ssn=None, fname=None, lname=None, dob=None, pnum=None, email=None):
    global mydb
    global cursor
    ownerList = [new_ssn, fname, lname, dob, pnum, email]

    sqlLine = 'SELECT * FROM owners WHERE SSN = ' + str(owner_ssn)
    cursor.execute(sqlLine)
    tmp = cursor.next()

    for x in range(0, 6):
        if ownerList[x] is None:
            ownerList[x] = str(tmp[x])

    sqlLine = 'UPDATE owners SET ' \
              'SSN = %s, fname = %s, lname = %s, date_of_birth = %s, phone_number = %s, email = %s ' \
              'WHERE SSN = ' + str(owner_ssn)

    cursor.execute(sqlLine, ownerList)
    mydb.commit()


def updatePet(pet_id, pet_name=None, dob=None, pet_type=None, owner_ssn=None):
    global mydb
    global cursor
    petList = [pet_name, dob, pet_type, owner_ssn]

    sqlLine = 'SELECT * FROM pets WHERE petID = ' + str(pet_id)
    cursor.execute(sqlLine)
    check = cursor.fetchone()
    if check is None:
        print("No petID found")
        return False

    sqlLine = 'SELECT pet_name, date_of_birth, pet_type, owner_SSN FROM pets WHERE petID = ' + str(pet_id)
    cursor.execute(sqlLine)
    tmp = cursor.next()

    for x in range(0, 4):
        if petList[x] is None:
            petList[x] = str(tmp[x])

    sqlLine = 'UPDATE pets SET ' \
              'pet_name = %s, date_of_birth = %s, pet_type = %s, owner_SSN = %s ' \
              'WHERE petID = ' + str(pet_id)

    cursor.execute(sqlLine, petList)
    mydb.commit()


def updateDoctor(doctor_id, new_id=None, fname=None, lname=None, dob=None, pnum=None, email=None):
    global mydb
    global cursor
    doctorList = [new_id, fname, lname, dob, pnum, email]

    sqlLine = 'SELECT * FROM doctors WHERE doctorID = ' + str(doctor_id)
    cursor.execute(sqlLine)
    tmp = cursor.next()

    for x in range(0, 6):
        if doctorList[x] is None:
            doctorList[x] = str(tmp[x])

    sqlLine = 'UPDATE doctors SET ' \
              'doctorID = %s, fname = %s, lname = %s, date_of_birth = %s, phone_number = %s, email = %s ' \
              'WHERE doctorID = ' + str(doctor_id)

    cursor.execute(sqlLine, doctorList)
    mydb.commit()


def updateAppointment(appointment_id, new_date=None, new_pet_id=None, new_doctor_id=None, new_status=None):
    global mydb
    global cursor

    sqlLine = 'SELECT * FROM pets WHERE petID = ' + str(new_pet_id)
    cursor.execute(sqlLine)
    check = cursor.fetchone()
    if check is None:
        print("No petID found")
        return False

    sqlLine = 'SELECT * FROM doctors WHERE doctorID = ' + str(new_doctor_id)
    cursor.execute(sqlLine)
    check = cursor.fetchone()
    if check is None:
        print("No doctorID found")
        return False

    sqlLine = 'SELECT expected_date, petID, doctorID, status FROM appointments WHERE ID = ' + str(appointment_id)
    cursor.execute(sqlLine)
    tmp = cursor.next()

    if new_date is None:
        new_date = tmp[0]

    if new_pet_id is None:
        new_pet_id = tmp[1]

    if new_doctor_id is None:
        new_doctor_id = tmp[2]

    if new_status is None:
        new_status = tmp[3]

    sqlLine = 'UPDATE appointments SET ' \
              'expected_date = %s, petID = %s, doctorID = %s, status = %s ' \
              'WHERE ID = ' + str(appointment_id)
    apptList = [new_date, new_pet_id, new_doctor_id, new_status]

    cursor.execute(sqlLine, apptList)
    mydb.commit()


def delOwner(owner_ssn):
    global mydb
    global cursor

    sqlLine = 'SELECT petID from pets WHERE owner_SSN = ' + str(owner_ssn)
    cursor.execute(sqlLine)
    for petId in cursor:
        delPet(petId[0])

    sqlLine = 'DELETE FROM owners WHERE SSN = ' + str(owner_ssn)
    cursor.execute(sqlLine)
    mydb.commit()


def delPet(pet_id):
    global mydb
    global cursor

    sqlLine = 'DELETE FROM appointments WHERE petID = ' + str(pet_id)
    cursor.execute(sqlLine)
    mydb.commit()

    sqlLine = 'DELETE FROM pets WHERE petID = ' + str(pet_id)
    cursor.execute(sqlLine)
    mydb.commit()


def delDoctor(doctor_id):
    global mydb
    global cursor

    sqlLine = 'DELETE FROM appointments WHERE doctorID = ' + str(doctor_id)
    cursor.execute(sqlLine)
    mydb.commit()

    sqlLine = 'DELETE FROM doctors WHERE doctorID = ' + str(doctor_id)
    cursor.execute(sqlLine)
    mydb.commit()


def delAppointment(appointment_id):
    global mydb
    global cursor

    sqlLine = 'DELETE FROM appointments WHERE ID = ' + str(appointment_id)

    cursor.execute(sqlLine)
    mydb.commit()


def getOwners(offset, limit, name=None, ssn=None):
    if name is None or name == '':
        name = ' '
    if ssn is not None and ssn != '':
        ssn = 'SSN = \'' + str(ssn) + '\' '
    else:
        ssn = 'SSN '

    fullname = name.split(' ')
    sqlLine = 'SELECT o.*, COUNT(petID) AS "pets" FROM owners o ' \
              'LEFT JOIN pets p ON o.SSN = p.owner_SSN ' \
              'WHERE (o.fname LIKE \'' + fullname[0] + '%\'' + 'OR o.lname LIKE \'' + fullname[0] + '%\') ' \
              'AND ' + ssn + 'GROUP BY SSN ORDER BY o.fname LIMIT ' + str(offset) + ', ' + str(limit)

    cursor.execute(sqlLine)
    result = cursor.fetchall()
    owners = pd.DataFrame(result, columns=["SSN", "First name", "Last name", "Date of birth",
                                           "Phone number", "Email", "Pets"])

    return owners


def getPets(offset, limit, name=None, pet_id=None):
    if name is None or name == '':
        name = ''
    if pet_id is not None and pet_id != '':
        pet_id = 'petID = \'' + str(pet_id) + '\' '
    else:
        pet_id = 'petID '

    sqlLine = 'SELECT p.*, CONCAT(o.fname, " ", o.lname) AS "owner name" FROM pets p ' \
              'LEFT JOIN owners o ON p.owner_SSN = o.SSN ' \
              'WHERE (p.pet_name LIKE ' + '\'' + name + '%\' ' \
              'OR p.pet_type LIKE ' + '\'' + name + '%\' ' \
              'OR CONCAT(o.fname, " ", o.lname) like \'%' + name + '%\') AND ' + str(pet_id) + \
              'LIMIT ' + str(offset) + ', ' + str(limit)

    cursor.execute(sqlLine)
    result = cursor.fetchall()
    pets = pd.DataFrame(result, columns=["Pet ID", "Pet name", "Date of birth", "Pet Type", "Owner SSN", "Owner Name"])

    return pets


def getDoctors(offset, limit, name=None, doctor_id=None):
    if name is None or name == '':
        name = ' '
    if doctor_id is not None and doctor_id != '':
        doctor_id = 'd.doctorID = \'' + str(doctor_id) + '\' '
    else:
        doctor_id = 'd.doctorID '

    fullname = name.split(' ')
    sqlLine = 'SELECT d.*, COUNT(a.doctorID) Meetings FROM doctors d ' \
              'LEFT JOIN appointments a ON a.doctorID = d.doctorID ' \
              'WHERE (d.fname LIKE \'' + fullname[0] + '%\'' + 'OR d.lname LIKE \'' + fullname[1] + '%\') ' \
              'AND ' + doctor_id + \
              'GROUP BY doctorID ORDER BY fname LIMIT ' + str(offset) + ', ' + str(limit)

    cursor.execute(sqlLine)
    result = cursor.fetchall()
    doctors = pd.DataFrame(result, columns=["Doctor ID", "First Name", "Last Name", "Date of birth",
                                            "Phone number", "Email", "Meetings"])
    return doctors


def getAppointments(offset, limit, name=None, appt_id=None):
    if name is None or name == '':
        name = ''
    if appt_id is not None and appt_id != '':
        appt_id = 'ID = \'' + str(appt_id) + '\' '
    else:
        appt_id = 'ID '

    sqlLine = 'SELECT a.id, a.expected_date, a.petID, p.pet_name, ' \
              'p.owner_SSN, CONCAT(o.fname, " ", o.lname) AS "owner name", ' \
              'a.doctorID, CONCAT(d.fname, " ", d.lname) AS "doctor Name", a.status FROM appointments a ' \
              'LEFT JOIN pets p ON a.petID = p.petID ' \
              'LEFT JOIN doctors d ON a.doctorID = d.doctorID ' \
              'LEFT JOIN owners o ON p.owner_SSN = o.SSN ' \
              'WHERE (p.pet_name like \'' + name + '%\' ' \
              'OR CONCAT(o.fname, " ", o.lname) like \'%' + name + '%\' ' \
              'OR CONCAT(d.fname, " ", d.lname) like \'%' + name + '%\') ' \
              'AND ' + appt_id + 'ORDER BY expected_date DESC LIMIT ' + str(offset) + ', ' + str(limit)
    cursor.execute(sqlLine)
    result = cursor.fetchall()
    appointments = pd.DataFrame(result, columns=["ID", "Expected date", "Pet ID", "Pet Name",
                                                 "Owner SSN", "Owner Name",
                                                 "Doctor ID", "Doctor Name", "Status"])

    return appointments


def normalAppointment(key):
    global mydb
    global cursor

    sqlLine = 'SELECT expected_date, petID, doctorID, status FROM appointments WHERE ID = ' + str(key)
    cursor.execute(sqlLine)
    res = cursor.fetchone()
    return res


def normalOwner(key):
    global mydb
    global cursor

    sqlLine = 'SELECT * FROM owners WHERE SSN = ' + str(key)
    cursor.execute(sqlLine)
    res = cursor.fetchone()
    return res


def normalPet(key):
    global mydb
    global cursor

    sqlLine = 'SELECT * FROM pets WHERE petID = ' + str(key)
    cursor.execute(sqlLine)
    res = cursor.fetchone()
    return res


def normalDoctor(key):
    global mydb
    global cursor

    sqlLine = 'SELECT * FROM doctors WHERE doctorID = ' + str(key)
    cursor.execute(sqlLine)
    res = cursor.fetchone()
    return res
