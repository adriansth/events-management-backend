from models.event import Event
from fastapi import HTTPException

# create event
def create_event(db, event: Event):
   event_ref = db.collection("events").document()
   event_ref.set(event.to_dict())
   return { "message": "Event created successfully" }

# get events by organizer
def get_events_by_organizer(db, organizer: str):
   events_ref = db.collection("events")
   query = events_ref.where("organizer", "==", organizer)
   results = query.stream()
   events_data = []
   for event in results:
      event_data = event.to_dict()
      event_data["id"] = event.id
      events_data.append(event_data)
   if not events_data:
      raise HTTPException(status_code=404, detail="Events not found")
   return events_data

# get event by id
def get_event_by_id(db, event_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_data = event.to_dict()
   event_data["id"] = event_id
   return event_data

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

# add joiner to event
def add_joiner_to_event(db, event_id: str, user_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get() 
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_data = event.to_dict()
   if any(joiner["user_id"] == user_id for joiner in event_data["joiners"]):
      raise HTTPException(status_code=400, detail="User is already a joiner") 
   new_joiner = {"user_id": user_id, "status": "pending"}
   event_data["joiners"].append(new_joiner)
   event_ref.update({"joiners": event_data["joiners"]})
   return {"message": "Joiner added successfully"}

# update joiner to accepted
def update_joiner_to_accepted(db, event_id: str, user_id: str): 
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_data = event.to_dict()
   joiner_found = False
   for joiner in event_data["joiners"]:
      if joiner["user_id"] == user_id:
         joiner["status"] = "accepted"
         joiner_found = True
         break
   if not joiner_found:
      raise HTTPException(status_code=404, detail="Joiner not found in the event")
   event_ref.update({ "joiners": event_data["joiners"] })
   return { "message": "Joiner status updated to accepted" }

# update joiner to cancelled
def update_joiner_to_cancelled(db, event_id: str, user_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_data = event.to_dict()
   joiner_found = False
   for joiner in event_data["joiners"]:
      if joiner["user_id"] == user_id:
         joiner["status"] = "cancelled"
         joiner_found = True
         break
   if not joiner_found:
      raise HTTPException(status_code=404, detail="Joiner not found in the event")
   event_ref.update({ "joiners": event_data["joiners"] })
   return { "message": "Joiner status updated to cancelled" }

# get events where the user is a joiner
def get_events_by_joiner(db, user_id: str):
   events_ref = db.collection("events")
   results = events_ref.stream()
   invited_events = []
   for event in results:
      event_data = event.to_dict()
      for joiner in event_data["joiners"]:
         if joiner["user_id"] == user_id:
            event_data["id"] = event.id
            invited_events.append(event_data)
            break
   if not invited_events:
      raise HTTPException(status_code=404, detail="No events found for this user")
   return invited_events

# get joiner by user id
def get_joiner_by_user_id(db, event_id: str, user_id: str):
   event_ref = db.collection("events").document(event_id)
   event = event_ref.get()
   if not event.exists:
      raise HTTPException(status_code=404, detail="Event not found")
   event_data = event.to_dict()
   for joiner in event_data["joiners"]:
      if joiner["user_id"] == user_id:
         return {"user_id": joiner["user_id"], "status": joiner["status"]}
   raise HTTPException(status_code=404, detail="Joiner not found")
