from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User, Profile


# Create your forms here.

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', required=True)
	password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
	remember_me = forms.BooleanField(label='Remember me', required=False)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError("This user does not exist")
		if not user.check_password(password):
			raise forms.ValidationError("Incorrect password")
		if not user.is_active:
			raise forms.ValidationError("This user is no longer active")
		return super(LoginForm, self).clean(*args, **kwargs)


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewStatusPostForm(forms.Form):
	status = forms.CharField(label='', required=True, help_text='', widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))

class UserProfile(forms.Form):
	first_name = forms.CharField(label='First Name', required=False)
	last_name = forms.CharField(label='Last Name', required=False)
	email = forms.EmailField(label='Email', required=False)
	phone = forms.CharField(label='Phone', required=False)
	bio = forms.CharField(label='Bio', required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))
	profile_pic = forms.ImageField(label='Profile Picture', required=False)

	class Meta:
		model = Profile

