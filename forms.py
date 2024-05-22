from .models import UserResponse
from django import forms


class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['first_ques', 'second_ques', 'third_ques', 'fourth_ques', 'fifth_ques']
        widgets = {
            'first_ques': forms.Select(attrs={'class': 'form-control'}),
            'second_ques': forms.Select(attrs={'class': 'form-control'}),
            'third_ques': forms.Select(attrs={'class': 'form-control'}),
            'fourth_ques': forms.Select(attrs={'class': 'form-control'}),
            'fifth_ques': forms.Select(attrs={'class': 'form-control'}),
        }