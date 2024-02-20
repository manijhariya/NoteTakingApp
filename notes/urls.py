from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from notes.views import (create_note, get_note_history, get_or_update_note,
                         share_note)

urlpatterns = [
    path("notes/create/", create_note, name="create_note"),
    path("notes/<int:note_id>/", get_or_update_note, name="get_or_update_note"),
    path("notes/share/", share_note, name="share_note"),
    path(
        "notes/version-history/<int:note_id>/",
        get_note_history,
        name="get_note_history",
    ),
]
