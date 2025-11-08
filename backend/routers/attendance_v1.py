"""
Version 1 API Routes for Attendance Management
Handles POST and GET requests for attendance records
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging
import json

from database import get_db
from schemas import (
    AttendanceV1Create, 
    AttendanceV1Response, 
    AttendanceV1ListResponse,
    MessageResponse
)
import crud

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/attendance/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Attendance Record",
    description="Receives attendance data from Android app and stores in database"
)
async def create_attendance(
    attendance: AttendanceV1Create,
    db: Session = Depends(get_db)
):
    """
    POST endpoint to receive attendance data from Android app
    
    Request body example:
    ```json
    {
      "student_id": "STU123",
      "device_mac": "AA:BB:CC:DD:EE:FF",
      "timestamp": "2025-11-08T10:30:00",
      "bluetooth_signal_strength": -45,
      "status": "present"
    }
    ```
    """
    try:
        # Log received JSON
        logger.info(f"Received attendance data: {attendance.model_dump_json()}")
        
        # Create record in database
        db_record = crud.create_attendance_record(db, attendance)
        
        # Log success
        logger.info(f"✓ Attendance stored - Record ID: {db_record.id}, Student: {attendance.student_id}")
        
        return MessageResponse(message="Attendance record stored successfully")
        
    except Exception as e:
        logger.error(f"✗ Failed to store attendance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store attendance record: {str(e)}"
        )

@router.get(
    "/attendance/",
    response_model=AttendanceV1ListResponse,
    summary="Get All Attendance Records",
    description="Fetches attendance records for React frontend with pagination and filtering"
)
async def get_attendance_list(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    student_id: Optional[str] = Query(None, description="Filter by student ID"),
    db: Session = Depends(get_db)
):
    """
    GET endpoint to fetch attendance records (for React frontend)
    
    Query parameters:
    - skip: Pagination offset (default: 0)
    - limit: Maximum records to return (default: 100)
    - student_id: Optional filter by student ID
    
    Response example:
    ```json
    {
      "total": 150,
      "records": [
        {
          "id": 1,
          "student_id": "STU123",
          "device_mac": "AA:BB:CC:DD:EE:FF",
          "timestamp": "2025-11-08T10:30:00",
          "bluetooth_signal_strength": -45,
          "status": "present",
          "created_at": "2025-11-08T10:30:05",
          "updated_at": null
        }
      ]
    }
    ```
    """
    try:
        # Log request
        logger.info(f"Fetching attendance records - skip: {skip}, limit: {limit}, student_id: {student_id}")
        
        # Get records from database
        records = crud.get_attendance_records(db, skip=skip, limit=limit, student_id=student_id)
        total = crud.get_total_count(db, student_id=student_id)
        
        # Log response
        logger.info(f"✓ Returning {len(records)} records (total: {total})")
        
        return AttendanceV1ListResponse(
            total=total,
            records=records
        )
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch attendance records: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance records: {str(e)}"
        )

@router.get(
    "/attendance/{record_id}",
    response_model=AttendanceV1Response,
    summary="Get Single Attendance Record",
    description="Fetch a specific attendance record by ID"
)
async def get_attendance_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    GET endpoint to fetch a single attendance record by ID
    """
    try:
        logger.info(f"Fetching attendance record ID: {record_id}")
        
        record = crud.get_attendance_by_id(db, record_id)
        
        if not record:
            logger.warning(f"✗ Attendance record not found: ID={record_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance record with ID {record_id} not found"
            )
        
        logger.info(f"✓ Found attendance record: ID={record_id}")
        return record
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to fetch attendance record: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance record: {str(e)}"
        )

@router.delete(
    "/attendance/{record_id}",
    response_model=MessageResponse,
    summary="Delete Attendance Record",
    description="Delete a specific attendance record by ID"
)
async def delete_attendance(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    DELETE endpoint to remove an attendance record
    """
    try:
        logger.info(f"Attempting to delete attendance record ID: {record_id}")
        
        deleted = crud.delete_attendance_record(db, record_id)
        
        if not deleted:
            logger.warning(f"✗ Attendance record not found: ID={record_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance record with ID {record_id} not found"
            )
        
        logger.info(f"✓ Deleted attendance record: ID={record_id}")
        return MessageResponse(message="Attendance record deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Failed to delete attendance record: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attendance record: {str(e)}"
        )