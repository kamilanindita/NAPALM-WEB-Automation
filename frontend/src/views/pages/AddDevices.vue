<template>
  <div>
    <CCard>
      <CCardHeader>
        <CRow>
          <CCol>
            <CIcon name="cil-library-add"/> Add Device
          </CCol>
          <CCol class="text-right">
            <CButton color="info" @click="toggledHelp = !toggledHelp">{{ toggledHelp? 'Hide' : 'Help?' }}</CButton>
          </CCol>
        </CRow>
      </CCardHeader>
      <CCardBody>
        <CRow>
          <CCol>
            <CCollapse :show="toggledHelp">
              <CRow class="mb-4">
                <CCol>
                  <HelpAddDevice />
                </CCol>
              </CRow>
            </CCollapse>
          </CCol>
        </CRow>
        <CRow>
          <CCol lg="6" sm="12">
            <CCard>
              <CCardHeader>
                Device
              </CCardHeader>
              <CCardBody>
                <FormAddDevice :currentAlertCounter="currentAlertCounter" :responsTestConnection="responsTestConnection" :addLoading="addLoading" v-on:add="addDevice($event)" v-on:testConnectionDevice="testConnectionDevice($event)" />
              </CCardBody>
            </CCard>
          </CCol>
          <CCol lg="6" sm="12">
            <CCard>
              <CCardHeader>
                Results
              </CCardHeader>
              <CCardBody>
                <CAlert v-if="results" color="success">
                  {{ results }}
                </CAlert>
                <CAlert v-else-if="results" color="danger">
                  {{ results }}
                </CAlert>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>
  </div>
</template>


<script>
import FormAddDevice from '../components/forms/FormAddDevice'
import HelpAddDevice from '../components/helps/HelpAddDevice'

import { postDevice }  from '@/services/addDevice.js'
import axios from "axios";

export default {
  name:'AddDevice',
  components:{
    FormAddDevice,
    HelpAddDevice,
  },
  onIdle () {
    this.$store.dispatch('userLogout')
      .then(() => {
        this.$router.push({ name: 'Logout' })
      })
  },
  data(){
    return {
      results:'',
      toggledHelp:false,
      responsTestConnection:'',
      currentAlertCounter:0,
      addLoading:false
    }
  },
  methods:{
    addDevice(device){
      this.addLoading=true
      const promise = new Promise((resolve, reject) => {
        axios.post('/devices/', { 
          'ip_address':device.ip_address,
          'username':device.username,
          'password':device.password,
          'type_device':device.type_device,
          'network_driver':device.network_driver,
          'optional_args':device.optional_args
         })
          .then(response => {
              this.addLoading=false
              this.results=response.data.information
              this.$store.dispatch('DeviceList')
              this.$store.dispatch('DeviceOption')
              resolve()
          })
          .catch(err => {
              this.addLoading=false
              this.results=''
              console.log(err)
              reject(err)
          })
      })
      
    },
    testConnectionDevice(ip){
      this.currentAlertCounter=5
      const promise = new Promise((resolve, reject) => {
        axios.post('/devices/connection/', { 'ip_address':ip })
          .then(response => {
              this.responsTestConnection=response.data.connection
              resolve()
          })
          .catch(err => {
              console.log(err)
              reject(err)
          })
      })
    }
  }
}
</script>