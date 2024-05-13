from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Event
from .forms import EventForm

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        user=request.user
        if form.is_valid():
            event = form.save(commit=False)
            event.user= request.user
            event.save()
            if user.is_admin:
                  return redirect('events')
            elif user.is_association:
                 return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)  
    return render(request, 'events/event_list.html', {'events': events})

def events(request):
    events = Event.objects.all() # Retrieve all events from the database
    return render(request, 'events/events.html', {'events': events})

def donor_event_list(request):
    donor = request.user
    events_attended = donor.attended_events.all()
    return render(request, 'events/donor_event_list.html', {'events_attended': events_attended})

def eventIndex (request):
    events = Event.objects.all()
    return render(request, 'events/eventIndex.html', {'events': events})

def participate_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.user.is_authenticated and request.user.is_donor:
        if request.user not in event.attendees.all():
            # Add the current user (donor) to the event's attendees
            event.attendees.add(request.user)
            event.save()

    return redirect('event_detail', event_id=event_id)

def EventDetail(request, pk):
    events = get_object_or_404(Event, pk=pk)
    return render(request, 'publications/detail.html', {'events': events})
 
