from fastapi import APIRouter, HTTPException
import bcrypt
import jwt
import os
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
                    CONCAT (v.name, ', ', v.address) AS location 
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

@router.get("/events/{event_id}")
def get_event_id(event_id):
    try:
        event_id = int(event_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail= "id is not a valid integer"
        )
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    events.id,
                    events.title,
                    events.description,
                    events.starts_at,
                    events.ends_at,
                    v.name AS location,
                    v.address,
                    v.capacity,
                    events.created_at
                FROM events
                JOIN venues v ON events.venue_id = v.id
                where events.id = %s;
            """,(event_id,))

            row = cursor.fetchone() 

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail= "Event not found")
            events_data ={
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "starts_at": row[3],
                    "ends_at": row[4],
                    "location": row[5],
                    "address": row[6],
                    "capacity": row[7],
                    "created_at": row[8]
                }
    return {"event": events_data}

@router.post("/auth/login")
def login(credentials: dict):
    email = credentials.get("email")
    password = credentials.get("password")
    if not email or not password:
        raise HTTPException(
            status_code = 400,
            detail = "Email and Password are required."
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT id, email, password
            FROM users
            WHERE email = %s""",
            (email,))
            user = cursor.fetchone()

    if user is None:
        raise HTTPException(
            status_code= 401,
            detail= "invalid credentials"
        )

    if not bcrypt.checkpw(
    password.encode("utf-8"),
    user[2].encode("utf-8")
):
        raise HTTPException(
            status_code= 401,
            detail= "invalid credentials"
        )
    token = jwt.encode(
    {"sub": str(user[0])},
    os.getenv("JWT_SECRET"),
    algorithm="HS256"
)

    return {"token": token}