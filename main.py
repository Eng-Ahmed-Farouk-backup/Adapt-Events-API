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

def verify_api_key(api_key: str):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE key = ?", (api_key,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise fastapi.HTTPException(status_code=401, detail="Invalid or inactive API key")
    
    key_id, daily_limit, requests_today, last_reset_date, key_name = row
    
    # Check if we need to reset the daily counter (new day)
    today = datetime.now().date()
    last_reset = datetime.strptime(last_reset_date, '%Y-%m-%d').date()
    
    if today > last_reset:
        # Reset counter for new day
        cursor.execute('''
            UPDATE api_keys 
            SET requests_today = 0, last_reset_date = ? 
            WHERE id = ?
        ''', (today, key_id))
        requests_today = 0
    
    # Check if key has exceeded daily limit
    if requests_today >= daily_limit:
        conn.close()
        raise fastapi.HTTPException(
            status_code=429,  # Too Many Requests
            detail=f"Daily API limit of {daily_limit} requests exceeded. Please try again tomorrow."
        )
    
    # Increment the request counter
    cursor.execute('''
        UPDATE api_keys 
        SET requests_today = requests_today + 1,
            last_used = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (key_id,))
    
    conn.commit()
    conn.close()
    
    return True , key_id, key_name

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

class add_event_model(pydantic.BaseModel):
    name: str
    description: str
    tags: list
    date: str
    ticket_price: int
    city: str
    country: str

class add_api_key_model(pydantic.BaseModel):
    daily_limit: int

@app.post("/add_event")
async def add_event(model: add_event_model, api_key: str):
    if not verify_api_key(api_key):
        return {"error": "Invalid API key"}
    
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO events (name, description, tags, date, ticket_price, city, country)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (model.name, model.description, ','.join(model.tags), model.date, model.ticket_price, model.city, model.country))
        conn.commit()
        return {"message": "Event added successfully"}
    except Exception as e:
        conn.rollback()
        print(f"Error adding event: {e}")
        return {"error": f"Error adding event: {e}"}
    finally:
        conn.close()

@app.delete("/delete_event")
async def delete_event(id: int, api_key: str):
    if not verify_api_key(api_key):
        return {"error": "Invalid API key"}
    
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM events WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Event deleted successfully"}
    except Exception as e:
        conn.rollback()
        print(f"Error deleting event: {e}")
        return {"error": f"Error deleting event: {e}"}
    finally:
        conn.close()
    

@app.post("/generate_api_key")
async def generate_api_key(model: add_api_key_model):
    new_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
                        INSERT INTO api_keys (key, daily_limit, requests_today, last_request_date)
                        VALUES (?, ?, 0, ?)''',(new_key, model.daily_limit, datetime.datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        return {"api_key": new_key, "daily_limit": model.daily_limit}
    except Exception as e:
        conn.rollback()
        print(f"Error generating API key: {e}")
        return {"error": f"Error generating API key: {e}"}



