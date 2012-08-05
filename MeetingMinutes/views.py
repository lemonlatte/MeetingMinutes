import json
from datetime import datetime

import pytz
from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from pymongo.objectid import ObjectId
from pymongo import Connection

meetingDB = Connection("localhost:27017", tz_aware=True)["MeetingMinutes"]["meetings"]
localtimezone = pytz.timezone(settings.TIME_ZONE)


def mongo_parser(data):
        for key, val in data.iteritems():
            if type(val) == ObjectId:
                data[key] = str(val)
            if type(val) == datetime:
                val = val.astimezone(localtimezone)
                data[key] = datetime.strftime(val, "%Y-%m-%d %H:%M")
        return data


def home(request):
    return render(request, "base.html")


def list_meetings(request):

    data = [mongo_parser(meeting) for meeting in meetingDB.find().sort("create_time", -1)]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
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


@login_required
@require_POST
def add_minute(request, _id):

    params = request.POST

    data = {
        "topic": params["topic"],
        "discussion": params["discussion"],
        "consensus": params["consensus"]
    }

    meetingDB.update({"_id": ObjectId(_id)}, {"$push": {"minutes": data}}, safe=True)

    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@require_POST
def del_meeting(request):

    _id = request.POST["_id"]

    meetingDB.remove({"_id": ObjectId(_id)}, safe=True)

    return HttpResponse(0)


@login_required
@require_POST
def del_minute(request, _id):

    index = request.POST["index"]

    meetingDB.update({"_id": ObjectId(_id)}, {"$unset": {"minutes.%s" % index: 1}}, safe=True)
    meetingDB.update({"_id": ObjectId(_id)}, {"$pull": {"minutes": None}}, safe=True)

    return HttpResponse(index)
