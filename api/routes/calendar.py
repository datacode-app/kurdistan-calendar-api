from fastapi import APIRouter, Request, Query, HTTPException
from typing import Dict, Union
from datetime import datetime
from pydantic import BaseModel

from api.core.rate_limiter import limiter
from api.utils.date_utils import (
    gregorian_to_kurdish, 
    kurdish_to_gregorian,
    is_valid_kurdish_date
)

router = APIRouter(
    prefix="/api/v1/calendar",
    tags=["calendar"],
)

class GregorianToKurdishRequest(BaseModel):
    date: str

class KurdishToGregorianRequest(BaseModel):
    year: int
    month: Union[str, int]
    day: int

@router.post("/convert/gregorian-to-kurdish")
@limiter.limit("10/minute")
async def convert_gregorian_to_kurdish(
    request: Request, 
    data: GregorianToKurdishRequest
):
    """
    Convert a Gregorian date to Kurdish date.
    Rate limited to 10 requests per minute.
    
    Example request:
    ```json
    {
        "date": "2024-03-21"
    }
    ```
    """
    try:
        # Validate date format
        datetime.fromisoformat(data.date)
        
        # Convert to Kurdish date
        kurdish_date = gregorian_to_kurdish(data.date)
        
        return {
            "status": "success",
            "gregorian_date": data.date,
            "kurdish_date": kurdish_date
        }
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Use YYYY-MM-DD."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting date: {str(e)}"
        )

@router.post("/convert/kurdish-to-gregorian")
@limiter.limit("10/minute")
async def convert_kurdish_to_gregorian(
    request: Request, 
    data: KurdishToGregorianRequest
):
    """
    Convert a Kurdish date to Gregorian date.
    Rate limited to 10 requests per minute.
    
    Example request:
    ```json
    {
        "year": 2724,
        "month": "Xakelew",
        "day": 1
    }
    ```
    
    Month can be either a string (Kurdish month name) or an integer (1-12).
    """
    try:
        # Validate Kurdish date
        if not is_valid_kurdish_date(data.year, data.month, data.day):
            raise HTTPException(
                status_code=400,
                detail="Invalid Kurdish date"
            )
        
        # Convert to Gregorian date
        gregorian_date = kurdish_to_gregorian(data.year, data.month, data.day)
        
        return {
            "status": "success",
            "kurdish_date": {
                "year": data.year,
                "month": data.month,
                "day": data.day
            },
            "gregorian_date": gregorian_date
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting date: {str(e)}"
        )

@router.get("/convert/gregorian-to-kurdish/{date}")
@limiter.limit("10/minute")
async def get_gregorian_to_kurdish(
    request: Request,
    date: str
):
    """
    Convert a Gregorian date to Kurdish date using GET request.
    Rate limited to 10 requests per minute.
    
    Date format: YYYY-MM-DD
    """
    try:
        # Validate date format
        datetime.fromisoformat(date)
        
        # Convert to Kurdish date
        kurdish_date = gregorian_to_kurdish(date)
        
        return {
            "status": "success",
            "gregorian_date": date,
            "kurdish_date": kurdish_date
        }
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Use YYYY-MM-DD."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting date: {str(e)}"
        )

@router.get("/validate/kurdish-date")
@limiter.limit("10/minute")
async def validate_kurdish_date(
    request: Request,
    year: int,
    month: Union[str, int],
    day: int
):
    """
    Validate if a Kurdish date is valid.
    Rate limited to 10 requests per minute.
    
    Query parameters:
    - year: Kurdish year (e.g., 2724)
    - month: Kurdish month name or month number (1-12)
    - day: Day of month
    """
    try:
        is_valid = is_valid_kurdish_date(year, month, day)
        
        return {
            "status": "success",
            "kurdish_date": {
                "year": year,
                "month": month,
                "day": day
            },
            "is_valid": is_valid
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error validating date: {str(e)}"
        ) 