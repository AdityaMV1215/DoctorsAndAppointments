from sqlalchemy.orm import Session
import models, schemas


def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id)


def get_doctors_by_last_name(*, db: Session, skip: int = 0, limit: int = 100, last_name: str):
    return db.query(models.Doctor).filter(models.Doctor.last_name == last_name).offset(skip).limit(limit).all()


def get_patients_by_last_name(*, db: Session, skip: int = 0, limit: int = 100, last_name: str):
    return db.query(models.Patient).filter(models.Patient.last_name == last_name).offset(skip).limit(limit).all()


def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()


def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).all()

def get_appointments_by_doctor_and_day(db: Session, doctor_id: int, day: str, time: str = None, skip: int = 0,
                                       limit: int = 100):
    if time != None:
        return db.query(models.Appointment).filter(
            models.Appointment.doctor_id == doctor_id and models.Appointment.appointment_date == day
            and models.Appointment.appointment_time == time).offset(skip).limit(limit).all()
    else:
        return db.query(models.Appointment).filter(
            models.Appointment.doctor_id == doctor_id
            and models.Appointment.appointment_date == day).offset(skip).limit(limit).all()


def create_doctor(db: Session, doctor: schemas.PersonCreate):
    db_doctor = models.Doctor(first_name=doctor.first_name, last_name=doctor.last_name)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def create_patient(db: Session, patient: schemas.PersonCreate):
    db_patient = models.Patient(first_name=patient.first_name, last_name=patient.last_name)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(doctor_id=appointment.doctor_id, patient_id=appointment.patient_id,
                                        appointment_kind=appointment.appointment_kind,
                                        appointment_date=appointment.appointment_date,
                                        appointment_time=appointment.appointment_time)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    if len(get_appointment_by_id(db=db, appointment_id=appointment_id)) == 0:
        return False
    db.query(models.Appointment).filter(models.Appointment.id == appointment_id).delete()
    db.commit()
    return True

