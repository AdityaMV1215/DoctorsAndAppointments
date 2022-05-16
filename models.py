from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    #items = relationship("Item", back_populates="owner")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    #items = relationship("Item", back_populates="owner")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(
        Integer,
        ForeignKey('doctors.id', ondelete='NO ACTION'),
        nullable=False,
        # no need to add index=True, all FKs have indexes
    )
    doctor = relationship('Doctor', foreign_keys=[doctor_id])

    patient_id = Column(
        Integer,
        ForeignKey('patients.id', ondelete='NO ACTION'),
        nullable=False,
        # no need to add index=True, all FKs have indexes
    )
    patient = relationship('Patient', foreign_keys=[patient_id])

    appointment_kind = Column(String)
    appointment_date = Column(String, index=True)
    appointment_time = Column(String, index=True)

    #items = relationship("Item", back_populates="owner")


