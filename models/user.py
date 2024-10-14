# user data model
class User:
   def __init__(self, uid, email, first_name, last_name): 
      self.uid: uid
      self.email: email
      self.first_name: first_name
      self.last_name: last_name
   
   def to_dict(self):
      return {
         "uid": self.uid,
         "email": self.email,
         "first_name": self.first_name,
         "last_name": self.last_name
      }