from django import forms
from django.contrib.auth.models import User
from models import UserProfile,Status_update,Friendship,Friendship_Request,Rating,Like,Comment
class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        widget = {'like_status': forms.HiddenInput()}
        widget = {'liked_by': forms.HiddenInput()}

        fields =[]
class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    first_name = forms.CharField(widget= forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','date_of_birth')


class Status_updateForm(forms.ModelForm):
    class Meta:
        model = Status_update
        widgets = {'status':forms.TextInput()}
        fields = []

class Friendship_RequestForm(forms.ModelForm):
    class Meta:
        model = Friendship_Request

        widget = {'request_to_friend':forms.HiddenInput()}
        fields =[]


class Friendship_AcceptForm(forms.ModelForm):
    class Meta:
        model = Friendship_Request
        fields = []
class Rating_Form(forms.ModelForm):
    class Meta:
        model = Rating
        widget = {'movies_id':forms.HiddenInput()}
        widget = {'user':forms.HiddenInput()}
        fields = ['rate']

