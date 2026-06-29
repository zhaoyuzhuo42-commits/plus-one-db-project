from fastapi import APIRouter, HTTPException
from db.connection import get_connection
app = APIRouter(prefix="/api", tags=["events"])


@router.get("/events")
def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            events.id, 
            events.title, 
            events.starts_at, 
            events.ends_at, 
            events.address AS location 
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
    
    cursor.close()
    conn.close()
    
    return {"events": events_data}