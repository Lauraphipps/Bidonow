import _ from 'lodash';
import Vue from 'vue';
import modal from '../components/modal.vue';

import '../sass/main.scss'

// document.body.appendChild(component());

var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue.js!',
        showModal: false
    },
    components: {
        modal: modal
    },
    methods: {
        reverseMessage: function () {
            this.message = this.message.split('').reverse().join('')
        },
        openSignUp: function () {
            alert('Open signup');
        }
    }
});
