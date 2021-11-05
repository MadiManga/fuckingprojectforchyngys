from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class LoginForm(forms.ModelForm):
    password=forms.CharField()


    class Meta:
        model=User
        fields=['username','password']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Login'
        self.fields['password'].label="Password"


        def clean(self):
            username=self.cleaned_data["username"]
            password=self.cleaned_data['password']
            user=User.objects.filter(username=username).first()
            if not user:
                raise forms.ValidationError(f'User with login {username}')
            if not user.check_password(password):
                raise forms.ValidationError('Wrong password')
            return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    phone=forms.CharField(required=False)
    email=forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = "Password"
        self.fields['confirm_password'].label = 'Confirm password'
        self.fields['phone'].label = "Phone:"
        self.fields['email'].label = 'Email:'

    def clean_email(self):
        email=self.cleaned_data['email']
        domain=email.split('.')[-1]
        if domain in ['net','xyz']:
            raise forms.ValidationError(f'Registration for domen {domain} is impossible')
        if User.objects.filter(email=email).exists():
            raise forms .ValidationError("That's email has registred")
        return email

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Name {username} is busy.try later')
        return username

    def clean(self):
        if 'password' in self.cleaned_data and 'password1' in self.cleaned_data and self.cleaned_data['password'] != \
                self.cleaned_data['password1']:
            raise forms.ValidationError("The password does not match ")
        return self.cleaned_data

    class Meta:
        model=User
        fields=['username','password','confirm_password','phone','email']
