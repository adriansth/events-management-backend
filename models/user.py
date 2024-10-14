# user data model
from pydantic import BaseModel

class User(BaseModel):
    uid: str
    email: str
    first_name: str
    last_name: str

    def to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }