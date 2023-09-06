from django.db import models
from conflicts.models import Conflicts # Этой модели пока нет, так что проверить не могу
from user.models import User
from uuid import uuid4


class Conferences(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    conflict_id = models.ForeignKey(Conflicts, on_delete=models.CASCADE) # Я сделал ForeignKey, хотя в миро указан BigInt
    user_id = models.ManyToManyField(User)
    start_at = models.DateTimeField(auto_now=True, editable=False) # Тут дата автоматически ставится при создании и больше не изменяется, правильно?
    file_path = models.FilePathField(upload_to='conflicts_doc/', blank=True, null=True)

