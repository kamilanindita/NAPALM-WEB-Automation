import Vue from 'vue'
import Router from 'vue-router'

// Views containers
const TheContainer = () => import('@/views/containers/TheContainer')

// Views - page
const Dashboard = () => import('@/views/pages/Dashboard')
const AddDevices = () => import('@/views/pages/AddDevices')
const DeviceLists = () => import('@/views/pages/DeviceLists')
const ACLIPv4 = () => import('@/views/pages/ACLIPv4')
const ACLIPv6 = () => import('@/views/pages/ACLIPv6')
const Backup = () => import('@/views/pages/Backup')
const Restore = () => import('@/views/pages/Restore')
const History = () => import('@/views/pages/History')
const Login = () => import('@/views/pages/Login')
const Logout = () => import('@/views/pages/Logout')
const Register = () => import('@/views/pages/Register')
const NotFound = () => import('@/views/pages/Page404')

Vue.use(Router)

export default new Router({
  mode: 'history',
  linkActiveClass: 'active',
  scrollBehavior: () => ({ y: 0 }),
  routes: configRoutes()
})

function configRoutes () {
  return [
    {
      path: '/',
      redirect:'/dashboard',
      name: 'Dashboard',
      component: TheContainer,
      meta: {
        requiresLogin: true
      },
      children: [
        {
          path: 'dashboard',
          name: 'Home',
          component: Dashboard,
        },
        {
          path: 'dashboard/add-device',
          name: 'Add Device',
          component: AddDevices
        },
        {
          path: 'dashboard/device-list',
          name: 'Device List',
          component: DeviceLists
        },
        {
          path: 'dashboard/backup',
          name: 'Backup',
          component: Backup
        },
        {
          path: 'dashboard/restore',
          name: 'Restore',
          component: Restore
        },
        {
          path: 'dashboard/history',
          name: 'History',
          component: History
        },
        {
          path: 'dashboard/acl-ipv4',
          name: 'ACL IPv4',
          component: ACLIPv4
        },
        {
          path: 'dashboard/acl-ipv6',
          name: 'ACL IPv6',
          component: ACLIPv6
        },
      ]
    },
    {
      path: '/',
      name: 'Auth',
      component: {
        render (c) { return c('router-view') }
      },
      children: [
        {
          path: 'login',
          name: 'Login',
          component: Login
        },
        {
          path: 'logout',
          name: 'Logout',
          component: Logout
        },
        {
          path: 'register',
          name: 'Register',
          component: Register
        }
      ]
    },
    { path: '*', name:'NotFound', component: NotFound }
  ]
}

