from fastapi import FastAPI, Depends
import firebase_admin
from firebase_admin import credentials, firestore
from handlers.user_handler import *
from handlers.event_handler import *
from models.user import User
from models.event import Event
from middleware.auth import verify_token
from fastapi.middleware.cors import CORSMiddleware

# initialize firestore
cred = credentials.Certificate("events-5c576-firebase-adminsdk-sixqt-7813fc726e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create user
@app.post("/user/")
def create_user_route(user: User):
    return create_user(db, user)

# get user by uid
@app.get("/user/{uid}")
def get_user_by_uid_route(uid: str):
    return get_user_by_uid(db, uid)

# update user by uid
@app.put("/user/{uid}")
def update_user_by_uid_route(uid: str, user_update: dict):
    return update_user_by_uid(db, uid, user_update)

# delete user by uid
@app.delete("/user/{uid}")
def delete_user_by_uid_route(uid: str):
    return delete_user_by_uid(db, uid)

# create event
@app.post("/event/")
def create_event_route(event: Event):
   return create_event(db, event)

# get events by organizer
@app.get("/event/owned/{organizer}/")
def get_events_by_organizer_route(organizer: str):
    return get_events_by_organizer(db, organizer)

# get event by id
@app.get("/event/{event_id}")
def get_event_by_id_route(event_id: str):
    return get_event_by_id(db, event_id)

# update event by id
@app.put("/event/{event_id}")
def update_event_by_id_route(event_id: str, event_update: dict):
    return update_event_by_id(db, event_id, event_update)

# delete event by id
@app.delete("/event/{id}")
def delete_event_by_id_route(event_id: str):
    return delete_event_by_id(db, event_id)

# add joiner route
@app.post("/event/{event_id}/join/")
def add_joiner_route(event_id: str, user_id: str):
    return add_joiner_to_event(db, event_id, user_id)

# update joiner to accepted
@app.put("/event/{event_id}/joiner/{user_id}/accept/")
def accept_joiner_route(event_id: str, user_id: str):
    return update_joiner_to_accepted(db, event_id, user_id)

# update joiner to cancelled
@app.put("/event/{event_id}/joiner/{user_id}/cancel/")
def cancel_joiner_route(event_id: str, user_id: str):
    return update_joiner_to_cancelled(db, event_id, user_id)

# get events by joiner
@app.get("/event/invited/{user_id}/")
def get_invited_events_route(user_id: str):
    return get_events_by_joiner(db, user_id)