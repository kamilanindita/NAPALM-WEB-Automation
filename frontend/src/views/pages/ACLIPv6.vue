<template>
  <div>
    <CCard>
      <CCardHeader>
        <CRow>
          <CCol>
            <CIcon name="cil-terminal"/> ACL IPv6
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
                  <HelpACLIPv6 />
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
                    <CCard class="inputDevice" v-for="(device, deviceIndex) in devices" :key="device.id">
                      <CCardHeader>
                        <CRow style="height:30px">
                          <p class="mt-2 ml-3">Device</p>
                          <CCol col=3>
                            <CSelect
                              id="device.id"
                              :value.sync="device.toDevice"
                              :options="device_options"
                              @change="getDeviceExis(deviceIndex, device.toDevice)"
                            />
                          </CCol>
                          <CCol col=3>
                            <CSpinner v-if="statusLoading" size="sm" color="info"/>
                            <CAlert :key="device.id" :show.sync="currentAlertCounter" v-if="Status[deviceIndex]=='Connected'" style="margin-top:-6px" size="sm" color="success" closeButton>
                                <small>Status : {{ Status[deviceIndex] }}</small>
                            </CAlert>
                            <CAlert :key="device.id" :show.sync="currentAlertCounter" v-else-if="Status[deviceIndex]=='Disconnected'" style="margin-top:-6px" size="sm" color="danger" closeButton>
                                <small>Status : {{ Status[deviceIndex] }}</small>
                            </CAlert>
                          </CCol>
                          <CCol class="text-right">
                            <CButton v-if="device.toggledEx" color="primary" size="sm" @click="btnToggleExisting(deviceIndex)">
                              <p style="height:6px">HIDE</p>
                            </CButton>
                            <CButton v-else color="secondary" size="sm" @click="btnToggleExisting(deviceIndex)">
                              <p style="height:6px">EXISTING</p>
                            </CButton>
                             &nbsp;
                            <CButton v-if="device.toggledGUI" color="primary" size="sm" @click="btnToggleGUI(deviceIndex)">
                              <p style="height:6px">GUI</p> 
                            </CButton>
                            <CButton v-else color="secondary" size="sm" @click="btnToggleGUI(deviceIndex)">
                              <p style="height:6px">GUI</p> 
                            </CButton>
                            &nbsp;
                            <CButton v-if="device.toggledCLI" color="primary" size="sm" @click="btnToggledCLI(deviceIndex)">
                              <CIcon name="cil-code"/> 
                            </CButton>
                            <CButton v-else color="secondary" size="sm" @click="btnToggledCLI(deviceIndex)">
                              <CIcon name="cil-code"/> 
                            </CButton>
                            &nbsp;
                            <CButton color="danger" size="sm" v-if="devices.length > 1 && devices.length-1!=deviceIndex"  @click="removeInputDevice(device.id)">
                              <CIcon name="cil-minus"/> 
                            </CButton>
                            <CButton color="success" size="sm" v-else @click="addInputDevice">
                              <CIcon name="cil-plus"/> 
                            </CButton>
                          </CCol>
                        </CRow>
                      </CCardHeader>
                        <CCardBody>
                            <CCollapse :show="Boolean(device.toggledEx)" >
                              <CRow class="mb-4">
                                <CCol>
                                  Existing Configurations
                                  <CSpinner v-if="existingLoading" size="sm" color="info"/>

                                  <CTextarea
                                    v-model="device.aclExis.rule"
                                    rows="4"
                                    disabled
                                  />
                                  <CTextarea
                                    label="Applying to Interfaces"
                                    v-if="device.aclExis.applying"
                                    v-model="device.aclExis.applying"
                                    rows="4"
                                    disabled
                                  />
                                </CCol>
                              </CRow>
                            </CCollapse>
                            <CCollapse :show="Boolean(device.toggledCLI)">
                              <CRow class="mb-4">
                                <CCol>
                                  Commads Line
                                  <CTextarea
                                    v-model="device.CommadsLine"
                                    rows="6"
                                  />
                                </CCol>
                              </CRow>
                            </CCollapse>
                            <CCollapse :show="Boolean(device.toggledGUI)">
                            <CRow>
                              <p class="mt-2 ml-3 mr-1">Name &nbsp;</p>
                              <CCol col=3>
                                <CInput
                                  :value.sync="device.aclName"
                                />
                              </CCol>
                            </CRow>
                            <CRow>
                              <CCol col=3 style="margin-left:57px">
                                <CAlert color="warning" hidden closeButton>
                                    Tidak diperlukan nama
                                </CAlert>
                              </CCol>
                            </CRow>
                           
                            <table>
                              <tr>
                                <td width="80px">Protocol</td>
                                <td min-width="125px">Src Address</td>
                                <td min-width="125px">Src Prefix</td>
                                <td width="55px">Src Port</td>
                                <td min-width="125px">Dst Address</td>
                                <td min-width="125px">Dst Prefix</td>
                                <td width="55px">Dst Port</td>
                                <td width="80px">Description</td>
                                <td width="92px">Action</td>
                                <td>
                                  <CButton color="success" size="sm" @click="addInputList(deviceIndex)">
                                    <CIcon name="cil-plus"/> 
                                  </CButton>
                                </td>
                              </tr>
                              <tr class="inputList" v-for="(list, listIndex) in device.list" :key="list.id">
                                <td>
                                  <CSelect
                                    :value.sync="list.protocol"
                                    :options="['tcp','udp','ipv6','icmp']"
                                  />
                                </td>
                                <td>
                                  <CInput
                                    :value.sync="list.source"
                                  />
                                </td>
                                <td>
                                  <CInput
                                    :value.sync="list.sourcePrefix"
                                  /></td>
                                <td>
                                  <CInput
                                    :value.sync="list.sourcePort"
                                  />
                                </td>
                                <td>
                                  <CInput
                                    :value.sync="list.destination"
                                  /></td>
                                <td>
                                  <CInput
                                    :value.sync="list.destinationPrefix"
                                  /></td>
                                <td>
                                  <CInput
                                    :value.sync="list.destinationPort"
                                  />
                                </td>
                                <td>
                                  <CInput
                                    :value.sync="list.description"
                                  /></td>
                                <td>
                                  <CSelect
                                    :value.sync="list.action"
                                    :options="['permit','deny']"
                                  />
                                </td>
                                <td>
                                  <CButton color="danger" size="sm" class="mb-3" v-if="device.list.length > 1 && device.list.length-1!=listIndex"  @click="removeInputList(deviceIndex, list.id)">
                                    <CIcon name="cil-minus"/> 
                                  </CButton>

                                  <CButton color="success" size="sm" class="mb-3" v-else @click="addInputList(deviceIndex)">
                                    <CIcon name="cil-plus"/> 
                                  </CButton>

                                </td>
                              </tr>
                            </table>

                          <br>
                          <CRow>
                          <CCol>
                          <CRow col=3>
                            <p class="mt-2 ml-3 mr-2">Type Traffic</p>
                            <CSelect
                              :value.sync="device.typeTraffic"
                              :options="['in','out']"
                            />
                          </CRow>
                          </CCol>
                          <CCol col=9>
                          <CRow>
                            <p class="mt-2 ml-3 mr-2">Applying to an Interface </p>
                            <CSelect
                              :value.sync="device.interfacApply"
                              :options="device.intList"
                            />
                          </CRow>
                          </CCol>
                          </CRow>
                          </CCollapse>
                       
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
                    Run <CSpinner size="sm" color="light"/>
                    </CButton>

                    <CButton 
                      v-else="runLoading"
                      color="primary" 
                      @click="runACL"
                    >
                      Run
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
                Result
              </CCardHeader>
              <CCardBody>
                 <CRow  v-for="(item, index) in Results">
                    <CCol>
                      <CAlert v-if="item.status=='success'" color="success">
                          {{ item.result }}
                      </CAlert>
                      <CAlert v-else-if="item.status=='failed'" color="danger">
                          {{ item.result }}
                      </CAlert>
                  </CCol>
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
import HelpACLIPv6 from '../components/helps/HelpACLIPv6';
import axios from "axios";

