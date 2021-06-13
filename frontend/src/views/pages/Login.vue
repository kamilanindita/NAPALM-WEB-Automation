<template>
  <div class="c-app flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol sm="8" md="6" lg="4">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <FormLogin :incorrectAuth="incorrectAuth" v-on:login="login($event)" />
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
import FormLogin from '../components/forms/FormLogin'
import axios from "axios";

export default {
  name: 'Login',
  components:{
    FormLogin
  },
  data () {
    return {
      incorrectAuth: false
    }
  },
  methods: {
    login (account) {
      this.$store.dispatch('userLogin', {
        username: account.username,
        password: account.password
      })
      .then(() => {
        this.$router.push({ name: 'Dashboard' })
      })
      .catch(err => {
        console.log(err)
        this.incorrectAuth = true
      })
      }
    }
}
</script>

</script>
