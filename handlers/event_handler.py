from models.event import Event
from fastapi import HTTPException

# create event
def create_event(db, event: Event):
   event_ref = db.collection("events")
   event_ref.set(event.to_dict())
   return { "message": "Event created successfully" }

# get events by organizer
def get_events_by_organizer(db, organizer: str):
   events_ref = db.collection("events")
   query = events_ref.where("organizer", "==", organizer)
   results = query.stream()
   events_data = None
   for event in results:
      events_data = event.to_dict()
      break
   if not events_data:
      raise HTTPException(status_code=404, detail="Events not found")
   return events_data

# get event by id
def get_event_by_id(db, event_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   return event.to_dict()

# update event by id
def update_event_by_id(db, event_id: str, event_update: dict):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_ref.update(event_update)
   return { "message": "Event updated successfully" }

# delete event by id
def delete_event_by_id(db, event_id):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_ref.delete()
   return { "message": "Event deleted successfully" }