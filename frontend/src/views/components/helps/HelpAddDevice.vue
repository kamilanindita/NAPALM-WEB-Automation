<template>
    <CCard>
        <CCardHeader>
            <p>Fitur Add Device</p>
        </CCardHeader>
        <CCardBody>
            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                    Fitur Add Device merupakan proses menambahkan perangkat jaringan baru ke dalam sistem. Pada menu ini, pengguna dapat menambahkan informasi berupa parameter konfigurasi perangkat jaringan
                    yang digunakan untuk melakukan remote perangkat jaringan untuk keperluan automasi.
                </CListGroupItem>
            </CCard>
            <CCard>
                <CCardHeader>
                    # IP Address
                </CCardHeader>
                <CCardBody>
                     Alamat IP dari perangkat jaringan yang akan dilakukan automasi. Format penulisan ip address yang digunakan adalah ip vesi 4, sebagai contoh: 192.168.1.1.
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Terdapat ujicoba konektivitas secara otomatis terhadap perangkat jaringan yang akan ditambahkan setelah pengisian IP Address. Apabila terhubung akan mendapatkan infomasi status Connected, namun apabil tidak terhubung maka statusnya Disconnected.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Username
                </CCardHeader>
                <CCardBody>
                    Nama pengguna untuk proses autentikasi pada perangkat jaringan. Menggunakan sistem autentikasi secara terpusat, memanfaatkan RADIUS atau TACACS+ untuk proses autentikasi ke perangkat jaringan sehingga menggunakan nama pengguna (username) dari perangkat jaringan yang telah terdaftar sebelumnya pada server autentikasi.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Password
                </CCardHeader>
                <CCardBody>
                    Kata sandi yang sesuai dengan Nama pengguna (username) yang telah terdaftar pada server autentikasi.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Type Device
                </CCardHeader>
                <CCardBody>
                    Jenis atau tipe dari perangkat jaringan. Terdapat pilihan: Router, Switch.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Network Driver
                </CCardHeader>
                <CCardBody>
                    Driver digunakan agar setiap perangkat jaringan yang terpasang dapat terhubung atau dikenalli serta dapat berinteraksi dengan sistem. Berikut ini driver yang sudah include dalam NAPALM dan dapat digunakan pada sistem ini sesuai dengan masing masing vendor:<br>
                    <CDataTable
                        :items="items"
                        :fields="fields"
                        hover
                        small
                        border
                    >
                </CDataTable>
                    Driver lain yang dapat digunakan yaitu huawei_vrp dan ros. NAPALM driver huawei_vrp untuk perangkat vendor HUAWEI Campus Network Switch dapat mendukung versi S5700,S6700,dll. NAPALM driver ros untuk perangkat vendor Mikrotik.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Optional Args
                </CCardHeader>
                <CCardBody>    
                Meyediakan parameter konfigurasi tambahan bilamana diperlukan melalui opsi penerusan argumen opsional tertentu ke beberapa driver sehingga dapat mengirimkan parameter tertentu yang dibutuhkan oleh perangkat jaringan yang tidak tersedia pada form konfigurasi. Penulisan argumen dalam format dictionary atau key and value seperti {'key':'value'}. Berikut ini key argumen yang dapat digunakaan: <br>
                <ul>
                    <li>dest_file_system (ios) - Destination file system for SCP transfers (default: flash:).</li>
                    <li>enable_password (eos) - Password required to enter privileged exec (enable) (default: '').</li>
                    <li>force_no_enable (ios, nxos_ssh) - Do not automatically enter enable-mode on connect (default: False).</li>
                    <li>global_delay_factor (ios, nxos_ssh) - Allow for additional delay in command execution (default: 1).</li>
                    <li>port (eos, ios, iosxr, junos, nxos, nxos_ssh) - Allows you to specify a port other than the default.</li>
                    <li>secret (ios, nxos_ssh) - Password required to enter privileged exec (enable) (default: '').</li>
                </ul>
                
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                Tombol <CButton color="primary" size="sm" disabled>Add</CButton> digunakan untuk menambahkan perangkat jaringan ke dalam sistem setalah pengisian parameter yang diperlukan.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Results, merupakan respon ketika melakukan proses penambahan perangkat jaringan dengan menekan tombol <CButton color="primary" size="sm" disabled>Add</CButton>, apabila berhasil menambahkan perangkat akan mendapat respon dari sistem aplikasi berupa
                informasi detail sepeti, hostname, interface list, model, version, vendor dan lain
                sebagainya dari perangkat jaringan yang berhasil ditambahkan, namun bila gagal akan mendapatkan informasi failed.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Contoh
                </CCardHeader>
                <CCardBody>
                    1. Isikan IP address, apabila terhubung maka akan mendapatkan status seperti di bawah ini:<br>
                    <img src="../../../../public/img/help/adddevice/status-connected.png" style="width:100%; height:auto;"/>
                    2. Isikan parameter selanjutnya yang dibutuhkan,<br>
                    <img src="../../../../public/img/help/adddevice/add-parameter.png" style="width:100%; height:auto;"/>
                    2. Setelah selesai mengisi parameter, klik tombol Add, tunggu sampai selesai.<br>
                    <img src="../../../../public/img/help/adddevice/loading.png" style="width:100%; height:auto;"/>
                    4. Apabila berhasil maka akan memperoleh infomasi seperti di bawah ini,<br>
                    <img src="../../../../public/img/help/adddevice/result.png" style="width:100%; height:auto;"/>
                    5. Selesai.
                </CCardBody>
            </CCard>

        </CCardBody>
    </CCard>
</template>

<script>
export default {
    name:'HelpAddDevice',
    data (){
        return {
            items:[{'-':'Driver Name','eos':'eos','junos':'junos','ios':'ios'},{'-':'Structured data','eos':'yes','junos':'yes','ios':'no'},{'-':'Minimum version','eos':'4.15.0F','junos':'12.1','ios':'12.4(20)T'},{'-':'Backend library','eos':'pyeapi','junos':'junos-eznc','ios':'netmiko'}],
            fields:[
                { key: '-',label: '-', _style:'width:215px;'},
                { key: 'eos',label: 'eos'},
                { key: 'junos',label: 'junos'},
                { key: 'ios',label: 'ios'}
            ]
        }
    }
}

</script>