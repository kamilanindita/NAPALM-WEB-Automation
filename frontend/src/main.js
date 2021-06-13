import 'core-js/stable'
import Vue from 'vue'
import App from './App'
import router from './router'
import CoreuiVue from '@coreui/vue'
import { iconsSet as icons } from './assets/icons/icons.js'
import store from './stores/store'
import IdleVue from 'idle-vue'
import Multiselect from 'vue-multiselect'
import axiosSetup from "./stores/axios";


// call the axios setup method here
axiosSetup()

// register globally
Vue.component('multiselect', Multiselect)

const eventsHub = new Vue()

//idle 5 menit
Vue.use(IdleVue, {
  eventEmitter: eventsHub,
  idleTime: 300000
})



Vue.config.performance = true
Vue.use(CoreuiVue)
Vue.prototype.$log = console.log.bind(console)

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresLogin)) {
    if (!store.getters.loggedIn) {
	  //store.dispatch("RefreshToken",{con:false});
      next({ name: 'Login' })
    } else {
	  //store.dispatch("RefreshToken",{con:true});
      next()
    }
  } else {
    next()
  }
})



new Vue({
  el: '#app',
  router,
  store,
  icons,
  template: '<App/>',
  components: {
    App
  }
})
