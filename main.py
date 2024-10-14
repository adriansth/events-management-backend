from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore

# initialize firestore
cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
firebase_admin.initialize_app(cred) 
db = firestore.client()

app = FastAPI()

@app.get("/")
def read_root():
   return { "message": "Welcome to the Realtime Events Management App" }

# event data model
class Event:
   def __init__(self, title, organizer, date_time, duration, location):
      self.title = title
      self.organizer = organizer
      self.date_time = date_time
      self.duration = duration
      self.location = location
      self.joiners = []

   def to_dict(self):
      return {
         "title": self.title,
         "organizer": self.organizer,
         "date_time": self.date_time,
         "duration": self.duration,
         "location": self.location, 
         "joiners": self.joiners,        
      }

# create an event
@app.post("/event/")
def create_event(event: Event):
   event_ref = db.collection("events").document()
   event_ref.set(event.to_dict())
   return { "id": event_ref.id, "message": "Event created successfully" }

# join an event
@app.post("/event/{event_id}/join/")
def join_event(event_id: str, user_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_data = event.to_dict()
   if user_id not in event_data["joiners"]:
      event_data["joiners"].append(user_id)
      event_ref.update({ "joiners": event_data["joiners"] })
   return { "message": f"{user_id} joined the event" } 

# cancel an event
@app.delete("/event/{event_id}/cancel/")
def cancel_event(event_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_ref.delete()
   return { "message": "Event cancelled successfully" }
