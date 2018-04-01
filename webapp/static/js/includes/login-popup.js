import 'materialize-css/dist/js/materialize.min.js';
import '../../sass/includes/auth-popups.scss';


$(function () {
$('.login-popup').each(function (el) {
    $('.btn-login').click((e) => {
        e.preventDefault();
        $('.login-modal').modal('open');
    });
    $('.btn-login-submit').click((e) => {
        e.preventDefault();
        var data = {
            email: $('.login-inp-email').val(),
            password: $('.login-inp-password').val()
        };
        console.log(data);
        $('.login-error').hide();
        $.ajax({
            url: '/api/auth/login/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
        })
        .done((data) => {
            if (data.success) {
                alert('logged in');
                window.location = '/';
            } else {
                $('.login-error').show();
                alert('Failed');
            }
        });
    });
});
})
