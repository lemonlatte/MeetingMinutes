import json
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from pymongo.objectid import ObjectId
from pymongo import Connection

meetingDB = Connection("localhost:27017", tz_aware=True)["MeetingMinutes"]["meetings"]


def mongo_parser(data):
        for key, val in data.iteritems():
            if type(val) == ObjectId:
                data[key] = str(val)
            if type(val) == datetime:
                data[key] = datetime.strftime(val, "%Y-%m-%d %H:%M")
        return data


def home(request):
    return render(request, "base.html")


def list_meetings(request):

    data = [mongo_parser(meeting) for meeting in meetingDB.find()]
    return HttpResponse(json.dumps(data), content_type="application/json")


@require_POST
def add_meeting(request):

    params = request.POST

    meeting = {
               "create_time": timezone.now(),
               "meeting_name": params["meeting_name"],
               "attendees": params["attendees"].split(","),
               "purpose": params["purpose"],
               "attachments": [],
               "minutes": []
               }
    meetingDB.insert(meeting, safe=True)

    return HttpResponse(json.dumps(mongo_parser(meeting)))


def del_meeting(request):

    _id = request.POST["_id"]

    meetingDB.remove({"_id": ObjectId(_id)}, safe=True)

    return HttpResponse(0)


def del_minute(request, _id):

    index = request.POST["index"]

    meetingDB.update({"_id": ObjectId(_id)}, {"$unset": {"minutes.%s" % index: 1}}, safe=True)
    meetingDB.update({"_id": ObjectId(_id)}, {"$pull": {"minutes": None}}, safe=True)

    return HttpResponse(index)
