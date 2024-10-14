from models.user import User
from firebase_admin import firestore
from fastapi import HTTPException

db = firestore.client()

# create user
def create_user(user: User):
   user_ref = db.collection("users").document(user.uid)
   if user_ref.get().exists:
      raise HTTPException(status_code=400, detail="User with this uid already exists")
   user_ref.set(user.to_dict())
   return { "message": "User created successfully" }

# get user by uid
def get_user_by_uid(uid: str):
   users_ref = db.collection("users")
   query = users_ref.where("uid", "==", uid).limit(1)
   results = query.stream()
   user_data = None
   for user in results:
      user_data = user.to_dict()
      break
   if not user_data:
      raise HTTPException(status_code=404, detail="User not found")
   return user_data

# update user by uid
def update_user_by_uid(uid: str, user_update: dict):
   users_ref = db.collection("users")
   query = users_ref.where("uid", "==", uid).limit(1)
   results = query.stream()
   user_ref = None
   for user in results:
      user_ref = user.reference
      break
   if not user_ref:
      raise HTTPException(status_code=404, detail="User not found")
   user_ref.update(user_update)
   return { "message": "User updated successfully" }

# delete user by uid
def delete_user_by_uid(uid: str):
   users_ref = db.collection("users")
   query = users_ref.where("uid", "==", uid).limit(1)
   results = query.stream()
   user_ref = None
   for user in results:
      user_ref = user.reference
      break
   if not user_ref:
      raise HTTPException(status_code=404, detail="User not found")
   return { "message": "User deleted successfully" }