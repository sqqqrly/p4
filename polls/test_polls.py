from django.test import TestCase
from django.utils import timezone
import datetime
from polls.models import Poll

class Test_PollMethods(TestCase):
    def testWasPublishedRecentlyWithFuturePoll(self):
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

