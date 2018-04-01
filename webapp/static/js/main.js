import _ from 'lodash';
import '../sass/main.scss';

import 'materialize-css/dist/js/materialize.min.js';


import './includes/signup-popup.js';
import './includes/login-popup.js';


$(function () {
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


    // Initialize jQuery widgets;

    $('.modal').modal();
});
