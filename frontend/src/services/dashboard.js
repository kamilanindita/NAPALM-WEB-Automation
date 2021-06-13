import { getAPI } from '../stores/axios'

const getSummary = () => {
    const promise = new Promise((resolve, reject) => {
        getAPI.get('/devices/informations/summary', { headers: { Authorization: `Bearer ${this.$store.state.accessToken}` } })
        .then(response => {
            resolve(response.data)
        })
        .catch(err => {
            reject(err)
        })
    })
    return promise
}

function getLastHistory() {
    const responses=[
        { "date": "15:00:15, 14-01-2021", "device": "IP Address: 192.168.100.104 ,Type: Router, Vendor: Huawei", "config": "permit  ip any any", "status": "Success"},
        { "date": "14:16:15, 13-01-2021", "device": "IP Address: 192.168.100.105 ,Type: Router, Vendor: Mikrotik", "config": "permit icmp any any", "status": "Failed"},
        { "date": "14:15:15, 13-01-2021", "device": "IP Address: 192.168.100.102 ,Type: Router, Vendor: Juniper", "config": "deny icmp any any", "status": "Success"},
        { "date": "14:14:15, 13-01-2021", "device": "IP Address: 192.168.100.101 ,Type: Router, Vendor: Cisco", "config": "permit  ip any any", "status": "Success"},
        { "date": "14:13:15, 13-01-2021", "device": "IP Address: 192.168.100.103 ,Type: Switch, Vendor: Arista", "config": "permit icmp any any", "status": "Failed"},
    ]
    return responses;
}


export { getSummary, getLastHistory }






  