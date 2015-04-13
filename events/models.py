from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
	title = models.CharField(max_length=100)
	hashtag = models.CharField(max_length=50)
	start_date = models.DateTimeField(blank=True,null=True)
	end_date = models.DateTimeField(blank=True,null=True)

class Post(models.Model):
	source = models.IntegerField() # 1 - twitter, 2 - instagram
	source_id = models.CharField(max_length=100)
	html = models.CharField(max_length=5000)
	time_posted = models.DateTimeField(blank=True,null=True)
	score = models.IntegerField()
	event = models.ForeignKey('Event')
	updown = models.IntegerField(blank=True, null=True)

	def getUpDown(self, user):
		if len(Vote.objects.filter(post=self, user=user)) == 0:
			return -1
		else:
			return Vote.objects.filter(post=self, user=user)[0].updown

class Vote(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey('Post')
	updown = models.IntegerField()# 1 - up, 0 - down