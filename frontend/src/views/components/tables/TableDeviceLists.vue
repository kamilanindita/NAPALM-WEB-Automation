<template>
    <CDataTable
        :items="items"
        :fields="fields"
        hover
        border
        sorter
    >

        <template #information_details="{item, index}">
        <td class="py-2 text-center">
            <CButton
            color="primary"
            variant="outline"
            square
            size="sm"
            @click="toggleInformation(item, index)"
            >
            <CIcon name="cil-external-link"/>               
            </CButton>
        </td>
        </template>
        
        <template #interfaces_details="{item, index}">
            <td class="py-2 text-center">
                <CButton
                color="primary"
                variant="outline"
                square
                size="sm"
                @click="toggleInterface(item, index)"
                >
                <CIcon name="cil-external-link"/>
                </CButton>
            </td>
        </template>
        <template #arp_details="{item, index}">
        <td class="py-2 text-center">
            <CButton
            color="primary"
            variant="outline"
            square
            size="sm"
            @click="toggleARP(item, index)"
            >
            <CIcon name="cil-external-link"/>
            </CButton>
        </td>
        </template>
        <template #action="{item, index}">
        <td class="py-2 text-center">
            <CButton
            color="primary"
            variant="outline"
            square
            size="sm"
            @click="toggleEdit(item)"
            >
            <CIcon name="cil-pencil"/>
            </CButton>
            &nbsp;
            
            <CButton
            color="primary"
            variant="outline"
            square
            size="sm"
            @click="toggleDeleteConfirm(item)"
            >
            <CIcon name="cil-trash"/>
            </CButton>
        </td>
        </template>
        
        <template #details="{item}">
        
        <CModal
            title="Confirm Delete"
            color="danger"
            :show.sync="warningDelete"
             @update:show="closeModalDelete"
        >
            Are you sure you want to delete this {{ deviceDelete.type }} device with ip address {{ deviceDelete.ip_address }}?
        </CModal>

        <CModal
            size="lg"
            color="info"
            :show.sync="modalEdit.toggle"
        >
            <CCard>
            <CCardHeader>
                <CRow>
                <CCol>
                    <p class="font-weight-bold">Edit</p>
                </CCol>
                <CCol class="text-right">
                    <p><span class="font-weight-bold">Last updated:</span> {{ itemEdit.updated_at }}</p>
                </CCol>
                </CRow>
            </CCardHeader>
            <CCardBody>
                <CCol>
                <CCard>
                    <CCardBody>
                    <CRow>
                        <CCol sm="12">
                            <CInput
                                v-model="itemEdit.ip_address"
                                label="IP Address"
                                @change="$emit('testConnectionDevice', itemEdit.ip_address)"
                            />
                            <CAlert :show.sync="currentAlertCounter" v-if="responsTestConnection && responsTestConnection=='Connected'" color="success" closeButton>
                                Status : {{ responsTestConnection }}
                            </CAlert>
                            <CAlert :show.sync="currentAlertCounter" v-else-if="responsTestConnection && responsTestConnection=='Disconnected'" color="danger" closeButton>
                                Status : {{ responsTestConnection }}
                            </CAlert>
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol sm="12">
                            <CInput
                                v-model="itemEdit.username"
                                label="Username"
                            />
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol sm="12">
                        <CInput
                            v-model="itemEdit.password"
                            label="Password"
                        />
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol sm="12">
                        <CSelect
                            :value.sync="itemEdit.type_device"
                            label="Type Device"
                            :options="['Router','Switch']"
                        />
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol sm="12">
                        <CSelect
                            :value.sync="itemEdit.network_driver"
                            label="Network Driver"
                            :options="['ios','eos','junos','ros','huawei_vrp']"
                        />
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol sm="12">
                        <CInput
                            v-model="itemEdit.optional_args"
                            label="Optional Args"
                            placeholder="{}"
                        />
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol>
                            <CAlert :show.sync="currentAlertCounter" v-if="responsUpdate==200" color="success">
                            Status : Success
                            </CAlert>
                            <CAlert :show.sync="currentAlertCounter" v-else-if="responsUpdate && responsUpdate!=200" color="danger">
                                Status : Failed
                            </CAlert>
                        </CCol>
                    </CRow>
                    <CRow>
                        <CCol sm="12">
                        <CButton color="primary" v-on:click.prevent="$emit('handleUpdateDevice',itemEdit)">
                            Update
                        </CButton>
                        </CCol>
                    </CRow>
                    </CCardBody>
                </CCard>
                </CCol>
            </CCardBody>
            </CCard>
        </CModal>

        <CModal
            size="lg"
            color="info"
            :show.sync="modalInformation.toggle"
        >
            <CCard>
            <CCardHeader>
                <CRow>
                <CCol>
                    <p class="font-weight-bold">Informations</p>
                </CCol>
                <CCol class="text-right">
                    <CButton
                    v-if="SyncLoading"
                    size="sm"
                    color="primary"
                    >
                    <CSpinner size="sm" color="light"/> Sync
                    </CButton>

                    <CButton
                    v-else="SyncLoading"
                    size="sm"
                    color="primary"
                    v-on:click.prevent="$emit('handleSyncInformation', modalInformation.id)"
                    >
                    <CIcon name="cil-loop-circular"/> Sync
                    </CButton>
                </CCol>
                </CRow>
            </CCardHeader>
            <CCardBody>
                <CRow>
                <CCol col=2>
                    FQDN
                </CCol>
                <CCol col=10>
                    : {{ informationItems.fqdn }}
                </CCol>
                </CRow> 
                <CRow>
                <CCol col=2>
                    HOSTNAME
                </CCol>
                <CCol col=10>
                    : {{ informationItems.hostname }}
                </CCol>
                </CRow>
                <CRow>
                <CCol col=2>
                    INTERFACE LIST
                </CCol>
                <CCol col=10>
                    : {{ informationItems.interfaces_list }}
                </CCol>
                </CRow>
                <CRow>
                <CCol col=2>
                    MODEL
                </CCol>
                <CCol col=10>
                    : {{ informationItems.model }}
                </CCol>
                </CRow>
                <CRow>
                <CCol col=2>
                    OS VERSION
                </CCol>
                <CCol col=10>
                    : {{ informationItems.os_version }}
                </CCol>
                </CRow>
                <CRow>
                <CCol col=2>
                    SERIAL NUMBER
                </CCol>
                <CCol col=10>
                    : {{ informationItems.serial_number }}
                </CCol>
                </CRow>
                <CRow>
                <CCol col=2>
                    UPTIME
                </CCol>
                <CCol col=10>
                    : {{ informationItems.uptime }}
                </CCol>
                </CRow> 
                <CRow>
                <CCol col=2>
                    VENDOR
                </CCol>
                <CCol col=10>
                    : {{ informationItems.vendor }}
                </CCol>
                </CRow>                 
            </CCardBody>
            <CCardFooter>
                <CAlert :show.sync="currentAlertCounter" v-if="SyncMessage=='success'" color="success" closeButton>
                    Synchronos : {{ SyncMessage }}
                </CAlert>
                <CAlert :show.sync="currentAlertCounter" v-else-if="SyncMessage && SyncMessage!='success'" color="danger" closeButton>
                    Synchronos : {{ SyncMessage }}
                </CAlert>
            </CCardFooter>
            </CCard>
        </CModal>

        <CModal
            size="lg"
            color="info"
            :show.sync="modalInterfaces.toggle"
        >
            <CCard>
            <CCardHeader>
                <CRow>
                <CCol>
                    <p class="font-weight-bold">Interfaces</p>
                </CCol>
                <CCol class="text-right">
                    <CButton
                    v-if="SyncLoading"
                    size="sm"
                    color="primary"
                    >
                    <CSpinner size="sm" color="light"/> Sync
                    </CButton>

                    <CButton
                    v-else="SyncLoading"
                    size="sm"
                    color="primary"
                    v-on:click.prevent="$emit('handleSyncInterface',modalInterfaces.id)"
                    >
                    <CIcon name="cil-loop-circular"/> Sync
                    </CButton>
                </CCol>
                </CRow>
            </CCardHeader>
            <CCardBody>
                <CCol>
                <CDataTable
                    :items="interfacesItems"
                    :fields="interfaces_fields"
                    hover
                    border
                    striped
                />
                </CCol>
            </CCardBody>
            <CCardFooter>
                <CAlert :show.sync="currentAlertCounter" v-if="SyncMessage=='success'" color="success" closeButton>
                    Synchronos : {{ SyncMessage }}
                </CAlert>
                <CAlert :show.sync="currentAlertCounter" v-else-if="SyncMessage && SyncMessage!='success'" color="danger" closeButton>
                    Synchronos : {{ SyncMessage }}
                </CAlert>
            </CCardFooter>
            </CCard>
        </CModal>

        <CModal
            size="lg"
            color="info"
            :show.sync="modalARP.toggle"
        >
            <CCard>
            <CCardHeader>
                <CRow>
                <CCol>
                    <p class="font-weight-bold">ARP Table</p>
                </CCol>
                <CCol class="text-right">
                    <CButton
                    v-if="SyncLoading"
                    size="sm"
                    color="primary"
                    >
                    <CSpinner size="sm" color="light"/> Sync
                    </CButton>

                    <CButton
                    v-else="SyncLoading"
                    size="sm"
                    color="primary"
                    v-on:click.prevent="$emit('handleSyncARP', modalARP.id)"
                    >
                    <CIcon name="cil-loop-circular"/> Sync
                    </CButton>
                </CCol>
                </CRow>
            </CCardHeader>
            <CCardBody>
                <CCol>
                <CDataTable
                    :items="ARPItems"
                    :fields="arp_fields"
                    hover
                    border
                    striped
                />
                </CCol>
            </CCardBody>
            <CCardFooter>
                <CAlert :show.sync="currentAlertCounter" v-if="SyncMessage=='success'" color="success" closeButton>
                    Synchronos : {{ SyncMessage }}
                </CAlert>
                <CAlert :show.sync="currentAlertCounter" v-else-if="SyncMessage && SyncMessage!='success'" color="danger" closeButton>
                    Synchronos : {{ SyncMessage }}
                </CAlert>
            </CCardFooter>
            </CCard>
        </CModal>

        </template>
      
    </CDataTable>
