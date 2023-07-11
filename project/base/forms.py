from django.forms import ModelForm
from .models import  Room, User
from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'created', 'updated', 'participants']


class AccountCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditAccount(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'image']