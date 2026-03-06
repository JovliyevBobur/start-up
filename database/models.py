"""
Qishloq-AI Database Models
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, BigInteger, String, Float, DateTime, Text, Boolean, ForeignKey
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """Foydalanuvchi modeli"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    region = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    farm_size = Column(Float, nullable=True)  # gektarlarda
    soil_type = Column(String(100), nullable=True)
    main_crops = Column(String(500), nullable=True)  # vergul bilan ajratilgan
    is_premium = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    language = Column(String(10), default="uz")
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    soil_records = relationship("SoilRecord", back_populates="user", lazy="selectin")
    consultations = relationship("Consultation", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<User {self.telegram_id}: {self.full_name}>"


class SoilRecord(Base):
    """Tuproq tahlili yozuvlari"""
    __tablename__ = "soil_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    moisture = Column(Float, nullable=True)       # Namlik (%)
    temperature = Column(Float, nullable=True)     # Harorat (°C)
    ph = Column(Float, nullable=True)              # pH darajasi
    npk_n = Column(Float, nullable=True)           # Azot (mg/kg)
    npk_p = Column(Float, nullable=True)           # Fosfor (mg/kg)
    npk_k = Column(Float, nullable=True)           # Kaliy (mg/kg)
    ec = Column(Float, nullable=True)              # Elektr o'tkazuvchanlik (mS/cm)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="soil_records")

    def __repr__(self):
        return f"<SoilRecord {self.id} user={self.user_id}>"


class Consultation(Base):
    """Maslahat yozuvlari"""
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    consultation_type = Column(String(50), nullable=False)  # soil, irrigation, fertilizer, crop, disease, weather
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="consultations")

    def __repr__(self):
        return f"<Consultation {self.id} type={self.consultation_type}>"
