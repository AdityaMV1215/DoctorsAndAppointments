from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/insert-doctor", response_model=schemas.Doctor)
def insert_doctor(doctor: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db=db, doctor=doctor)

@app.post("/insert-patient", response_model=schemas.Patient)
def insert_patient(patient: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)

@app.post("/create-appointment", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appointment_time_minutes = appointment.appointment_time.split(":")[1]

    if int(appointment_time_minutes) % 15 != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Appointments can only be scheduled in 15 minute intervals")

    existing_appointments = crud.get_appointments_by_doctor_and_day(db=db, doctor_id=appointment.doctor_id,
                                                                    day=appointment.appointment_date,
                                                                    time=appointment.appointment_time)

    if len(existing_appointments) == 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No more than 3 appointments can be scheduled at the same time for a given doctor")

    return crud.create_appointment(db=db, appointment=appointment)

@app.delete("/delete-appointment/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_appointment(db=db, appointment_id=appointment_id)
    if is_deleted:
        return {"Status": "Deleted Appointment with Id {} successfully".format(appointment_id)}
    else:
        return {"Status": "Could not Delete Appointment with Id {} as it does not exist".format(appointment_id)}

@app.get("/get-appointments-by-doctor-and-date/{doctor_id}/{date}", response_model=List[schemas.Appointment])
def get_appointments_by_doctor_and_date(doctor_id: int, date: str, time: Optional[str] = None, skip: int = 0, limit: int = 100,
                                        db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_doctor_and_day(db=db, doctor_id=doctor_id, day=date, time=time, skip=skip, limit=limit)
    return appointments


@app.get("/get-doctors-by-last-name/{last_name}", response_model=List[schemas.Doctor])
def get_doctors_by_last_name(last_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = crud.get_doctors_by_last_name(db=db, skip=skip, limit=limit, last_name=last_name)
    return doctors

@app.get("/get-doctors", response_model=List[schemas.Doctor])
def get_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = crud.get_doctors(db=db, skip=skip, limit=limit)
    return doctors

@app.get("/get-patients-by-last-name/{last_name}", response_model=List[schemas.Patient])
def get_patients_by_last_name(last_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = crud.get_patients_by_last_name(db=db, skip=skip, limit=limit, last_name=last_name)
    return patients

@app.get("/get-patients", response_model=List[schemas.Doctor])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = crud.get_patients(db=db, skip=skip, limit=limit)
    return patients