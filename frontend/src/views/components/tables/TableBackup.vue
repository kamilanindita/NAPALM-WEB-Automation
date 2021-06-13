<template>
    <CDataTable
        :items="items"
        :fields="fields"
        hover
        border
        sorter
    >
        <template #download="{item, index}">
        <td class="py-2 text-center">
            <CButton
                v-if="item.filename" 
                color="primary"
                variant="outline"
                square
                size="sm"
                v-on:click.prevent="$emit('toggleDownload', item)" 
                >
                <CIcon name="cil-cloud-download"/>
            </CButton>
            <CButton
                v-else="item.filename"
                color="primary"
                variant="outline"
                square
                size="sm" 
                disabled
                >
                <CIcon name="cil-cloud-download"/>
            </CButton>
        </td>
        </template>
        <template #status="{item}">
        <td>
            <CBadge :color="getBadge(item.status)">
            {{item.status}}
            </CBadge>
        </td>
        </template>

    </CDataTable>
</template>

<script>
export default {
    name: 'TableHistory',
    data(){
        return{
            fields:[
                { key: 'created_at',label: 'Date', _style:'min-width:80px; width:215px;' },
                { key: 'devices',label: 'Device', _style:'width:200px;'},
                { key: 'backup',label: 'Configuration', _style:'min-width:80px'},
                { 
                    key: 'download', 
                    label: 'Download', 
                    _style: 'min-width:10px; width:25px;', 
                    sorter: false, 
                    filter: false
                },
                { 
                    key: 'status', 
                    label: 'Status', 
                    _style: 'min-width:10px; width:20px;', 
                }
            ]
        }
    },
    props:['items'],
    methods:{
        getBadge (status) {
        switch (status) {
            case 'success': return 'success'
            case 'failed': return 'danger'
        }
    }
  }
}
</script>