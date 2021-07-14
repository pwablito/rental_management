import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import * as VueGoogleMaps from 'vue2-google-maps'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(VueGoogleMaps, {
    load: {
        key: "<INSERT_API_KEY_HERE>",
    }
});

Vue.config.productionTip = false

new Vue({
    render: h => h(App),
}).$mount('#app')