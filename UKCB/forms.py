from django import forms
from UKCB.models import City, Review
from django.contrib.auth.models import User

class CityForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
						   help_text="Please enter the city name.")
	description = forms.CharField(widget=forms.HiddenInput(), initial="none")
	tag = forms.CharField(widget=forms.HiddenInput(), initial="none")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = City
		fields = ('name',)

class ReviewForm(forms.ModelForm):
	rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	price = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	description = forms.CharField(max_length=512,
								  help_text="Please enter your review here.")

	class Meta:
		model = Review

		exclude = ('city',)

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		if url and not url.startswith('http://'):
			url = f'http://{url}'
			cleaned_data['url'] = url

		return cleaned_data