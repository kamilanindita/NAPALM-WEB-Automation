<template>
    <CDataTable
        :items="items"
        :fields="fields"
        hover
        small
        border
        sorter
    >
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
                { key: 'created_at',label: 'Date', _style:'width:215px;'},
                { key: 'devices',label: 'Device', _style:'width:200px'},
                { key: 'config',label: 'Configuration', _style:'min-width:80px'},
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