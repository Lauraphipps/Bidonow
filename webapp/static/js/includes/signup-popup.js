import 'materialize-css/dist/js/materialize.min.js';
import '../../sass/includes/auth-popups.scss';


$(function () {
$('.signup-popup').each(function (el) {
    $('.btn-sign-up').click((e) => {
        e.preventDefault();
        $('#sign-up-popup').modal('open');
    });
    $('.btn-sign-up-submit').click((e) => {
        e.preventDefault();
        var data = {
            email: $('.inp-email').val(),
            password: $('.inp-password').val()
        };
        console.log(data);
        $.ajax({
            url: '/api/auth/signup/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
        })
        .done((response) => {
            console.log(response);
            alert('success');
            $('.sign-up-modal').modal('close');
            $('.login-modal').modal('open');
        });
    });
});
});
