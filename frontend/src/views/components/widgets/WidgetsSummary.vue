<template>
  <CRow>
    <CCol sm="6" lg="3">
      <CCard color="primary" style="height:160px;">
        <CCardBody class="text-light">  
          <h3 class="mt-4">{{ summary.devices }}</h3>
          <p>Devices</p>
        </CCardBody>
      </CCard> 
    </CCol>
    <CCol sm="6" lg="3">
      <CCard color="success" style="height:160px;">
        <CCardBody class="text-light">  
          <h3 class="mt-4">{{ summary.success_task }}</h3>
          <p>Success Task</p>
        </CCardBody>
      </CCard>
    </CCol>
    <CCol sm="6" lg="3">
      <CCard color="danger" style="height:160px;">
        <CCardBody class="text-light">  
          <h3 class="mt-4">{{ summary.failed_task }}</h3>
          <p>Failed Task</p>
        </CCardBody>
      </CCard>
    </CCol>
    <CCol sm="6" lg="3">
      <CCard color="info" style="height:160px;">
        <CCardBody class="text-light">  
          <h3 class="mt-4">System Date</h3>
          <p>{{ summary.system }}</p>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>

<script>
export default {
  name: 'WidgetsSummary',
  props:['summary']
}
</script>
