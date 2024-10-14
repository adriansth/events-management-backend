# event data model
class Event:
   def __init__(self, title, organizer, date_time, duration, location):
      self.title = title
      self.organizer = organizer
      self.date_time = date_time
      self.duration = duration
      self.location = location
      self.joiners = []

   def to_dict(self):
      return {
         "title": self.title,
         "organizer": self.organizer,
         "date_time": self.date_time,
         "duration": self.duration,
         "location": self.location, 
         "joiners": self.joiners,        
      }