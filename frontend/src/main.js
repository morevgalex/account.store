import Vue from 'vue'
import App from './App.vue'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'


import router from './router'
import store from './store';
import i18n from './i18n'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
}).$mount('#app')
