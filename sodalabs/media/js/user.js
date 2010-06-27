function UserEvent() {
    this.triggerLogin = function(user_id,user_name) {
        $(this).trigger('user_login', {'user_id':user_id,'user_name':user_name});
    }
    return true;
}

var User = {

    eventManager : new UserEvent(),

    init : function() {
        e_m = User.eventManager;
        $(e_m).bind('user_login', User.afterLogin);
        $(document).bind('hrefChanged', User.userSelected);
    }, 

    userSelected : function(e, diff) {
        if(diff.user) {
            $('#sub_header').html('<h3>'+diff['user']+'</h3>');
        }
    },

    openLoginScreen : function() {
        $('#signup_container').css({'display':'block'});
        return false;
    },

    afterLogin : function(e, data) {
        $('#login_container').animate({opacity:0}, function() {
                $.get('/accounts/ajax_login_container', function(data) {
                    $('#login_container').html(data);
                    $('#login_container').animate({opacity:1});
                });
        });

        DocString.add({'user':data['user_name']});
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
                User.eventManager.triggerLogin(data['user_id'],data['user_name']);
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
                    User.eventManager.triggerLogin(data['user_id'],data['user_name']);
                }
            } catch(e) {
                alert('Error : ' + e.description);
                return false;
            }

        });
        return false;
    }
}
