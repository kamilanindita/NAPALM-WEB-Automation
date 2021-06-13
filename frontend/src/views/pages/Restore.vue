<template>
  <div>
    <CCard>
      <CCardHeader>
         <CRow>
          <CCol>
            <CIcon name="cil-cloud-upload"/> Restore
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
                  <HelpRestore />
                </CCol>
              </CRow>
            </CCollapse>
          </CCol>
        </CRow>
        <CRow>
          <CCol>
            <CCard>
              <CCardBody>
                <CRow>
                  <CCol>
                    <CCard v-for="(device, index) in devices" :key="device.id" style="height:75px;">
                      <CCardBody>
                        <CRow style="height:30px">
                          <p class="mt-2 ml-3">Device</p>
                          <CCol col=3>
                            <CSelect
                              id="device.id"
                              :value.sync="device.idDevice"
                              :options="device_options"
                              required
                              @change="testConnection()"
                            />
                          </CCol>
                          <p class="mt-2 ml-3">Source</p>
                          <CCol col=3>
                            <input class="mt-1" type="file" @change="loadFileRestore($event, index)" required>
                          </CCol>
                          <CCol col=3>
                            <CSpinner style="margin-left:100px" v-if="statusLoading" size="sm" color="info"/>
                            <CAlert :key="device.id" :show.sync="currentAlertCounter" v-if="Status[index]=='success' || Status[index]=='Connected'" style="margin-top:-6px" size="sm" color="success" closeButton>
                                <small>Status : {{ Status[index] }}</small>
                            </CAlert>
                            <CAlert :key="device.id" :show.sync="currentAlertCounter" v-else-if="Status[index]=='failed' || Status[index]=='Disconnected'" style="margin-top:-6px" size="sm" color="danger" closeButton>
                                <small>Status : {{ Status[index] }}</small>
                            </CAlert>
                          </CCol>
                          <CCol class="text-right">
                            <CButton color="danger" size="sm" @click="removeInputDevice(device.id)" v-if="devices.length-1==index && devices.length!=1">
                              <CIcon name="cil-minus" />
                            </CButton>
                            <CButton color="success" size="sm" @click="addInputDevice" v-else >
                              <CIcon name="cil-plus" /> 
                            </CButton>
                          </CCol>
                        </CRow>
                      </CCardBody>
                    </CCard>
                   </CCol> 
                </CRow>
                <CRow>
                  <CCol sm="12">
                    <CButton
                    v-if="runLoading"
                    size="sm"
                    color="primary"
                    >
                    Restore <CSpinner size="sm" color="light"/>
                    </CButton>

                    <CButton 
                      v-else="runLoading"
                      color="primary" 
                      @click="runRestore"
                    >
                      Restore
                    </CButton>
                  </CCol>
                </CRow>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
        <CRow>
          <CCol>
            <CCard>
              <CCardHeader>
                History Restore
              </CCardHeader>
              <CCardBody>
                <TableRestore :items="items" />
                <CRow>
                  <CButton v-if="this.$store.getters.RestoreConfiguration.previous" @click="prevPage" class="ml-3" size="sm" color="primary"><CIcon name="cil-chevron-left"/></CButton>
                  <CButton v-else class="ml-3" size="sm" color="secondary"><CIcon name="cil-chevron-left"/></CButton>
                  <CButton v-if="this.$store.getters.RestoreConfiguration.next" @click="nextPage" class="ml-1" size="sm" color="primary"><CIcon name="cil-chevron-right" /></CButton>
                  <CButton v-else class="ml-1" size="sm" color="secondary" disabled><CIcon name="cil-chevron-right" /></CButton>
                 </CRow>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>
  </div>
</template>


<script>
import TableRestore from '../components/tables/TableRestore'
import HelpRestore from '../components/helps/HelpRestore'
import { getRestore } from '@/services/restore.js'
import axios from "axios";

