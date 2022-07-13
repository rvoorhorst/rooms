from django.db import models
from django.urls import reverse, reverse_lazy
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse_lazy("room", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.body[0:50]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=200)
    bio = models.TextField(null=True)
    avatar = models.ImageField(
        null=True, default="default.png", upload_to="profile_images"
    )

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"pk": self.pk})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    subject = models.CharField(max_length=64, blank=True, null=True)
    body = models.TextField(blank=True, null=True, verbose_name=("message"))
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subject: {self.subject[0:10]}.. from {self.sender} to {self.receiver} at {self.created}"
