<template>
  <div>
    <CCard>
      <CCardHeader>
        <CRow>
          <CCol>
            <CIcon name="cil-list-rich"/> Device List
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
                  <HelpDeviceLists />
                </CCol>
              </CRow>
            </CCollapse>
          </CCol>
        </CRow>
        <CRow>
          <CCardBody>
            <TableDeviceLists :items="items" :informationItems="informationItems" :interfacesItems="interfacesItems" :ARPItems="ARPItems" :responsUpdate="responsUpdate" :SyncMessage="SyncMessage" :SyncLoading="SyncLoading" :currentAlertCounter="currentAlertCounter" v-on:getInformationItems="getInformationItems($event)" v-on:getInterfaceItems="getInterfaceItems($event)" v-on:getARPItems="getARPItems($event)" v-on:handleUpdateDevice="handleUpdateDevice($event)" v-on:handleDeleteDevice="handleDeleteDevice($event)" :responsTestConnection=responsTestConnection v-on:testConnectionDevice="testConnectionDevice($event)" v-on:handleSyncInformation="handleSyncInformation($event)" v-on:handleSyncInterface="handleSyncInterface($event)" v-on:handleSyncARP="handleSyncARP($event)" />
            <CRow>
              <CButton v-if="this.$store.getters.DeviceLists.previous" @click="prevPage" class="ml-3" size="sm" color="primary"><CIcon name="cil-chevron-left"/></CButton>
              <CButton v-else class="ml-3" size="sm" color="secondary"><CIcon name="cil-chevron-left" disabled/></CButton>
              <CButton v-if="this.$store.getters.DeviceLists.next" @click="nextPage" class="ml-1" size="sm" color="primary"><CIcon name="cil-chevron-right" /></CButton>
              <CButton v-else class="ml-1" size="sm" color="secondary"><CIcon name="cil-chevron-right" disabled/></CButton>
            </CRow>
          </CCardBody>
        </CRow>
      </CCardBody>
    </CCard>
  </div>
</template>


<script>
import TableDeviceLists from '../components/tables/TableDeviceLists'
import HelpDeviceLists from '../components/helps/HelpDeviceLists'
import { getDeviceARP  } from '@/services/deviceLists.js'
import axios from "axios";

