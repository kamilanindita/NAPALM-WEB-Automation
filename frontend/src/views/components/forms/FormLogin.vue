<template>
    <CForm v-on:submit.prevent="login">
        <p style="font-size:18px; font-weight:bold" class="text-center">Access Control List <br> Configuration Management</p>
        <p class="text-muted">Sign In to your account</p>
        <CAlert color="danger" v-if="incorrectAuth">
            Incorrect username or password entered - please try again
        </CAlert>
        <CInput
            :value.sync="account.username"
            placeholder="Username"
            autocomplete="username"
        >
            <template #prepend-content><CIcon name="cil-user"/></template>
        </CInput>
        <CInput
            :value.sync="account.password"
            placeholder="Password"
            type="password"
            autocomplete="curent-password"
            @keyup.enter="$emit('login',account)"
        >
            <template #prepend-content><CIcon name="cil-lock-locked"/></template>
        </CInput>
        <CRow>
        <CCol col="6" class="text-left">
            <CButton v-on:click.prevent="$emit('login',account)" color="primary" class="px-4">Login</CButton>
        </CCol>
        <CCol col="6" class="text-right">
            <p class="mt-2"><CIcon name="cil-user-follow"/><router-link :to = "{ name:'Register' }" style="color:gray;text-decoration: none;">Register?</router-link></p>
        </CCol>
        </CRow>
    </CForm>
</template>

<script>

export default {
  name:'FormLogin',
  data(){
    return {
      account: {
          username:'',
          password:'',
      },
    }
  },
  props:['incorrectAuth']
}
</script>