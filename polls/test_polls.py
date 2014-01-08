from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime
from polls.models import Poll

class Test_PollMethods(TestCase):
    def testWasPublishedRecentlyWithOldPoll(self):
        oldPoll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(oldPoll.was_published_recently(), False)
    def testWasPublishedRecentlyWithRecentPoll(self):
        recentPoll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=23))
        self.assertEqual(recentPoll.was_published_recently(), True)
    def testWasPublishedRecentlyWithFuturePoll(self):
        futurePoll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(futurePoll.was_published_recently(), False)

def create_poll(question, days):
    """
    Creates a poll with question published days offset to now, negative in past, positive in future.
    """
    return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):
    def testIndexViewWithNoPolls(self):
        response = self.client.get(reverse('p4:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])
    def testIndexViewWithAPastPoll(self):
        create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('p4:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'],
                ['<Poll: Past poll.>'])
    def testIndexViewWithAFuturePoll(self):
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('p4:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])
    def testIndexViewWithFuturePollAndPastPoll(self):
        create_poll(question="Past poll.", days=-30)
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('p4:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'],
                ['<Poll: Past poll.>'])
    def testIndexViewWithTwoPastPolls(self):
        create_poll(question="Past poll 1.", days=-30)
        create_poll(question="Past poll 2.", days=-5)
        response = self.client.get(reverse('p4:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'],
                ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>'])
