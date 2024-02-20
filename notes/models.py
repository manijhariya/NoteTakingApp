# Notes Models 
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Note(models.Model):
    """
    Note Model class
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name="notes_shared", blank=True)

    def __str__(self) -> str:
        return self.title


class NoteUpdate(models.Model):
    """
    NoteUpdate class
    """
    note = models.ForeignKey(Note, related_name="updates", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
