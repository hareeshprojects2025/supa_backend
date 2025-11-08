"""
Pydantic Schemas for Request/Response Validation
Versioned schemas allow future API changes without breaking existing clients
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# ==================== VERSION 1 SCHEMAS ====================

class AttendanceV1Base(BaseModel):
    """Base schema for v1 attendance data"""
    student_name: str = Field(..., min_length=1, max_length=100, description="Student full name")
    student_id: str = Field(..., min_length=1, max_length=50, description="Unique student identifier/token")
    timestamp: datetime = Field(..., description="Attendance timestamp")
    bluetooth_signal_strength: Optional[int] = Field(None, ge=-100, le=0, description="Signal strength in dBm")
    status: str = Field(..., pattern=r"^(present|absent|late)$", description="Attendance status")


class AttendanceV1Create(AttendanceV1Base):
    """Schema for creating v1 attendance records (from Android app)"""
    model_config = ConfigDict(
        extra='ignore',  # Ignore extra fields gracefully
        json_schema_extra={
            "example": {
                "student_name": "John Doe",
                "student_id": "STU123",
                "timestamp": "2025-11-08T10:30:00",
                "bluetooth_signal_strength": -45,
                "status": "present"
            }
        }
    )

class AttendanceV1Response(AttendanceV1Base):
    """Schema for returning v1 attendance records (to React frontend)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class AttendanceV1ListResponse(BaseModel):
    """Schema for listing multiple attendance records"""
    total: int
    records: list[AttendanceV1Response]

class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Attendance record stored successfully"
            }
        }
    )

# ==================== VERSION 2 SCHEMAS (PLACEHOLDER) ====================

# ==================== VERSION 2 SCHEMAS (PLACEHOLDER) ====================

class AttendanceV2Base(BaseModel):
    """
    Placeholder for v2 schema with potentially different field names
    Example: 'student_id' might become 'studentID' or 'user_identifier'
    """
    pass

class AttendanceV2Create(AttendanceV2Base):
    """Placeholder for v2 create schema"""
    pass

class AttendanceV2Response(AttendanceV2Base):
    """Placeholder for v2 response schema"""
    pass#, description="Attendance status")

class AttendanceV1Create(AttendanceV1Base):
    """Schema for creating v1 attendance records (from Android app)"""
    model_config = ConfigDict(
        extra='ignore',  # Ignore extra fields gracefully
        json_schema_extra={
            "example": {
                "student_id": "STU123",
                "device_mac": "AA:BB:CC:DD:EE:FF",
                "timestamp": "2025-11-08T10:30:00",
                "bluetooth_signal_strength": -45,
                "status": "present"
            }
        }
    )

class AttendanceV1Response(AttendanceV1Base):
    """Schema for returning v1 attendance records (to React frontend)"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class AttendanceV1ListResponse(BaseModel):
    """Schema for listing multiple attendance records"""
    total: int
    records: list[AttendanceV1Response]

class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Attendance record stored successfully"
            }
        }
    )

# ==================== VERSION 2 SCHEMAS (PLACEHOLDER) ====================

class AttendanceV2Base(BaseModel):
    """
    Placeholder for v2 schema with potentially different field names
    Example: 'student_id' might become 'studentID' or 'user_identifier'
    """
    pass

class AttendanceV2Create(AttendanceV2Base):
    """Placeholder for v2 create schema"""
    pass

class AttendanceV2Response(AttendanceV2Base):
    """Placeholder for v2 response schema"""
    pass