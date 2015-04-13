import twitter
import time
import sys
import datetime
import pytz
import urllib
import json
from dateutil.parser import parse
from instagram.client import InstagramAPI

from django.core.management.base import BaseCommand, CommandError

from events.models import Event, Post

consumer_key = "C6N8KWKBCTv4wJseyYY0i42CN"
consumer_secret = "dYodyKDuaVoqWsc6g4DoRT4oufgR0noxC1I5TJZs8KUA87oqYh"
access_token = "25333458-MoYEifjzxjaxcp5e935W3qwPMCKJbgf6PbaMxKZC1"
access_token_secret = "Ypy5HSk35vuncJo6KMXEyEqpBNfKNasfZ8qV6pavXHCKu"

instagram_token = "180513181.ec4b97d.f20c4efd9eb844e6a56fae2af8972626"

class Command(BaseCommand):
	help = 'Gets hour data once an hour'

	def add_arguments(self, parser):
		bob = 5

	def handle(self, *args, **options):
		api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

		#TWITTER
		statuses = api.GetSearch(term="#whereyatyo", count=50, result_type="recent")
		current_time = datetime.datetime.now(pytz.utc)
		#go through all events
		for event in Event.objects.filter(start_date__lte=current_time, end_date__gte=current_time):
			for stat in statuses:
				if len(Post.objects.filter(source_id=stat.id, source=1)) == 0:
					if "#"+event.hashtag in stat.text:
						t = parse(stat.created_at)
						if t > event.start_date and t < event.end_date:
								post = Post(source_id=stat.id,
											source=1,
											time_posted=t,
											event=event,
											score=0,
											html=api.GetStatusOembed(id=stat.id)["html"].encode('ascii', 'ignore').decode('ascii'))
								try:
									post.save()
								except:
									print "Failed: " + str(stat.id)
		#INSTAGRAM
		api = InstagramAPI(access_token=instagram_token)
		grams = api.tag_recent_media(count=50, tag_name="whereyatyo")
		grams = grams[0]
		for event in Event.objects.filter(start_date__lte=current_time, end_date__gte=current_time):
			for gram in grams:
				if len(Post.objects.filter(source_id=gram.id, source=2)) == 0:
					for tag in gram.tags:
						if tag.name == event.hashtag:
							t = pytz.utc.localize(gram.created_time)
							if t > event.start_date and t < event.end_date:
								url = "http://api.instagram.com/oembed?url=" + gram.link
								response = urllib.urlopen(url);
								data = json.loads(response.read())
								html = data["html"]
								post = Post(source_id=gram.id,
											source=2,
											time_posted=t,
											event=event,
											score=0,
											html=html)
								try:
									post.save()
								except:
									import pdb; pdb.set_trace()
									print "Failed: " + str(stat.id)
							break










