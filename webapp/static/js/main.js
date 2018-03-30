import _ from 'lodash';
import '../sass/main.scss';

import 'materialize-css/dist/js/materialize.min.js';


$(function () {
    $('.btn-sign-up').click((e) => {
        e.preventDefault();
        $('#sign-up-modal').modal('open');
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
        });
    });
    $('.modal').modal();
});
