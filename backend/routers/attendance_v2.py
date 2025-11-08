"""
Version 2 API Routes - Placeholder for Future Development
This file demonstrates how to add a new API version without breaking existing clients
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from database import get_db
from schemas import AttendanceV2Create, AttendanceV2Response, MessageResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/attendance/",
    response_model=MessageResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Submit Attendance Record (V2 - Not Implemented)",
    description="Placeholder for version 2 API with different field names"
)
async def create_attendance_v2(
    attendance: AttendanceV2Create,
    db: Session = Depends(get_db)
):
    """
    POST endpoint for v2 API (not yet implemented)
    
    Future v2 schema might include:
    - Different field names (e.g., 'studentID' instead of 'student_id')
    - Additional fields (e.g., 'location', 'attendance_mode')
    - Changed validation rules
    """
    logger.info("V2 API endpoint called (not implemented)")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="API version 2 is not yet implemented. Please use /api/v1/attendance/"
    )

@router.get(
    "/attendance/",
    response_model=list[AttendanceV2Response],
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Get Attendance Records (V2 - Not Implemented)",
    description="Placeholder for version 2 API"
)
async def get_attendance_list_v2(
    db: Session = Depends(get_db)
):
    """
    GET endpoint for v2 API (not yet implemented)
    """
    logger.info("V2 API endpoint called (not implemented)")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="API version 2 is not yet implemented. Please use /api/v1/attendance/"
    )

# To enable v2 in the future:
# 1. Update schemas.py with complete AttendanceV2Base, AttendanceV2Create, AttendanceV2Response
# 2. Update models.py if database schema needs changes (or create a new table)
# 3. Update crud.py with v2-specific database operations
# 4. Implement the routes above
# 5. Add router to main.py: app.include_router(attendance_v2.router, prefix="/api/v2", tags=["Attendance V2"])