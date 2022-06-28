from django.urls import path
from django.conf import settings
from base import views
from base.views import (
    MessageDeleteView,
    RoomCreateView,
    RoomUpdateView,
    RoomDetailView,
    RoomDeleteView,
    UserRegisterView,
    CommentDeleteView,
    ProfileDetailView,
    ProfileUpdateView,
    TopicListView,
    ActivityListView,
    MessageCreateView,
    MessageListView,
    MessageDetailView,
    MessageDeleteView,
)
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path("register", UserRegisterView.as_view(), name="register"),
    path("room/<int:pk>/", RoomDetailView.as_view(), name="room"),
    path("create-room/", RoomCreateView.as_view(), name="create-room"),
    path("update-room/<int:pk>/", RoomUpdateView.as_view(), name="update-room"),
    path("delete-room/<int:pk>/", RoomDeleteView.as_view(), name="delete-room"),
    path("delete-comment/<int:pk>/", CommentDeleteView.as_view(), name="delete-comment"),
    path("user-profile/<int:pk>/", ProfileDetailView.as_view(), name="user-profile"),
    path("update-profile/<int:pk>/", ProfileUpdateView.as_view(), name="update-profile"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("activity/", ActivityListView.as_view(), name="activity-list"),
    path("create-message/<int:pk>", MessageCreateView.as_view(), name="create-message"),
    path("messages/", MessageListView.as_view(), name="message-list"),
    path("message/<int:pk>", MessageDetailView.as_view(), name="message-detail"),
    path("delete-message/<int:pk>", MessageDeleteView.as_view(), name="delete-message"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)