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
        "duration": "2:30",
        "location": "Test Location",
        "joiners": []
    }
    event = Event(**event_data)
    event_ref = Mock()
    db.collection().document.return_value = event_ref

    result = create_event(db, event)
    event_ref.set.assert_called_once_with(event.to_dict())
    assert result == {"message": "Event created successfully"}

def test_get_events_by_organizer(mocker):
    db = Mock()
    organizer_id = "1234"
    event_doc = Mock()
    event_doc.to_dict.return_value = {
        "title": "Test Event",
        "organizer": organizer_id,
        "joiners": [],
    }
    event_doc.id = "event123"
    db.collection().where().stream.return_value = [event_doc]
    result = get_events_by_organizer(db, organizer_id)
    assert len(result) == 1
    assert result[0]["id"] == "event123"
    assert result[0]["organizer"] == organizer_id

def test_delete_event_by_id(mocker):
    db = Mock()
    event_id = "event123"

    # Mock Firestore document
    event_ref = Mock()
    event_ref.get.return_value.exists = True
    db.collection().document.return_value = event_ref

    result = delete_event_by_id(db, event_id)
    event_ref.delete.assert_called_once()
    assert result == {"message": "Event deleted successfully"}