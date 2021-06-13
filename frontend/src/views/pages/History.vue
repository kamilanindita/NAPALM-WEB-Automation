<template>
  <div>
    <CCard>
      <CCardHeader>
         <CRow>
          <CCol>
            <CIcon name="cil-history"/> History Configuration
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
                  <HelpHistory/>
                </CCol>
              </CRow>
            </CCollapse>
          </CCol>
        </CRow>
        <TableHistory :items="items"/>
        <CRow>
          <CButton v-if="this.$store.getters.HistoryConfiguration.previous" @click="prevPage" class="ml-3" size="sm" color="primary"><CIcon name="cil-chevron-left"/></CButton>
          <CButton v-else class="ml-3" size="sm" color="secondary"><CIcon name="cil-chevron-left"/></CButton>
          <CButton v-if="this.$store.getters.HistoryConfiguration.next" @click="nextPage" class="ml-1" size="sm" color="primary"><CIcon name="cil-chevron-right" /></CButton>
          <CButton v-else class="ml-1" size="sm" color="secondary"><CIcon name="cil-chevron-right" /></CButton>
        </CRow>
      </CCardBody>
    </CCard>
  </div>
</template>

<script>
import TableHistory from '../components/tables/TableHistory'
import HelpHistory from '../components/helps/HelpHistory' 
import axios from "axios";

export default {
  name: 'History',
  components:{
    TableHistory,
    HelpHistory
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
      toggledHelp:false,
    }
  },
  mounted(){
    this.getHistory()
  },
  methods:{
    prevPage(){
        if(this.$store.getters.HistoryConfiguration.previous){
          this.$store.dispatch('HistoryConfiguration', {
            url: this.$store.getters.HistoryConfiguration.previous
          })
          .then(() => {
            this.getHistory()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },
    nextPage(){
        if(this.$store.getters.HistoryConfiguration.next){
          this.$store.dispatch('HistoryConfiguration', {
            url: this.$store.getters.HistoryConfiguration.next
          })
          .then(() => {
            this.getHistory()
          })
          .catch(err => {
            console.log(err)
          })
        }
    },
    getHistory(){
      if (this.$store.getters.HistoryConfiguration){
        this.items=this.$store.getters.HistoryConfiguration.results.map((item, id) => { return {...item, id}})
      }
      else{
        this.$store.dispatch('HistoryConfiguration')
          .then(()=>{
            this.items=this.$store.getters.HistoryConfiguration.results.map((item, id) => { return {...item, id}})
          })
          .catch(err=>{
            console.log(err)
          })
      }
    }
  },
}
</script>




