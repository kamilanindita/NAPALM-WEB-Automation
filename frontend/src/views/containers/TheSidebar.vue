<template>
  <CSidebar 
    fixed 
    :minimize="minimize"
    :show="show"
    @update:show="(value) => $store.commit('set', ['sidebarShow', value])"
  >
    <CSidebarBrand class="d-md-down-none">
      <p class="mb-2 c-sidebar-brand-full text-center">
        <CIcon class="c-avatar-img" name="cil-user" style="background-color:#dad8d8;"/> 
        <br>
        {{ username }}
      </CHeaderNavLink>
      </p>
      <p class="font-weight-bold mt-3 c-sidebar-brand-minimized">
        <CIcon class="c-avatar-img" name="cil-user" style="background-color:#dad8d8;"/> 
      </CHeaderNavLink>
      </p>
    </CSidebarBrand>

    <CRenderFunction flat :content-to-render="$options.nav"/>
    <CSidebarMinimizer
      class="d-md-down-none"
      @click.native="$store.commit('set', ['sidebarMinimize', !minimize])"
    />
  </CSidebar>
</template>

<script>
import nav from './_nav'

export default {
  name: 'TheSidebar',
  nav,
  data(){
    return{
      username:'',
    }
  },
  created(){
    this.username= this.$store.state.username
  },
  computed: {
    show () {
      return this.$store.state.sidebarShow 
    },
    minimize () {
      return this.$store.state.sidebarMinimize 
    }
  }
}
</script>