export default {
  name: 'Restore',
  components:{
    TableRestore,
    HelpRestore
  },
  onIdle () {
    this.$store.dispatch('userLogout')
      .then(() => {
        this.$router.push({ name: 'Logout' })
      })
  },
  data () {
    return {
      items:[],
      counter: 0,
      currentAlertCounter:5,
      statusLoading:false,
      runLoading:false,
      device_options:[],
      devices: [{
        id: 'device0',
        idDevice: '',
        restore:'',
      }],
      collapseDuration: 0,
      toggledHelp:false,
      text:'',
      responsTestConnection:'',
      Status:[],
    }
  },
  mounted(){
    this.getDevices()
    this.getRestore()
  },
  methods: {
    prevPage(){
        if(this.$store.getters.RestoreConfiguration.previous){
          this.$store.dispatch('RestoreConfiguration', {
            url: this.$store.getters.RestoreConfiguration.previous
          })
          .then(() => {
            this.getRestore()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },
    nextPage(){
        if(this.$store.getters.RestoreConfiguration.next){
          this.$store.dispatch('RestoreConfiguration', {
            url: this.$store.getters.RestoreConfiguration.next
          })
          .then(() => {
            this.getRestore()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },
    toggleDetails (item) {
      this.$set(this.items[item.id], '_toggled', !item._toggled)
      this.collapseDuration = 300
      this.$nextTick(() => { this.collapseDuration = 0})
    },
    addInputDevice() {
      if (this.devices.length < 5){
        this.devices.push({
          id: `device${++this.counter}`,
          idDevice: this.$store.getters.DeviceOptions[0].value,
          restore:'',
        });
      }
    },
    removeInputDevice(id) {
      let index = this.devices.map((item) => item.id).indexOf(id);
      this.devices.splice(index, 1);
    },
    testConnection() {
      this.statusLoading=true
      this.currentAlertCounter=5
      this.Status=[]
      for (var i = 0; i < this.devices.length; i++) {
        const promise = new Promise((resolve, reject) => {
          axios.get(`/devices/connection/${this.devices[i].idDevice}`)
            .then(response => {
                this.statusLoading=false
                this.Status.push(response.data.connection) 
                resolve()
            })
            .catch(err => {
                this.statusLoading=false
                this.Status.push('failed')
                console.log(err)
                reject(err)
            })
        })
      } 
    },
    runRestore() {
      this.runLoading=true
      this.currentAlertCounter=5
      this.Status=[]
      for(var i = 0; i < this.devices.length; i++) {
        this.currentAlertCounter=5
        let formData = new FormData();
        formData.append("file", this.devices[i].restore);
        
        const promise = new Promise((resolve, reject) => {
          axios.defaults.timeout=30000
          axios.post(`/devices/restore/${this.devices[i].idDevice}/run`, formData,{
              headers: {
                  'Content-Type': 'multipart/form-data'
              }
            })
            .then(response => {
                this.runLoading=false
                this.Status.push(response.data.status)
                this.$store.dispatch('RestoreConfiguration')
                  .then(()=>{
                    this.items=this.$store.getters.RestoreConfiguration.results.map((item, id) => { return {...item, id}})
                  })
                  .catch(err=>{
                    console.log(err)
                  })
                resolve()
            })
            .catch(err => {
                this.runLoading=false
                this.Status.push('failed')
                console.log(err)
                this.$store.dispatch('RestoreConfiguration')
                  .then(()=>{
                    this.items=this.$store.getters.RestoreConfiguration.results.map((item, id) => { return {...item, id}})
                  })
                  .catch(err=>{
                    console.log(err)
                  })
                reject(err)
            })
        })
      }     
    },
    loadFileRestore(ev, index) {
      const file = ev.target.files[0];
      this.devices[index].restore=file
    },
    getDevices(){
      if (this.$store.getters.DeviceOptions){
        this.device_options=this.$store.getters.DeviceOptions
        this.devices[0].idDevice=this.device_options[0].value
        this.testConnection()
      }
      else{
        this.$store.dispatch('DeviceOption')
          .then(()=>{
            this.device_options=this.$store.getters.DeviceOptions
            this.devices[0].idDevice=this.device_options[0].value
            this.testConnection()
          })
          .catch(err=>{
            console.log(err)
          })
      }
    },
    getRestore(){
      if (this.$store.getters.RestoreConfiguration){
        this.items=this.$store.getters.RestoreConfiguration.results.map((item, id) => { return {...item, id}})
      }
      else{
        this.$store.dispatch('RestoreConfiguration')
          .then(()=>{
            this.items=this.$store.getters.RestoreConfiguration.results.map((item, id) => { return {...item, id}})
          })
          .catch(err=>{
            console.log(err)
          })
      }
    },
    testConnectionDevice(ip){
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
  }
}

</script>
