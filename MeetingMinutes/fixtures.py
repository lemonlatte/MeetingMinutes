from pymongo import Connection
from django.utils import timezone

meetingDB = Connection("localhost:27017", tz_aware=True)["MeetingMinutes"]["meetings"]


def create_meeting():

    meetingDB.remove()

    for x in range(10):
        meeting = {
                   "create_time": timezone.now(),
                   "meeting_name": "Test",
                   "attendees": ["Jim", "Willy"],
                   "purpose": "This is purpose",
                   "attachments": [],
                   "minutes": [
                               {"topic": "Topic 1",
                                "discussion": "Blah, Blah",
                                "consensus": "We decide to ..."
                                }
                               ]
                   }
        meetingDB.save(meeting)
