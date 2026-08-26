from fastapi import APIRouter, HTTPException
from db.connection import get_connection


router = APIRouter(prefix="/api", tags=["events"])
@router.get("/events")
def get_all_events():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    events.id, 
                    events.title, 
                    events.starts_at, 
                    events.ends_at, 
                    CONCAT (v.name, ',', v.address) AS location 
                FROM events 
                JOIN venues v ON events.venue_id = v.id
                ORDER BY events.starts_at ASC;
            """)
    
    rows = cursor.fetchall()

    events_data = [
        {
            "id": r[0],
            "title": r[1],
            "starts_at": r[2],
            "ends_at": r[3],
            "location": r[4]
        } 
        for r in rows
    ]
    
    return {"events": events_data}