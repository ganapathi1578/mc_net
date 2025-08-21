from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.core.paginator import Paginator
from django.contrib import messages

def event_list(request):
    """Landing page: list events latest -> oldest, paginated."""
    qs = Event.objects.filter(is_published=True).select_related("author").all()
    paginator = Paginator(qs, 6)  # 6 per page
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    return render(request, "events/list.html", {"page": page})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "events/detail.html", {"event": event})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            return redirect("events:detail", pk=event.pk)
    else:
        form = EventForm()
    return render(request, "events/create.html", {"form": form})



@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # permission check: only author or staff can edit
    if not (request.user == event.author or request.user.is_staff):
        messages.error(request, "You don't have permission to edit this event.")
        return redirect("events:detail", pk=event.pk)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect("events:detail", pk=event.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = EventForm(instance=event)

    return render(request, "events/edit.html", {"form": form, "event": event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # only author or staff can delete
    if not (request.user == event.author or request.user.is_staff):
        messages.error(request, "You don't have permission to delete this event.")
        return redirect("events:detail", pk=event.pk)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted.")
        return redirect("events:list")

    return render(request, "events/confirm_delete.html", {"event": event})