from django import forms
from UKCB.models import Review
from django.contrib.auth.models import User
from UKCB.models import UserProfile
from django.forms.widgets import RadioSelect
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator


class ReviewForm(forms.ModelForm):

    

   

    Rating = forms.IntegerField( label="Rating", max_value = 5, min_value =0)
    
    Price = forms.IntegerField(label="Price", max_value = 5, min_value =0)
    Text = forms.CharField(label="Review", max_length=100, widget=forms.Textarea(attrs={'name':'body', 'rows':'3', 'cols':'5'}))
    

    class Meta:

    
        # Provide an association between the ModelForm and a model
        model = Review

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('City','WrittenBy')
        # or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')


    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # If url is not empty and doesn't start with 'http://',
        # then prepend 'http://'.
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password',)

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1','password2',)

        
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] ='form-control'
        self.fields['password1'].widget.attrs['class'] ='form-control'
        self.fields['password2'].widget.attrs['class'] ='form-control'


























    
