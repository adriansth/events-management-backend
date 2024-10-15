from pydantic import BaseModel
from typing import List

# joiner data model
class Joiner(BaseModel):
     user_id: str
     status: str # confirmed, pending, cancelled

# event data model
class Event(BaseModel):
      title: str
      organizer: str
      date_time: str
      duration: str
      location: str
      joiners: List[str] = []

      def to_dict(self):
         return {
            "title": self.title,
            "organizer": self.organizer,
            "date_time": self.date_time,
            "duration": self.duration,
            "location": self.location, 
            "joiners": [joiner.dict() for joiner in self.joiners]
         }