from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import TopicForm, EntryForm
from .models import Topic, Entry
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def index(request):
     return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
      topics = Topic.objects.filter(owner=request.user).order_by('date_added')
      context = {'topics': topics}
      return render(request, 'learning_logs/topics.html', context)

# def edit_entry(request, entry_id):
#     entry = Entry.objects.get(id=entry_id)
#     topic = entry.topic
#     form = EntryForm(request.POST, instance=entry)
#     if request.method == 'POST':
#
#         if form.is_valid():
#             form.save()
#             return redirect('topics', topic_id=topic.id)
#             #return HttpResponseRedirect(reverse('topics'))
#     context = {'form': form, 'entry': entry, 'topic': topic}
#     return render(request, 'learning_logs/new_topic.html', context)

def edit_entry(request, entry_id):
     """Edycja istniejącego wpisu."""
     entry = Entry.objects.get(id=entry_id)
     topic = entry.topic
     if request.method != 'POST':
         # Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu.
         form = EntryForm(instance=entry)
     else:
         # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
         form = EntryForm(instance=entry, data=request.POST)
         if form.is_valid():
            form.save()
            return redirect('topic', topic_id=topic.id)
     context = {'entry': entry, 'topic': topic, 'form': form}
     return render(request, 'learning_logs/edit_entry.html', context)



@login_required
def topic(request, topic_id):
     topic = Topic.objects.get(id=topic_id)
     #upewniamy sie ze temat nalezy do biezacego uzytkownika
     if topic.owner != request.user:
        raise Http404
     entries = topic.entry_set.order_by('date_added') #entry_set tworzymy na podstawie foreignkey
     context = {'topic': topic, 'entries': entries}
     return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = TopicForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('topics')
            #return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)



# def new_entry(request, topic_id):
#     """Dodanie nowego wpisu dla określonego tematu."""
#     topic = Topic.objects.get(id=topic_id)
#     if request.method != 'POST':
#         # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
#         form = EntryForm()
#     else:
#         # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
#         form = EntryForm(request.POST)
#         if form.is_valid():
#             new_entry = form.save(commit=False)
#             new_entry.topic = topic
#             new_entry.save()
#             return redirect('topic', topic_id=topic_id)
#     context = {'form': form, 'topic': topic}
#     return render(request, 'learning_logs/new_entry.html', context)

@login_required
def new_entry(request, topic_id):
    """Dodanie nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id=topic_id)
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # a metody save() dołączamy argument commit=False (patrz wiersz ), aby nakazać Django utworzenie nowego obiektu wpisu i jego przechowywanie w zmiennej new_entry, ale jeszcze bez zapisywania w bazie danych
            new_entry.topic = topic # Atrybutowi new_entry egzemplarza topic przypisujemy temat pobrany z bazydanych na początku kodu funkcji (patrz wiersz ), a następnie wywołujemysave() bez argumentów. W ten sposób wpis zostanie zapisany w bazie danychwraz z przypisanym mu prawidłowym tematem.
            new_entry.save()
            return redirect('topic', topic_id=topic_id)
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic.delete()
        return redirect('topics')

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('topics')
