<template>
  <div>
    <WidgetsSummary :summary="summary"/>
    <CCard>
      <CCardHeader>
        <CRow>
          <CCol>
            <CIcon name="cil-history"/> Recent Configuration
          </CCol>
          <CCol class="text-right">
            <CButton color="primary" size="sm" @click="goToHistory()">
              <CIcon name="cil-chevron-right"/>
            </CButton>
          </CCol>
        </CRow>
      </CCardHeader>
      <CCardBody>
        <TableLastHistory :items="items" />
      </CCardBody>
    </CCard>
    
  </div>
</template>

<script>
import WidgetsSummary from '../components/widgets/WidgetsSummary'
import TableLastHistory from '../components/tables/TableLastHistory'
import axios from "axios";

export default {
  name: 'Dashboard',
  components: {
    WidgetsSummary,
    TableLastHistory
  },
  onIdle () {
    this.$store.dispatch('userLogout')
      .then(() => {
        this.$router.push({ name: 'Logout' })
      })
  },
  data () {
    return {
      items: [],
      summary:{},
      
    }
  },
  created(){
    this.getSummary()
    this.getLastHistory()
  },
  methods: {
    getSummary(){
      const promise = new Promise((resolve, reject) => {
        axios.get('/devices/informations/summary')
          .then(response => {
              this.summary=response.data
              resolve()
          })
          .catch(err => {
              reject(err)
          })
      })
    },
    getLastHistory(){
      if (this.$store.getters.RecentConfiguration){
        this.items=this.$store.getters.RecentConfiguration.map((item, id) => { return {...item, id}})
      }
      else{
        this.$store.dispatch('RecentConfiguration')
          .then(()=>{
            this.items=this.$store.getters.RecentConfiguration.map((item, id) => { return {...item, id}})
          })
          .catch(err=>{
            console.log(err)
          })
      }
    },
    goToHistory(){
      return this.$router.push('/dashboard/history')
    }
  }
}
</script>
