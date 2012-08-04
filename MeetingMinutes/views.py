import json
from datetime import datetime

from django.shortcuts import render, HttpResponse
from pymongo.objectid import ObjectId
from pymongo import Connection

meetingDB = Connection("localhost:27017", tz_aware=True)["MeetingMinutes"]["meetings"]


def home(request):
    return render(request, "base.html")


def list_meetings(request):

    def mongo_parser(data):
        for key, val in data.iteritems():
            if type(val) == ObjectId:
                data[key] = str(val)
            if type(val) == datetime:
                data[key] = datetime.strftime(val, "%Y-%m-%d %H:%M")
        return data

    data = [mongo_parser(meeting) for meeting in meetingDB.find()]

    return HttpResponse(json.dumps(data), content_type="application/json")