</template>

<script>

const fields = [
  { key: 'ip_address',label: 'IP Address', _style:'min-width:40px' },
  { key: 'type_device',label: 'Type'},
  { 
    key: 'information_details', 
    label: 'Informations', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'interfaces_details', 
    label: 'Interfaces', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'arp_details', 
    label: 'ARP', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  },
  { key: 'created_at',label:'Created At'},
  { 
    key: 'action', 
    label: 'Action', 
    _style: 'min-width:30px;text-align:center;', 
    sorter: false, 
    filter: false
  }
]


const interfaces_fields = [
  { key: 'name',label: 'Name', _style:'min-width:40px' },
  { key: 'is_enabled',label: 'Enabled'},
  { 
    key: 'is_up', 
    label: 'UP', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'description', 
    label: 'Description', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'mac_address', 
    label: 'MAC Address', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'mtu', 
    label: 'MTU', 
    _style: 'min-width:30px;', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'speed', 
    label: 'Speed', 
    _style: 'min-width:30px;', 
    sorter: false, 
    filter: false
  }
]

const arp_fields = [
  { key: 'interface',label: 'Interface', _style:'min-width:40px' },
  { key: 'mac',label: 'MAC Address'},
  { 
    key: 'ip', 
    label: 'IP', 
    sorter: false, 
    filter: false
  },
  { 
    key: 'age', 
    label: 'Age', 
    _style: 'min-width:10px;', 
    sorter: false, 
    filter: false
  }
]

