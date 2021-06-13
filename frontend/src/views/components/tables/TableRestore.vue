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
            color="primary"
            variant="outline"
            square
            size="sm"
            @click="toggleDetails(item, index)"
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
    name: 'TableRestore',
    data(){
        return{
            fields:[
                { key: 'created_at',label: 'Date', _style:'min-width:80px; width:215px;' },
                { key: 'devices',label: 'Device', _style:'min-width:50px; width:200px;'},
                { key: 'restore',label: 'Restore', _style:'min-width:80px', sorter: false, filter:false},
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