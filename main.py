import fastapi
import sqlite3
from typing import Optional
import datetime
import fastapi.middleware.cors
import pydantic
import random
import string

import fastapi.middleware

app = fastapi.FastAPI()

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def event_to_dict(event):
    return {
        "id": event[0],
        "name": event[1],
        "description": event[2],
        "tags": event[3].split(','),
        "date": event[4],
        "ticket_price": event[5],
        "city": event[6],
        "country": event[7]
    }

@app.get("/")
async def get_events(id: Optional[int] = None, name: Optional[str] = None, country: Optional[str] = None, city: Optional[str] = None, tags: Optional[list] = None, date: Optional[str] = None):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM events WHERE date <= ?", (datetime.datetime.now().strftime("%Y-%m-%d"),))
        events = [event_to_dict(event) for event in cursor.execute("SELECT * FROM events").fetchall()]
    except Exception as e:
        print(f"Error fetching events: {e}")
        conn.close()
        return {"error": f"Error fetching events: {e}"}
    finally:
        conn.close()
    if id:
        events = [event for event in events if event["id"] == id]
    
    if name:
        events = [event for event in events if name.lower() in event["name"].lower()]

    if country:
        events = [event for event in events if country.lower() in event["country"].lower()]

    if city:
        events = [event for event in events if city.lower() in event["city"].lower()]
    
    if tags:
        events = [event for event in events if any(tag.lower() in [t.lower() for t in event["tags"]] for tag in tags)]
    
    if date:
        events = [event for event in events if datetime.datetime.strptime(event["date"], "%Y-%m-%d") > datetime.datetime.strptime(date, "%Y-%m-%d")]
    
    
    return events




