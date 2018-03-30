import Vue from 'vue'
import axios from 'axios';
import '../sass/control-panel.scss'
import Vuetify from 'vuetify'


const http = axios.create({
  baseURL: '/api',
  headers: {
    Authorization: 'Bearer {token}'
  }
});
 
Vue.use(Vuetify)
Vue.prototype.$http = http

import App from '../control-panel/app.vue'

Vue.config.productionTip = false


new Vue({
  render: h => h(App)
}).$mount('#app')
