from django import forms
from django.utils.translation import ugettext_lazy as _
from sodalabs.accounts.models import Musiphile
from django.contrib.auth import authenticate

class UserCreationForm(forms.ModelForm):
    '''
    A form that creates a user, with no priviledges, from the given email and password.
    '''
    musiphile_email = forms.EmailField(label=_("Email"), max_length=30)
    username = forms.CharField(label=_("Username"), max_length=30)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = Musiphile
        fields = ("musiphile_email", "password1","password2","username",)

    def clean_musiphile_email(self):
        musiphile_email = self.cleaned_data['musiphile_email']
        try:
            Musiphile.objects.get(musiphile_email=musiphile_email)
        except Musiphile.DoesNotExist:
            return musiphile_email
        raise forms.ValidationError(_("A user with that email already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data.get("password2", "")
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_username(self):
        return self.cleaned_data.get("username", "")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    '''
    Overrides built-in django auth form so that user can login with email address instead of username
    '''
    musiphile_email = forms.EmailField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)


    def clean(self):
        musiphile_email = self.cleaned_data.get('musiphile_email')
        password = self.cleaned_data.get('password')

        if musiphile_email and password:
            self.user_cache = authenticate(musiphile_email=musiphile_email,password=password)
            
            if self.user_cache is None:
                raise forms.ValidationError(_("Your email and password did not match.  Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled.  Cookies are required for logging in."))
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache



