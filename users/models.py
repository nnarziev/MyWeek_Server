from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=64)

    @classmethod
    def create(cls, username, password, email):
        res = cls(username, password, email)
        return res
