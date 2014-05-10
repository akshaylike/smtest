from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from transac.models import Transaction, TransactionView

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UploadForm(forms.ModelForm):
    name = forms.CharField(max_length=20, help_text="Please enter document name")
    pdfdoc = forms.FileField()

    class Meta:
        model = Transaction
        exclude = ['uploader']

class ShareForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ShareForm, self).__init__(*args, **kwargs)
        self.fields['documents'] = forms.ModelChoiceField(queryset=Transaction.objects.filter(uploader=user))
        self.fields['users'] = forms.ModelChoiceField(queryset=User.objects.filter(~Q(id=user)))

