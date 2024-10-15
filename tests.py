import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from handlers.event_handler import (
    create_event, get_events_by_organizer, delete_event_by_id,
    add_joiner_to_event, update_joiner_to_accepted, update_joiner_to_cancelled,
    get_joiner_by_user_id
)
from models.event import Event

def test_create_event(mocker):
    db = Mock()
    event_data = {
        "title": "Test Event",
        "organizer": "1234",
        "date_time": "2024-10-25-15:46",
        "duration": "2 hours",
        "location": "Test Location",
        "joiners": []
    }
    event = Event(**event_data)
    event_ref = Mock()
    db.collection().document.return_value = event_ref

    result = create_event(db, event)
    event_ref.set.assert_called_once_with(event.to_dict())
    assert result == {"message": "Event created successfully"}
 