export default {
    name: 'TableDeviceLists',
    data(){
        return{
            fields,
            interfaces_fields,
            arp_fields,
            collapseDuration: 0,
            warningDelete: false,
            deviceDelete:{
                id:'',
                type:'',
                ip_address:''
            },
            modalInformation:{
                id:'',
                toggle: false
            },
            modalInterfaces:{
                id:'',
                toggle: false
            },
            modalARP:{
                id:'',
                toggle: false
            },
            modalEdit:{
                toggle: false,
            },
            itemEdit:{},
            int_list: ['fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3']
        }
    },
    props:['items','informationItems','interfacesItems','ARPItems','currentAlertCounter','responsTestConnection','responsUpdate','SyncMessage','SyncLoading'],
    mounted(){
        
    },
    methods:{
        toggleInformation(item){
            this.$emit('getInformationItems',item.id_device)
            this.modalInformation.id= item.id_device
            this.modalInformation.toggle= true
        },
        toggleInterface(item){
            this.$emit('getInterfaceItems',item.id_device)
            this.modalInterfaces.id= item.id_device
            this.modalInterfaces.toggle= true
        },
        toggleARP(item){
            this.$emit('getARPItems',item.id_device)
            this.modalARP.id= item.id_device
            this.modalARP.toggle= true
        },
        toggleEdit(item){
            this.itemEdit=item
            this.modalEdit.toggle= true
        },
        toggleDeleteConfirm(item) {
            this.deviceDelete.id=item.id_device
            this.deviceDelete.type=item.type_device
            this.deviceDelete.ip_address=item.ip_address
            this.warningDelete = true
        },
         closeModalDelete(status, evt, accept) { 
            if (accept) { 
                this.$emit('handleDeleteDevice',this.deviceDelete.id)
            }
            else{
                this.deviceDelete.id=''
                this.deviceDelete.type=''
                this.deviceDelete.ip_address=''
            }
        },
    }
}
</script>