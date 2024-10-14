from fastapi import FastAPI, Depends
import firebase_admin
from firebase_admin import credentials, firestore
from handlers.user_handler import *
from models.user import User
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

@app.post("/user/")
def create_user_route(user: User):
    return create_user(db, user)

@app.get("/user/{uid}")
def get_user_by_uid_route(uid: str):
    return get_user_by_uid(db, uid)

@app.put("/users/{uid}")
def update_user_by_uid_route(uid: str, user_update: dict):
    return update_user_by_uid(db, uid, user_update)

@app.delete("/users/{uid}")
def delete_user_by_uid_route(uid: str):
    return delete_user_by_uid(db, uid)


