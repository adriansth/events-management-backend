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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create user route
@app.post("/user/")
def create_user(user: User = Depends(verify_token)):
   return create_user(db, user)

# get user by uid route
@app.get("/user/{uid}")
def get_user_by_uid(uid: str = Depends(verify_token)):
   return get_user_by_uid(db, uid)

# update user by uid route
@app.put("/users/{uid}")
def update_user_by_uid(uid: str, user_update: dict = Depends(verify_token)):
   return update_user_by_uid(db, uid, user_update)

# delete user by uid
@app.delete("/users/{uid}")
def delete_user_by_uid(uid: str = Depends(verify_token)):
   return delete_user_by_uid(db, uid)

