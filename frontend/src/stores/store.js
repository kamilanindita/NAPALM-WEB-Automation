import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';
import Cookies from 'js-cookie';
import axios from "axios";

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    accessToken:  null,
    refreshToken:  null,
    username:'',
    sidebarShow: 'responsive',
    sidebarMinimize: false,
    deviceOptions:null,
    deviceLists:null,
    recentConfiguration:null,
    historyConfiguration:null,
    backupConfiguration:null,
    restoreConfiguration:null,
	countDown:null,
  },
  plugins: [createPersistedState({
    paths: ['accessToken','refreshToken','username','sidebarShow','sidebarMinimize'],
    storage: {
      getItem: key => Cookies.get(key),
      setItem: (key, value) => Cookies.set(key, value, { expires: 3, secure: false }),
      removeItem: key => Cookies.remove(key)
    }
  })],
  mutations: {
    updateStorage (state, { access, refresh, username, countDown }) {
      state.accessToken = access
      state.refreshToken = refresh
      state.username = username
	  state.countDown = countDown
    },
    updateStorageToken (state, { access, refresh }) {
      state.accessToken = access
      state.refreshToken = refresh
    },
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
    },
    updateDeviceOptions (state, { items }) {
      state.deviceOptions = items
    },
    updateDeviceLists (state, { items }) {
      state.deviceLists = items
    },
    updateRecentConfiguration (state, { items }) {
      state.recentConfiguration = items
    },
    updateHistoryConfiguration (state, { items }) {
      state.historyConfiguration = items
    },
    updateBackupConfiguration (state, { items }) {
      state.backupConfiguration = items
    },
    updateRestoreConfiguration (state, { items }) {
      state.restoreConfiguration = items
    },
    destroyAllData (state) {
      state.deviceOptions=null
      state.deviceLists=null
      state.recentConfiguration=null
      state.historyConfiguration=null
      state.backupConfiguration=null
      state.restoreConfiguration=null
	  state.countDown=null
    },
    toggleSidebarDesktop (state) {
      const sidebarOpened = [true, 'responsive'].includes(state.sidebarShow)
      state.sidebarShow = sidebarOpened ? false : 'responsive'
    },
    toggleSidebarMobile (state) {
      const sidebarClosed = [false, 'responsive'].includes(state.sidebarShow)
      state.sidebarShow = sidebarClosed ? true : 'responsive'
    },
    set (state, [variable, value]) {
      state[variable] = value
    }
  },
  getters: {
    loggedIn (state) {
      return state.accessToken != null
    },
    getAccessToken: state => state.accessToken,
    getRefreshToken: state => state.refreshToken,
    DeviceOptions: state => state.deviceOptions,
    DeviceLists: state => state.deviceLists,
    RecentConfiguration: state => state.recentConfiguration,
    HistoryConfiguration: state => state.historyConfiguration,
    BackupConfiguration: state => state.backupConfiguration,
    RestoreConfiguration: state => state.restoreConfiguration

  },
  actions: {
    userLogout (context) {
      if (context.getters.loggedIn) {
		  //localStorage.removeItem('access_token')
		  //localStorage.removeItem('refresh_token')
          context.commit('destroyToken')
          context.commit('destroyAllData')
		  
      }
    },
    userLogin (context, usercredentials) {
      return new Promise((resolve, reject) => {
        axios.post('/api/token/', {
          username: usercredentials.username,
          password: usercredentials.password
        })
          .then(response => {
			//localStorage.setItem('access_token', response.data.access)
			//localStorage.setItem('refresh_token', response.data.refresh)
            console.log(response)
            context.commit('updateStorage', { access: response.data.access, refresh: response.data.refresh, username: usercredentials.username, countDown:3000 })
			resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
	  RefreshToken (context, params) {
		//let t
		//if (context.getters.loggedIn) {
			//if(params.con){
				//t=setInterval(function () {
					//alert("Hello\nHow are you?");
					return new Promise((resolve, reject) => {
						axios.post('/api/token/refresh/', {
							'refresh':this.state.refreshToken
						})
						.then(response => {
							context.commit('updateStorageToken', { access: response.data.access, refresh: response.data.refresh }) 
							resolve()
						})
						.catch(err => {
							reject(err);
						})
					})
				//},5000);
			//}
			//else{
				//clearInterval(t)
			//}
		//}
		//else{
			//clearInterval(t)
		//}
    },
    DeviceOption (context) {
      return new Promise((resolve, reject) => {
        axios.get('/devices/summary/list/')
					.then(response => {
						context.commit('updateDeviceOptions', { items: response.data }) 
						resolve()
					})
					.catch(err => {
						reject(err);
					})
      })
    },
    DeviceList (context, prevnext) {
      if(prevnext){
        return new Promise((resolve, reject) => {
          axios.get(prevnext.url)
            .then(response => {
              context.commit('updateDeviceLists', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
      else{
        return new Promise((resolve, reject) => {
          axios.get('/devices/')
            .then(response => {
              context.commit('updateDeviceLists', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
    },
    RecentConfiguration (context) {
      return new Promise((resolve, reject) => {
        axios.get('/devices/configurations/recent/')
					.then(response => {
						context.commit('updateRecentConfiguration', { items: response.data.results }) 
						resolve()
					})
					.catch(err => {
						reject(err);
					})
      })
    },
    HistoryConfiguration (context, prevnext) {
      if(prevnext){
        return new Promise((resolve, reject) => {
          axios.get(prevnext.url)
            .then(response => {
              context.commit('updateHistoryConfiguration', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
      else{
        return new Promise((resolve, reject) => {
          axios.get('/devices/configurations/')
            .then(response => {
              context.commit('updateHistoryConfiguration', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
    },
    BackupConfiguration (context, prevnext) {
      if(prevnext){
        return new Promise((resolve, reject) => {
          axios.get(prevnext.url)
            .then(response => {
              context.commit('updateBackupConfiguration', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
      else{
        return new Promise((resolve, reject) => {
          axios.get('/devices/backup/')
            .then(response => {
              context.commit('updateBackupConfiguration', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
    },
    RestoreConfiguration (context, prevnext) {
      if(prevnext){
        return new Promise((resolve, reject) => {
          axios.get(prevnext.url)
            .then(response => {
              context.commit('updateRestoreConfiguration', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
      else{
        return new Promise((resolve, reject) => {
          axios.get('/devices/restore/')
            .then(response => {
              context.commit('updateRestoreConfiguration', { items: response.data }) 
              resolve()
            })
            .catch(err => {
              reject(err);
            })
        })
      }
    },
  },
})
