from django import forms
from .models import Lesson
from django.contrib.auth.models import User, Group


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserGroupForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label=None
    )

    class Meta:
        model = User
        fields = ['group']


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        empty_label=None,
        label='Role'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'group']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
        return user
