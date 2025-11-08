"""
SQLAlchemy Database Models
Defines the database schema for attendance records
"""
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from database import Base

class AttendanceRecord(Base):
    """
    Attendance record model for storing student attendance data
    Compatible with v1 API schema
    """
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_name = Column(String(100), nullable=False)
    student_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    bluetooth_signal_strength = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False, default="present")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<AttendanceRecord(id={self.id}, student_id={self.student_id}, status={self.status})>"