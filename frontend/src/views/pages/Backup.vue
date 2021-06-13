<template>
  <div>
    <CCard>
      <CCardHeader>
         <CRow>
          <CCol>
            <CIcon name="cil-cloud-download"/> Backup
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
                  <HelpBackup />
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
                        <CRow>
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
                          <CCol col=3>
                            <CSpinner v-if="statusLoading" size="sm" color="info"/>
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
                    Backup <CSpinner size="sm" color="light"/>
                    </CButton>

                    <CButton 
                      v-else="runLoading"
                      color="primary" 
                      @click="runBackup"
                    >
                      Backup
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
                History Backup
              </CCardHeader>
              <CCardBody>
                 <TableBackup :items="items" v-on:toggleDownload="toggleDownload($event)"/>
                 <CRow>
                  <CButton v-if="this.$store.getters.BackupConfiguration.previous" @click="prevPage" class="ml-3" size="sm" color="primary"><CIcon name="cil-chevron-left"/></CButton>
                  <CButton v-else class="ml-3" size="sm" color="secondary"><CIcon name="cil-chevron-left" disabled/></CButton>
                  <CButton v-if="this.$store.getters.BackupConfiguration.next" @click="nextPage" class="ml-1" size="sm" color="primary"><CIcon name="cil-chevron-right" /></CButton>
                  <CButton v-else class="ml-1" size="sm" color="secondary"><CIcon name="cil-chevron-right" disabled/></CButton>
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
import TableBackup from '../components/tables/TableBackup'
import HelpBackup from '../components/helps/HelpBackup' 
import axios from "axios";

export default {
  name: 'Backup',
  components: {
    TableBackup,
    HelpBackup
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
      page:1,
      counter: 0,
      currentAlertCounter:5,
      statusLoading:false,
      runLoading:false,
      device_options:[],
      devices: [{
        id:0,
        idDevice: '',
      }],
      Status:[],
      toggledHelp:false,
    }
  },
  mounted(){
    this.getDevices()
    this.getBackup()
  },
  methods: {
    prevPage(){
        if(this.$store.getters.BackupConfiguration.previous){
          this.$store.dispatch('BackupConfiguration', {
            url: this.$store.getters.BackupConfiguration.previous
          })
          .then(() => {
            this.getBackup()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },
    nextPage(){
        if(this.$store.getters.BackupConfiguration.next){
          this.$store.dispatch('BackupConfiguration', {
            url: this.$store.getters.BackupConfiguration.next
          })
          .then(() => {
            this.getBackup()
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
          id: ++this.counter,
          idDevice: this.$store.getters.DeviceOptions[0].value,
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
    runBackup() {
      this.runLoading=true
      this.currentAlertCounter=5
      this.Status=[]
      for (var i = 0; i < this.devices.length; i++) {
        const promise = new Promise((resolve, reject) => {
          axios.get(`/devices/backup/${this.devices[i].idDevice}/run`)
            .then(response => {
              this.runLoading=false
              this.Status.push(response.data.status) 
              this.$store.dispatch('BackupConfiguration')
                .then(()=>{
                  this.items=this.$store.getters.BackupConfiguration.results.map((item, id) => { return {...item, id}})
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
              this.$store.dispatch('BackupConfiguration')
                .then(()=>{
                  this.items=this.$store.getters.BackupConfiguration.results.map((item, id) => { return {...item, id}})
                })
                .catch(err=>{
                  console.log(err)
                })
              reject(err)
            })
        })
      } 
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
    getBackup(){
      if (this.$store.getters.BackupConfiguration){
        this.items=this.$store.getters.BackupConfiguration.results.map((item, id) => { return {...item, id}})
      }
      else{
        this.$store.dispatch('BackupConfiguration')
          .then(()=>{
            this.items=this.$store.getters.BackupConfiguration.results.map((item, id) => { return {...item, id}})
          })
          .catch(err=>{
            console.log(err)
          })
      }
    },
    toggleDownload(item){
      if(item.filename){
        const promise = new Promise((resolve, reject) => {
          axios.get(`/backup/${item.filename}`, { responseType: 'blob' })
          .then(response => {
            const blob = new Blob([response.data])
            const link = document.createElement('a')
            link.href = URL.createObjectURL(blob)
            link.download = item.filename
            link.click()
            URL.revokeObjectURL(link.href)
            resolve()
          })
          .catch(err=>{
            console.log(err)
            reject(err)
          })
        })
      }
    },
  }
}
</script>
