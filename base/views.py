from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView, ModelFormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from base.models import Room, Topic, Comment, Profile, Message
from base.forms import UserRegisterForm, CommentForm


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    ).order_by("-comment__created", "-created", "-updated")[0:5]
    topics = Topic.objects.all()
    component_topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    comments = Comment.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "component_topics": component_topics,
        "room_count": room_count,
        "comments": comments,
    }
    return render(request, "base/home.html", context)


class RoomDetailView(ModelFormMixin, DetailView):
    model = Room
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comment_set.all()
        context["participants"] = self.object.participants.all()
        return context

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        Comment.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body"),
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ["topic", "name", "description"]

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


class RoomUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Room
    fields = ["topic", "name", "description"]
    success_message = "Your room was updated successfully."

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(host=self.request.user)
        return qs

    def test_func(self):
        obj = self.get_object()
        return obj.host == self.request.user


class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Your room was deleted sucessfully!")
        return response

    def test_func(self):
        obj = self.get_object()
        return obj.host == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse("room", kwargs={"pk": self.object.room_id})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Your comment was deleted sucessfully!")
        return response

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("home")
    success_message = "Your account was created successfully"

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.user.comment_set.all()
        context["rooms"] = self.object.user.room_set.all()
        context["topics"] = Topic.objects.all()
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ["name", "bio", "avatar"]
    success_message = "Your profile was updated successfully."

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class TopicListView(ListView):
    paginate_by = 5
    model = Topic
    context_object_name = "topics"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get("q") if self.request.GET.get("q") != None else ""
        query = self.request.GET.get("q")
        if query:
            return qs.filter(name__icontains=q)
        return qs


class ActivityListView(ListView):
    model = Comment
    context_object_name = "comments"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    

    def form_valid(self, form, **kwargs):
        form.instance.sender = self.request.user
        form.instance.receiver = User.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user-profile", kwargs={"pk": self.kwargs.get('pk')})


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "inbox"

    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(receiver=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("message-list")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Message deleted sucessfully!")
        return response

    def test_func(self):
        obj = self.get_object()
        return obj.receiver == self.request.user