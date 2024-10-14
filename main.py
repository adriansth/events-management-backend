from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore

# initialize firestore
cred = credentials.Certificate("events-5c576-firebase-adminsdk-sixqt-7813fc726e.json")
firebase_admin.initialize_app(cred) 
db = firestore.client()

app = FastAPI()