function UserEvent() {
    this.triggerLogin = function() {
        $(this).trigger('user_login');
    }
    return true;
}

var User = {

    eventManager : new UserEvent(),

    init : function() {
        e_m = User.eventManager;
        $(e_m).bind('user_login', User.afterLogin);
    }, 

    openLoginScreen : function() {
        $('#signup_container').css({'display':'block'});
        return false;
    },

    afterLogin : function() {
        $('#login_container').animate({opacity:0}, function() {
                $.get('/accounts/ajax_login_container', function(data) {
                    console.log('data : ' + data);
                    $('#login_container').html(data);
                    $('#login_container').animate({opacity:1});
                });
        });
    },

    closeLoginScreen : function() {
        $('#signup_container').css({'display':'none'});
        return false;
    },

    register : function() {
        form = $('#register_form');
        post_data = {
            'musiphile_email' : form.find('input[name=musiphile_email]').attr('value'),
            'password1'       : form.find('input[name=password1]').attr('value'),
            'password2'       : form.find('input[name=password2]').attr('value'),
            'action'          : form.find('input[name=action]').attr('value')
        };

        $('#signup_container .loading_overlay').css('display','block');

        $.post('/accounts/ajax_signup/', post_data, function(data) {
            $('#signup_container .loading_overlay').css('display','none');
            if (data['status'] == 'failed') {
                $('#register_form_container').html(data['message']);
            } else {
                User.closeLoginScreen();
                User.eventManager.triggerLogin();
            }
        });
        return false;
    },
    
    login : function() {
        form = $('#login_form');
        post_data = {
            'musiphile_email' : form.find('input[name=musiphile_email]').attr('value'),
            'password'        : form.find('input[name=password]').attr('value'),
            'action'          : form.find('input[name=action]').attr('value')
        };

        $('#signup_container .loading_overlay').css('display','block');

        $.post('/accounts/ajax_login/', post_data, function(data) {
            try {
                $('#signup_container .loading_overlay').css('display','none');
                if (data['status']=='failed') {
                    $('#login_form_container').html(data['message']);
                } else {
                    User.closeLoginScreen();
                    User.eventManager.triggerLogin();
                }
            } catch(e) {
                alert('Error : ' + e.description);
                return false;
            }

        });
        return false;
    }
}