export default {
  name: 'DeviceLists',
  components:{
      TableDeviceLists,
      HelpDeviceLists
  },
  onIdle () {
    this.$store.dispatch('userLogout')
      .then(() => {
        this.$router.push({ name: 'Logout' })
      })
  },
  data() {
    return {
      items:[],
      informationItems:[],
      interfacesItems:[],
      ARPItems:[],
      toggledHelp:false,
      responsTestConnection:'',
      responsUpdate:'',
      SyncMessage:'',
      SyncLoading:false,
      currentAlertCounter: 5,
    }
  },
  mounted(){
    this.getDevices()
  },
  methods: {
    getDevices(){
      if(this.$store.getters.DeviceLists){
        this.items=this.$store.getters.DeviceLists.results.map((item, id) => { return {...item, id}})
      }
      else{
        this.$store.dispatch('DeviceList')
          .then(()=>{
            this.items=this.$store.getters.DeviceLists.results.map((item, id) => { return {...item, id}})
          })
          .catch(err=>{
            console.log(err)
          })
      }
    },
    prevPage(){
        if(this.$store.getters.DeviceLists.previous){
          this.$store.dispatch('DeviceList', {
            url: this.$store.getters.DeviceLists.previous
          })
          .then(() => {
            this.getDevices()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },
    nextPage(){
        if(this.$store.getters.DeviceLists.next){
          this.$store.dispatch('DeviceList', {
            url: this.$store.getters.DeviceLists.next
          })
          .then(() => {
            this.getDevices()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },

    getInformationItems(id){
      this.informationItems=[]
      this.currentAlertCounter=5
      this.SyncMessage=null
      const promise = new Promise((resolve, reject) => {
        axios.get(`/devices/informations/${id}`)
          .then(response => {
              if(response.data){
                this.informationItems=response.data
              }
              else if(response.data.status==404){
                this.SyncMessage='data interfaces not found'
              }
              else if(response.data.status==500){
                this.SyncMessage='error bad request'
              }
              resolve()
          })
          .catch(err => {
              this.informationItems=[]
              this.SyncMessage='error bad request'
              console.log(err)
              reject(err)
          })
      })
    },
    getInterfaceItems(id){
      this.interfacesItems=[]
      this.currentAlertCounter=5
      this.SyncMessage=null
      const promise = new Promise((resolve, reject) => {
        axios.get(`/devices/interfaces/${id}`)
          .then(response => {
              if(response.data){
                this.interfacesItems=response.data
                this.interfacesItems=this.interfacesItems.map((item, id) => { return {...item, id}})
              }
              else if(response.data.status==404){
                this.SyncMessage='data interfaces not found'
              }
              else if(response.data.status==500){
                this.SyncMessage='error bad request'
              }
              resolve()
          })
          .catch(err => {
              this.interfacesItems=[]
              console.log(err)
              reject(err)
          })
      })
    },
    getARPItems(id){
      this.ARPItems=[]
      this.currentAlertCounter=5
      this.SyncMessage=null
      const promise = new Promise((resolve, reject) => {
        axios.get(`/devices/arp/${id}`)
          .then(response => {
              if(response.data){
                this.ARPItems=response.data
                this.ARPItems=this.ARPItems.map((item, id) => { return {...item, id}})
              }
              else if(response.data.status==404){
                this.SyncMessage='data interfaces not found'
              }
              else if(response.data.status==500){
                this.SyncMessage='error bad request'
              }
              resolve()
          })
          .catch(err => {
              this.ARPItems=[]
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
    },
    handleSyncInformation(id){
      this.SyncLoading=true
      this.currentAlertCounter=5
      this.SyncMessage=null
      const promise = new Promise((resolve, reject) => {
        axios.get(`/devices/informations/${id}/synchronos/`)
          .then(response => {
              if(response.data.status=="failed"){
                this.SyncLoading=false
                this.SyncMessage=response.data.message
              }
              else{
                this.SyncLoading=false
                this.SyncMessage="success"
                this.informationItems=response.data
              }
              resolve()
          })
          .catch(err => {
              this.SyncLoading=false
              this.SyncMessage='error bad request'
              console.log(err)
              reject(err)
          })
      })
    },
    handleSyncInterface(id){
      this.SyncLoading=true
      this.currentAlertCounter=5
      this.SyncMessage=null
      const promise = new Promise((resolve, reject) => {
        axios.get(`/devices/interfaces/${id}/synchronos/`)
          .then(response => {
              if(response.data.status=="failed"){
                this.SyncLoading=false
                this.SyncMessage=response.data.message
              }
              else{
                this.SyncLoading=false
                this.SyncMessage="success"
                this.interfacesItems=response.data
              }
              resolve()
          })
          .catch(err => {
              this.SyncLoading=false
              this.SyncMessage='error bad request'
              console.log(err)
              reject(err)
          })
      })
    },
    handleSyncARP(id){
      this.SyncLoading=true
      this.currentAlertCounter=5
      this.SyncMessage=null
      const promise = new Promise((resolve, reject) => {
        axios.get(`/devices/arp/${id}/synchronos/`)
          .then(response => {
              if(response.data.status=="failed"){
                this.SyncLoading=false
                this.SyncMessage=response.data.message
              }
              else{
                this.SyncLoading=false
                this.SyncMessage="success"
                this.ARPItems=response.data
              }
              resolve()
          })
          .catch(err => {
              this.SyncLoading=false
              this.SyncMessage='error bad request'
              console.log(err)
              reject(err)
          })
      })
    },
    handleUpdateDevice(item){
      this.currentAlertCounter=5
      const promise = new Promise((resolve, reject) => {
        axios.put(`/devices/${item.id_device}/`, 
        { 
          'ip_address':item.ip_address,
          'username':item.username,
          'password':item.password,
          'type_device':item.type_device,
          'network_driver':item.network_driver,
          'optional_args':item.optional_args
        })
          .then(response => {
              this.$store.dispatch('DeviceList')
              .then(()=>{
                this.responsUpdate=response.status
                this.items=this.$store.getters.DeviceLists.results.map((item, id) => { return {...item, id}})
              })
              .catch(err=>{
                console.log(err)
              })
              resolve()
          })
          .catch(err => {
              console.log(err)
              reject(err)
          })
      })
    },
    handleDeleteDevice(id){
      const promise = new Promise((resolve, reject) => {
        axios.delete(`/devices/${id}/`)
          .then(response => {
              this.$store.dispatch('DeviceList')
              .then(()=>{
                this.items=this.$store.getters.DeviceLists.results.map((item, id) => { return {...item, id}})
                this.$store.dispatch('DeviceOption')
              })
              .catch(err=>{
                console.log(err)
              })
              resolve()
          })
          .catch(err => {
              console.log(err)
              reject(err)
          })
      })
    },
  }
}
</script>