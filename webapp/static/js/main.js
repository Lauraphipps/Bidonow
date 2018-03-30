import _ from 'lodash';
import '../sass/main.scss';

import 'materialize-css/dist/js/materialize.min.js';


$(function () {
    $('.btn-sign-up').click((e) => {
        e.preventDefault();
        $('.sign-up-modal').modal('open');
    });
    $('.btn-login').click((e) => {
        e.preventDefault();
        $('.login-modal').modal('open');
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
    $('.btn-logout').click((e) => {
        var data = {}
        $.ajax({
            url: '/api/auth/logout/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            async: false,
        })
        .done((data) => {
            alert('logged out');
            window.location = '/';
        });
    });

    $('.modal').modal();
});
