from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import django.contrib.auth

from events.models import Event, Post, Vote

import datetime
import pytz

import twitter

consumer_key = "C6N8KWKBCTv4wJseyYY0i42CN"
consumer_secret = "dYodyKDuaVoqWsc6g4DoRT4oufgR0noxC1I5TJZs8KUA87oqYh"
access_token = "25333458-MoYEifjzxjaxcp5e935W3qwPMCKJbgf6PbaMxKZC1"
access_token_secret = "Ypy5HSk35vuncJo6KMXEyEqpBNfKNasfZ8qV6pavXHCKu"

def index(request):
	context = {}
	t = datetime.datetime.now(pytz.utc)
	context["live_events"] = Event.objects.filter(start_date__lte=t, end_date__gte=t)
	context["recent_events"] = Event.objects.filter(end_date__lt=t)
	if len(context["recent_events"]) > 5:
		context["recent_events"] = context["recent_events"][:5]
	context["upcoming_events"] = Event.objects.filter(start_date__gt=t)
	if len(context["upcoming_events"]) > 5:
		context["upcoming_events"] = context["upcoming_events"][:5]
	return render(request, 'events/index.html', context)


def logout(request):
	django.contrib.auth.logout(request)
	return HttpResponseRedirect("/")


def event(request, hashtag):
	context = {}

	event = Event.objects.filter(hashtag=hashtag)
	if len(event) > 0:
		event = event[0]
	else: 
		return HttpResponse("hashtag event not found")

	context["posts"] = Post.objects.filter(event=event).order_by("-time_posted")[:10]
	if request.user.is_authenticated():
		for post in context["posts"]:
			post.updown = post.getUpDown(request.user)
	context["event"] = event

	#load events
	t = datetime.datetime.now(pytz.utc)
	context["live_events"] = Event.objects.filter(start_date__lte=t, end_date__gte=t)
	context["recent_events"] = Event.objects.filter(end_date__lt=t)
	if len(context["recent_events"]) > 5:
		context["recent_events"] = context["recent_events"][:5]
	context["upcoming_events"] = Event.objects.filter(start_date__gt=t)
	if len(context["upcoming_events"]) > 5:
		context["upcoming_events"] = context["upcoming_events"][:5]


	return render(request, 'events/event.html', context)

def vote(request):
	if request.method == "GET" and request.user.is_authenticated:
		updown = request.GET["updown"]
		post = Post.objects.get(pk=request.GET["id"])
		vote = ""
		if len(Vote.objects.filter(post=post, user=request.user)) == 0:
			vote = Vote(user=request.user, post=post, updown=-1)
		else:
			vote = Vote.objects.filter(post=post, user=request.user)[0]

		response = 0

		if vote.updown == -1:
			if updown == "up":
				post.score = post.score + 1
				vote.updown = 1
				response = 1
			if updown == "down":
				post.score = post.score - 1
				vote.updown = 0
				response = -1
		elif vote.updown == 1:
			if updown == "down":
				post.score = post.score - 2
				vote.updown = 0
				response = -2
			if updown == "up":
				post.score = post.score - 1
				vote.updown = -1
				response = -1
		elif vote.updown == 0:
			if updown == "up":
				post.score = post.score + 2
				vote.updown = 1
				response = 2
			if updown == "down":
				post.score = post.score + 1
				vote.updown = -1
				response = 1

		if response == 0:
			return HttpResponse(str(response) + "," + str(vote.updown))

		try:
			post.save()
			vote.save()
			return HttpResponse(str(response) + "," + str(vote.updown))
		except:
			return HttpResponse("failed")
	else:
		return HttpResponse("failed")
