<template>
  <CHeader fixed with-subheader light>
    <CToggler
      in-header
      class="ml-3 d-lg-none"
      @click="$store.commit('toggleSidebarMobile')"
    />
    <CToggler
      in-header
      class="ml-3 d-md-down-none"
      @click="$store.commit('toggleSidebarDesktop')"
    />
    <CHeaderBrand class="mx-auto d-lg-none" to="/">
      <p class="font-weight-bold mt-3">ACCESS CONTROL LIST CONFIGURATION MANAGEMENT</p>
    </CHeaderBrand>
    <CHeaderNav class="d-md-down-none  mr-auto">
      <p class="font-weight-bold mt-3">ACCESS CONTROL LIST CONFIGURATION MANAGEMENT</p>
    </CHeaderNav>
    <CHeaderNav class="mr-4">
      <CButton color="danger" size="sm" v-c-tooltip="'Logout'" @click="logoutConfirm" >
        Logout <CIcon name="cil-account-logout" size="sm"/>
      </CButton>
      <CModal
            title="Confirm Logout"
            color="danger"
            :show.sync="warningLogout"
             @update:show="closeModal" 
      >
            Are you sure you want to logout this username {{ username }}?
      </CModal>
    </CHeaderNav>
    <CSubheader class="px-3">
      <CBreadcrumbRouter class="border-0 mb-0"/>
    </CSubheader>
  </CHeader>
</template>

<script>
export default {
  name: 'TheHeader',
  data(){
    return {
      username:'',
      warningLogout: false,
    }
  },
  created(){
    this.username= this.$store.state.username
  },
  methods:{
    logoutConfirm() {
      this.warningLogout = true
    },
    closeModal(status, evt, accept) { 
      if (accept) { 
        return this.$router.push('/logout')
      }
    }
  }
}
</script>
