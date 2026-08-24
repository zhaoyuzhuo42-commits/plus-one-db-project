import json
from connection import get_connection

def seed():
    conn = get_connection()
    cur = conn.cursor()

    def delete_table():
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TABLE IF EXISTS venues CASCADE;")
        cur.execute("DROP TABLE IF EXISTS events CASCADE;")
        cur.execute("DROP TABLE IF EXISTS rsvps CASCADE;")

    def create_table():
        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)

        cur.execute("""
            CREATE TABLE venues (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address VARCHAR(255),
                capacity INT NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE events (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                starts_at TIMESTAMPTZ NOT NULL,
                ends_at TIMESTAMPZ NOT NULL,
                organiser_id INTEGER REFERENCES users(id),
                venue_id INTEGER REFERENCES venues(id)
                creat_at TIMESTAMPZ WITH TIME ZONE DEFAULT NOW()
            );
        """)
        cur.execute("""
            CREATE TABLE rsvps (
                id SEREAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                event_id INTEGER REFERENCES events(id),
                creat_at TIMESTAMPZ WITH TIME ZONE DEFAULT NOW()
            );
        """)

    def insert_data():
        with open('db/data/users.json', 'r') as f:
            users_data = json.load(f)
        for user in users_data:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                        (user['name'], user['email'], user['password']))
            
        with open('db/data/venues.json', 'r') as f:
            venues_data = json.load(f)
        for venue in venues_data:
            cur.execute("INSERT INTO venues (name, address, capacity) VALUES (%s, %s)", 
                        (venue['name'], venue['address'], venue['capacity']))
            
        with open('db/data/events.json', 'r') as f:
            events_data = json.load(f)
        for event in events_data:
            cur.execute("INSERT INTO events (title, description, starts_st, ends_at, organiser_id, venue_id) VALUES (%s, %s, %s, %s, %s)", 
                        (event['title'], event['description'], event['starts_at'], event['ends_at'], event['organiser_id'], event['venue_id']))
            
        with open("db/data/rsvps.json", "r") as f:
            rsvps_data = json.load(f)
        for rsvp in rsvps_data:
            cur.execute("INSERT INTO rsvp (attendee_id, event_id) VALUES (%s, %s)",
                        (rsvp['attendee_id'], rsvp['event_id']))
            
    print("seed run")
    delete_table()
    create_table()
    insert_data()
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    seed()
