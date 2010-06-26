from sodalabs.accounts.forms import AuthenticationForm,UserCreationForm

def signup_form(request):
    login_form = AuthenticationForm(request)
    register_form = UserCreationForm()

    if request.method=='POST':
        action = request.POST.get('action',False)
        if action=='register':
            # create new dict for copying email into username because request.POST is immutable
            musiphile_email = request.POST.get('musiphile_email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            data = {
                'username' : musiphile_email,
                'musiphile_email' : musiphile_email,
                'password1' : password1,
                'password2' : password2,
            }

            register_form = UserCreationForm(data=data)
            register_form.is_valid()

        elif action=='login':
            data = request.POST.copy()
            login_form = AuthenticationForm(data=data)
            login_form.is_valid()


    login_form.auto_id = 'login_%s'
    register_form.auto_id = 'signup_%s'


    return {'login_form':login_form, 'register_form':register_form}
