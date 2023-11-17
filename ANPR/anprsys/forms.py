from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('police_id', 'password')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    username = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})) 
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    police_id = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Police Id'}))
    contact = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}))
    sex = forms.CharField(label="", max_length=1, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sex'}))
    nin = forms.CharField(label="", max_length=14, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIN'}))
    dob = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}))
    position = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}))
    district = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}))
    county = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'County'}))
    parish = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parish'}))
    village = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'police_id', 'contact', 'sex', 'nin', 'dob', 'position', 'district', 'county', 'parish', 'village')

        def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields['first_name'].widget.attrs['class'] = 'input'
            self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['placeholder'] = 'Email'

            self.fields['username'].widget.attrs['class'] = 'input'
            self.fields['username'].widget.attrs['placeholder'] = 'Username'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

            self.fields['police_id'].widget.attrs['class'] = 'input'
            self.fields['police_id'].widget.attrs['placeholder'] = 'Police Id'

            self.fields['contact'].widget.attrs['class'] = 'form-control'
            self.fields['contact'].widget.attrs['placeholder'] = 'Contact'

            self.fields['sex'].widget.attrs['class'] = 'form-control'
            self.fields['sex'].widget.attrs['placeholder'] = 'Sex'

            self.fields['dob'].widget.attrs['class'] = 'form-control'
            self.fields['dob'].widget.attrs['placeholder'] = 'Date of Birth'

            self.fields['nin'].widget.attrs['class'] = 'form-control'
            self.fields['nin'].widget.attrs['placeholder'] = 'NIN'

            self.fields['position'].widget.attrs['class'] = 'form-control'
            self.fields['position'].widget.attrs['placeholder'] = 'Position'

            self.fields['district'].widget.attrs['class'] = 'form-control'
            self.fields['district'].widget.attrs['placeholder'] = 'District'

            self.fields['county'].widget.attrs['class'] = 'form-control'
            self.fields['county'].widget.attrs['placeholder'] = 'County'

            self.fields['parish'].widget.attrs['class'] = 'form-control'
            self.fields['parish'].widget.attrs['placeholder'] = 'Parish'

            self.fields['village'].widget.attrs['class'] = 'form-control'
            self.fields['village'].widget.attrs['placeholder'] = 'Village'