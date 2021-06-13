<template>
    <CForm v-on:submit.prevent="add">
        <CRow>
            <CCol sm="12">
                <CInput
                :value.sync="device.ip_address"
                label="IP Address*"
                placeholder="192.168.1.100"
                @change="$emit('testConnectionDevice', device.ip_address)"
                required
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
                :value.sync="device.username"
                label="Username*"
                placeholder="Admin"
                required
                />
            </CCol>
        </CRow>
        <CRow>
            <CCol sm="12">
                <CInput
                :value.sync="device.password"
                label="Password*"
                placeholder="Admin"
                type="password"
                required
                />
            </CCol>
        </CRow>
        <CRow>
            <CCol sm="12">
                <CSelect
                :value.sync="device.type_device"
                label="Type Device*"
                :options="['Select','Router','Switch']"
                required
                />
            </CCol>
        </CRow>
        <CRow>
            <CCol sm="12">
                <CSelect
                :value.sync="device.network_driver"
                label="Network Driver*"
                :options="['Select','ios','eos','junos','ros','huawei_vrp']"
                required
                />
            </CCol>
        </CRow>
        <CRow>
            <CCol sm="12">
                <CInput
                :value.sync="device.optional_args"
                label="Optional Args"
                placeholder="{'key':'value'}"
                />
            </CCol>
        </CRow>
        <CRow>
            <CCol sm="12">
                <CButton
                    v-if="addLoading"
                    size="sm"
                    color="primary"
                >
                    Add <CSpinner size="sm" color="light"/>
                </CButton>

                <CButton 
                    v-else="addLoading" 
                    color="primary" 
                    v-on:click.prevent="$emit('add',device)"
                >
                    Add
                </CButton>
            </CCol>
        </CRow>
    </CForm>
</template>

<script>

export default {
  name:'FormAddDevice',
  data(){
    return {
      device: {
          ip_address:'',
          username:'',
          password:'',
          type_device:'',
          network_driver:'',
          optional_args:''
      },
      effectButton:false,
    }
  },
  props:['currentAlertCounter','responsTestConnection','addLoading'],
  methods:{

  }
}
</script>