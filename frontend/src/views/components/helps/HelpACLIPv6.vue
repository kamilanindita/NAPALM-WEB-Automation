<template>
    <CCard>
        <CCardHeader>
            <p>Fitur Device List</p>
        </CCardHeader>
        <CCardBody>
            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                    Fitur ACL IPv6 Configuration merupakan proses konfigurasi
                    ACL IPv6 ke perangkat jaringan yang telah terdaftar pada sistem aplikasi. Pengguna dapat
                    memilih satu atau beberapa perangkat sekaligus untuk dilakuakn konfigurasi ACL IPv6.
                    Terdapat beberapa fitur diantaranya yaitu sistem akan melakukan pengecekan
                    koneksi dari sistem ke perangkat jaringan yang telah dipilih, kemudian terdapat fitur untuk melihat existing konfigurasi ACL sehingga
                    diharapkan melihat konfigurasi yang telah ada pada perangkat jaringan agar tidak
                    terjadi masalah dikemudian setelah dilakukan konfigurasi ACL. Pada menu
                    konfigurasi ACL IPv6 ini pengguna dapat melakukan konfigurasi baik secara Graphic
                    User Interface (GUI) maupun Commands Line Interface (CLI).
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Existing Configurations
                </CCardHeader>
                <CCardBody style="text-align:justify;">
                    Memilih tombol Existing, maka akan menampilkan konfigurasi
                    ACL baik pada protocol TCP/IPv4 atau TCP/IPv6 yang ada pada perangkat jaringan yang
                    telah dipilih pada form combo box bernama Device.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # GUI Configurations
                </CCardHeader>
                <CCardBody style="text-align:justify;">
                    Pengguna dapat melakukan konfigurasi dengan
                    mengisikan parameter yang telah disediakan di dalam form seperti protocol, source
                    address, source wildcard, source port, destination address, destination wildcard,
                    destination port, description, dan action sehingga tidak perlu tahu syntax atau perintah di
                    berbagai vendor jaringan. Tersedia combo box bernama Device untuk pemilihan perangkat
                    jaringan yang akan dilakukan konfigurasi ACL IPv6. Form combo box tersebut memiliki daftar
                    perangkat jaringan yang sudah terdaftar pada sistem aplikasi yang terdiri dari hostname
                    dan alamat ip. Ketika perangkat jaringan dipilih maka sistem akan melakukan pengecekan
                    koneksi otomatis terlebih dahulu dari sistem aplikasi ke perangkat yang dituju sebelum
                    dilakukan konfigurasi ACL. Selain itu tersedia juga form nama untuk konfigurasi, tipe
                    traffic dan interface yang akan digunakan atau ditempatkannya rule.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # CLI Configurations
                </CCardHeader>
                <CCardBody style="text-align:justify;">
                    Memilih tombol ikon code (Commands Line Interface/CLI Configuration),
                    maka akan muncul tampilan form textarea yang disediakan untuk memperluas parameter
                    parameter konfigurasi ACL IPv6 dimana secara default menggunakan GUI yang terbatas
                    pada parameter konfigurasinya, namun pada fitur ini pengguna harus memiliki 
                    pengetahuan terhadap syntax atau perintah dari berbagai vendor perangkat jaringan karena
                    konfigurasi ditulis secara manual atau konvensional.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Results
                </CCardHeader>
                <CCardBody style="text-align:justify;">
                    Results, merupakan respon atau hasil ketika selesai melakukan proses konfigurasi ACL pada perangkat jaringan.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Contoh
                </CCardHeader>
                <CCardBody>
                    Pilih device yang akan dilakukan konfigurasi ACL IPv4,<br>
                    <img src="../../../../public/img/help/acl/ipv6_select_device.png" style="width:100%; height:auto;"/>
                    Secara otomatis akan dilakukan pengecekan konektivitas oleh sistem, <br>
                    <img src="../../../../public/img/help/acl/ipv6_device_connected.png" style="width:100%; height:auto;"/>
                    Apabila sebelumnya perangkat jaringan sudah ada konfigurasinya, maka dapat dilihat pada Existing,<br>
                    <img src="../../../../public/img/help/acl/ipv6_existing.png" style="width:100%; height:auto;"/>
                    Secara default sistem aplikasi menggunakan kondifurasi GUI, isikan parameter pada form isian sesuai kebutuhan, <br>
                    <img src="../../../../public/img/help/acl/ipv6_GUI_parameter.png" style="width:100%; height:auto;"/>
                    Setelah selesai mengisi parameter, pilih tombol Run untuk melakukan konfigurasi, tungu sampai selesai, <br>
                    <img src="../../../../public/img/help/acl/ipv6_GUI_loading.png" style="width:100%; height:auto;"/>
                    Apabila telah selesai, maka akan terdapat informasi pada Bagian Result, <br>
                    <img src="../../../../public/img/help/acl/ipv6_GUI_success.png" style="width:100%; height:auto;"/>
                    Selanjutnya apabila memilih konfigurasi secara CLI, maka isikan syntax sesuai vendor, 
                    <img src="../../../../public/img/help/acl/ipv6_CLI_parameter.png" style="width:100%; height:auto;"/>
                    Setelah mengisi parameter sesuai kebutuhan dengan menggunakan syntax sesuai dengan vendor yang digunakan, pilih Run untuk menjalankan konfigurasi.Tunggu sampai selesai.
                    <img src="../../../../public/img/help/acl/ipv6_CLI_loading.png" style="width:100%; height:auto;"/>
                    Apabila telah selesai, maka akan terdapat informasi pada Bagian Result, <br>
                    <img src="../../../../public/img/help/acl/ipv6_CLI_success.png" style="width:100%; height:auto;"/>
                    Selesai.
                </CCardBody>
            </CCard>

        </CCardBody>
    </CCard>
</template>

export default {
    name:'HelpACLIPv6'
}