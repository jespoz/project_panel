from django.db import models
from django_comments.models import CommentAbstractModel
from django.contrib.auth.models import User


class CommentWithArchive(CommentAbstractModel):
    archive = models.FileField(upload_to="adjuntos/", blank=True, null=True)


class Comentario(models.Model):
    creado_por = models.ForeignKey(User)
