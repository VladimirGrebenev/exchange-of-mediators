from django.db import models
# from conflicts.models import Conflicts # For future
from conflict.models import Conflict
from user.models import User
from uuid import uuid4


class Conferences(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    conflict_id = models.ForeignKey(Conflict, on_delete=models.CASCADE)
    initiator = models.ForeignKey(User, related_name='initiator', on_delete=models.CASCADE)
    invated_user = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    scheduled_date = models.DateTimeField()
    file_path = models.FilePathField(path='conflicts_doc/', blank=True, null=True)