export default {
  name:'ACLIPv6',
  components:{
    HelpACLIPv6,
  },
  onIdle () {
    this.$store.dispatch('userLogout')
      .then(() => {
        this.$router.push({ name: 'Logout' })
      })
  },
  data () {
    return {
      device_options:['-'],
      devices:[
        {
          id:'device0',
          toDevice:'',
          aclExis:'',
          intList:[],
          aclName:'',
          list:[
            {
              id:'list00',
              protocol:'tcp',
              source:'',
              sourcePrefix:'',
              sourcePort:'',
              destination:'',
              destinationPrefix:'',
              destinationPort:'',
              description:'',
              action:'permit'
            },
          ],
          CommadsLine:'',
          typeTraffic:'in',
          interfacApply:'',
          toggledEx: false,
          toggledGUI: true,
          toggledCLI: false,
        }
      ],
      Status:[],
      currentAlertCounter:5,
      statusLoading:false,
      existingLoading:false,
      runLoading:false,
      deviceCounter:0,
      listCounter:0,
      textExisting:'',
      toggledHelp:false,
      Results:[{
        'status':'',
        'result':''
      }]
    }
  },
  mounted(){
    this.getDevices()
  },
  methods:{
    getDeviceExis(index, id){
      this.existingLoading=true
      axios.get(`/devices/configurations/${id}/existing`)
        .then(response => {
            this.existingLoading=false
            this.devices[index].aclExis=response.data.existing
        })
        .catch(err => {
            this.existingLoading=false
            console.log(err)
        })

      axios.get(`/devices/interfaces/name/${id}/`)
        .then(response => {
            this.devices[index].intList=response.data
        })
        .catch(err => {
            console.log(err)
        })

      this.statusLoading=true
      this.currentAlertCounter=5
      this.Status=[]
      axios.get(`/devices/connection/${id}`)
        .then(response => {
            this.statusLoading=false
            this.Status.push(response.data.connection) 
        })
        .catch(err => {
            this.statusLoading=false
            this.Status.push('failed')
            console.log(err)
        })
      
    },
    getDevices(){
      if (this.$store.getters.DeviceOptions){
        this.device_options=this.$store.getters.DeviceOptions
        this.devices[0].toDevice=this.device_options[0].value
        this.getDeviceExis(0, this.$store.getters.DeviceOptions[0].value)
      }
      else{
        this.$store.dispatch('DeviceOption')
          .then(()=>{
            this.device_options=this.$store.getters.DeviceOptions
            this.devices[0].toDevice=this.device_options[0].value
            this.getDeviceExis(0, this.$store.getters.DeviceOptions[0].value)
          })
          .catch(err=>{
            console.log(err)
          })
      }

    },
    btnToggleExisting(id) {
     this.devices[id].toggledEx = !this.devices[id].toggledEx 
    },
    btnToggleGUI(id) {
     this.devices[id].toggledGUI = true
     this.devices[id].toggledCLI = false
    },
    btnToggledCLI(id) {
     this.devices[id].toggledGUI = false
     this.devices[id].toggledCLI = true
    },
    addInputDevice() {
      if (this.devices.length < 5) { 
        this.devices.push(
          {
            id: `device${++this.deviceCounter}`,
            toDevice:this.$store.getters.DeviceOptions[0].value,
            aclExis:'',
            intList:[],
            aclName:'',
            list:[
                {
                  id:`list${++this.listCounter}`,
                  protocol:'tcp',
                  source:'',
                  sourcePrefix:'',
                  sourcePort:'',
                  destination:'',
                  destinationPrefix:'',
                  destinationPort:'',
                  description:'',
                  action:'permit'
                }
              ],
            CommadsLine:'',
            typeTraffic:'in',
            interfacApply:'',
            toggledEx: false,
            toggledGUI: true,
            toggledCLI: false,
          }
        )
      }
    },
    removeInputDevice(id){
      /*
      let index = this.devices.map((item) => item.id).indexOf(id);
      this.devices.splice(index, 1);
      */
      var deviceList=this.devices.filter((item) => item.id!=id);
      this.devices=deviceList
    },
    addInputList(id) {
      if (this.devices[id].list.length < 5){
        this.devices[id].list.push(
          {
            id:`list${id}${++this.listCounter}`,
            protocol:'tcp',
            source:'',
            sourcePrefix:'',
            sourcePort:'',
            destination:'',
            destinationPrefix:'',
            destinationPort:'',
            description:'',
            action:'permit'
          }
        )
      }
    },
    removeInputList(deviceId, listId) {
        var newList=this.devices[deviceId].list.filter((item) => item.id!=listId);
        this.devices[deviceId].list=newList
    },
    runACL(){
      this.runLoading=true
      this.Results=[{
        'status':'',
        'result':''
      }]

      for (var i = 0; i < this.devices.length; i++) {
        if(this.devices[i].toggledCLI){
          axios.defaults.timeout=30000
          const promise = new Promise((resolve, reject) => {
            axios.post(`/devices/configurations/cli/${this.devices[i].toDevice}/run`,{ 'cli':this.devices[i].CommadsLine })
            .then(response => {
              this.runLoading=false
              this.Results.push({
                'status':response.data.status,
                'result':response.data
              })
              this.$store.dispatch('RecentConfiguration')
              this.$store.dispatch('HistoryConfiguration')
              resolve()
            })
            .catch(err => {
              this.runLoading=false
              this.Results.push({
                'status':'failed',
                'result':response.data
              })
              this.$store.dispatch('RecentConfiguration')
              this.$store.dispatch('HistoryConfiguration')
              console.log(err)
              reject(err)
            })
          })    
        }
        else if(this.devices[i].toggledGUI){
          axios.defaults.timeout=30000
          const promise = new Promise((resolve, reject) => {
            axios.post(`/devices/configurations/ipv6/${this.devices[i].toDevice}/run`,{
               'aclName':this.devices[i].aclName,
               'rule':this.devices[i].list,
               'apply':[{
                 'interface':this.devices[i].interfacApply,
                 'typeTraffic':this.devices[i].typeTraffic
               }]
            })
            .then(response => {
              this.runLoading=false
              this.Results.push({
                'status':response.data.status,
                'result':response.data
              })
              this.$store.dispatch('RecentConfiguration')
              this.$store.dispatch('HistoryConfiguration')
              resolve()
            })
            .catch(err => {
              this.runLoading=false
              this.Results.push({
                'status':'failed',
                'result':response.data
              })
              this.$store.dispatch('RecentConfiguration')
              this.$store.dispatch('HistoryConfiguration')
              console.log(err)
              reject(err)
            })
          })   
        }
      } 
    },
  }
}
</script>
