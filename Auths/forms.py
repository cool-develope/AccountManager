from django import forms
from .models import MyUser 
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput(render_value=True))

class RegistForm(forms.ModelForm):
	password = forms.CharField(label=_('Password '), widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat Pass ', widget=forms.PasswordInput)
	
	class Meta:
		model = MyUser
		fields = ('username', 'is_virtual')
		labels = {
			'username': _('Username '),
			'is_virtual': _('Mirror User ')
		}

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']