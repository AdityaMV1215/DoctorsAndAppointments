from pydantic import BaseModel


class PersonBase(BaseModel):
    first_name: str
    last_name: str


class PersonCreate(PersonBase):
    pass


class Doctor(PersonBase):
    id: int

    class Config:
        orm_mode = True

class Patient(PersonBase):
    id: int

    class Config:
        orm_mode = True

class Appointment(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_kind: str
    appointment_date: str
    appointment_time: str

    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_kind: str
    appointment_date: str
    appointment_time: str

    class Config:
        orm_mode = True