"""
CRUD Operations for Attendance Records
Database operations separated from route handlers
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import AttendanceRecord
from schemas import AttendanceV1Create
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def create_attendance_record(db: Session, attendance: AttendanceV1Create) -> AttendanceRecord:
    """
    Create a new attendance record in the database
    
    Args:
        db: Database session
        attendance: Pydantic model with attendance data
    
    Returns:
        Created AttendanceRecord instance
    """
    db_attendance = AttendanceRecord(
        student_name=attendance.student_name,
        student_id=attendance.student_id,
        timestamp=attendance.timestamp,
        bluetooth_signal_strength=attendance.bluetooth_signal_strength,
        status=attendance.status
    )
    
    try:
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        logger.info(f"Created attendance record: ID={db_attendance.id}, Student={attendance.student_id}")
        return db_attendance
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create attendance record: {str(e)}")
        raise

def get_attendance_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    student_id: Optional[str] = None
) -> List[AttendanceRecord]:
    """
    Retrieve attendance records with optional filtering
    
    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        student_id: Optional filter by student ID
    
    Returns:
        List of AttendanceRecord instances
    """
    query = db.query(AttendanceRecord)
    
    if student_id:
        query = query.filter(AttendanceRecord.student_id == student_id)
    
    records = query.order_by(desc(AttendanceRecord.timestamp)).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(records)} attendance records")
    return records

def get_attendance_by_id(db: Session, record_id: int) -> Optional[AttendanceRecord]:
    """
    Retrieve a single attendance record by ID
    
    Args:
        db: Database session
        record_id: Attendance record ID
    
    Returns:
        AttendanceRecord instance or None
    """
    return db.query(AttendanceRecord).filter(AttendanceRecord.id == record_id).first()

def get_total_count(db: Session, student_id: Optional[str] = None) -> int:
    """
    Get total count of attendance records
    
    Args:
        db: Database session
        student_id: Optional filter by student ID
    
    Returns:
        Total count of records
    """
    query = db.query(AttendanceRecord)
    
    if student_id:
        query = query.filter(AttendanceRecord.student_id == student_id)
    
    return query.count()

def delete_attendance_record(db: Session, record_id: int) -> bool:
    """
    Delete an attendance record by ID
    
    Args:
        db: Database session
        record_id: Attendance record ID
    
    Returns:
        True if deleted, False if not found
    """
    record = get_attendance_by_id(db, record_id)
    if record:
        db.delete(record)
        db.commit()
        logger.info(f"Deleted attendance record: ID={record_id}")
        return True
    return False