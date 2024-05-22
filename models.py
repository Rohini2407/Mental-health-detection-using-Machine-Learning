from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


answers = {
    ("Yes", 'Yes'), ('No', 'No')
}


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stage_number = models.IntegerField()
    first_ques = models.CharField(choices=answers, max_length=10)
    second_ques = models.CharField(choices=answers, max_length=10)
    third_ques = models.CharField(choices=answers, max_length=10)
    fourth_ques = models.CharField(choices=answers, max_length=10)
    fifth_ques = models.CharField(choices=answers, max_length=10)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '- [{}]'.format(str(self.date_time))

    class Meta:
        get_latest_by = 'date_time'

class DoctorInfo(models.Model):
    doc_name = models.CharField(max_length=500)
    specializatin = models.CharField(max_length=500)
    experience = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    fees = models.CharField(max_length=500)

    def __str__(self):
        return self.doc_name