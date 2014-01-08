from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Choice, Poll

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'
    def get_queryset(self):
        """Return the last n published polls excluding future ones."""
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] # Negative sign means descending order

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redesplay the poll voting from
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'error_message': "You did not select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully handling a POST.
        # Prevents double posts if user hits the back button.
        return HttpResponseRedirect(reverse('p4:results', args=(poll.id,)))


