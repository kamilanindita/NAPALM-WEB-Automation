<template>
  <div class="d-flex align-items-center min-vh-100">
    <CContainer fluid>
      <CRow class="justify-content-center">
        <CCol sm="8" md="6" lg="4">
          <CCard class="mx-4 mb-0">
            <CCardBody class="p-4">
              <CForm>
                <h1 class="text-center">Register</h1>
                <br>
                <p class="text-muted text-center">Create your account by contacting the department head</p>
                <br>
                <CRow>
                  <CCol class="text-center">
                    <p class="mt-2"><router-link :to = "{ name:'Login' }" style="color:gray;text-decoration: none;">Sign In?</router-link></p>
                  </CCol>
                </CRow>
              </CForm>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
export default {
  name: 'Register'
}
</script>
