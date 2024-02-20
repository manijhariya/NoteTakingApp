import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response

from notes.models import Note, NoteUpdate


@csrf_exempt  # To handle csrf errors
@login_required
def create_note(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Validation: title and content must be provided and must be strings
        if not title or not isinstance(title, str):
            return JsonResponse(
                {"error": "Invalid title"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not content or not isinstance(content, str):
            return JsonResponse(
                {"error": "Invalid content"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validation: title must be less than 200 characters -> Just for fun
        if len(title) > 200:
            return JsonResponse(
                {"error": "Title is too long"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            note = Note.objects.create(title=title, content=content, owner=request.user)
            NoteUpdate.objects.create(note=note, content=content)
            return JsonResponse(
                {"message": "Note created successfully", "note_id": note.id}
            )
        except Exception as e:
            # Error handling: return a 500 status code and the error message
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@login_required
def get_or_update_note(request, note_id):
    if request.method == "GET":
        note = get_object_or_404(Note, id=note_id)

        # Check if the logged-in user is the owner of the note
        if request.user != note.owner:
            return JsonResponse(
                {"error": "You do not have permission to view this note"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return JsonResponse({"title": note.title, "content": note.content})
    elif request.method == "PUT":
        note = get_object_or_404(Note, id=note_id)

        # Check if the logged-in user has access to the note
        if request.user != note.owner and request.user not in note.shared_with.all():
            return JsonResponse(
                {"error": "You do not have permission to edit this note"}, status=403
            )

        request_body = json.loads(request.body)
        new_content = request_body.get("content")

        # Validation: new_content must be provided and must be a string
        if not new_content or not isinstance(new_content, str):
            return JsonResponse({"error": "Invalid content"}, status=400)

        note_update = NoteUpdate.objects.create(note=note, content=new_content)
        Note.objects.update(id=note.id, content=new_content)

        return JsonResponse({"message": "Note updated successfully"})


@csrf_exempt
@login_required
def share_note(request):
    if request.method == "POST":
        note_id = request.POST.get("note_id")
        usernames = request.POST.getlist("usernames")
        note = get_object_or_404(Note, id=note_id)

    # Check if logged user is owner of this note
    if request.user != note.owner:
        return JsonResponse(
            {"error": "You do not permission to share this note"},
            status=status.HTTP_403_FORBIDDEN,
        )

    for username in usernames:
        user = get_object_or_404(User, username=username)
        note.shared_with.add(user)

    return JsonResponse({"message": "Note shared successfully!"})


@login_required
def get_note_history(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Check if the logged-in user has access to the note
    if request.user != note.owner and request.user not in note.shared_with.all():
        return JsonResponse(
            {"error": "You do not have permission to view this note"}, status=403
        )

    updates = note.updates.order_by("-timestamp").values("content", "timestamp")
    return JsonResponse(list(updates), safe=False)
