<template>
    <CCard>
        <CCardHeader>
            <p>Fitur Device List</p>
        </CCardHeader>
        <CCardBody>
            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                    Device List merupakan daftar kumpulan dari perangkat jaringan yang sudah ditambahkan ke dalam sistem.
                    Pada menu ini, pengguna dapat mengetahui daftar perangkat yang telah
                    ditambahkan ke sistem aplikasi yang digunakan untuk melakukan remote perangkat
                    jaringan untuk keperluan automasi. Secara garis besar, menu Device List terbagi
                    menjadi dua bagian utama, pertama terkait informasi detail seperti detail informasi
                    perangkat, interfaces, dan tabel ARP dari perangkat jaringan.
                    Bagian kedua terkait action terhadap informasi parameter untuk melakukan remot perangkat jaringan yaitu action 
                    edit dan delete perangkat dari Device List.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Daftar Tabel Perangkat
                </CCardHeader>
                <CCardBody>
                    Terdapat informasi mengenai semua perangkat jaringan yang telah terdaftar dalam sistem aplikasi. Terdapat beberapa informasi seperti IP Address,
                    Type device, tombol detail informasi perangkat, tombol interface, tombol tabel ARP, tanggal perangkat ditambahkan, serta terdapat tombol action edit dan delete.
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Pada tombol Informations, terhadap informasi perangkat jaringan seperti FQDN, HOSTNAME,INTERFACE LIST,MODEL, OS VERSION, SERIAL NUMBER, UPTIME, dan VENDOR.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                Pada tombol Interfaces, terhadap informasi seperti IP Address, Enabled, UP, Description, MAC Address, MTU, dan Speed.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CListGroupItem color="danger" style="text-align:justify;">
                Pada tombol ARP Table, terhadap informasi seperti Interface, MAC Address, IP, Age.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Sinkronisasi
                </CCardHeader>
                <CCardBody>
                    Tombol Sync yang berfungsi untuk proses sinkronisasai agar mendapatkan data atau informasi terbaru dari perangkat jaringan.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Edit
                </CCardHeader>
                <CCardBody>
                    Tombol edit akan menampilkan informasi untuk kebutuhan konektivitas dari sistem apliksi ke perangkat jaringan
                    seperti informasi ip address, username dan password SSH, type device, network driver,
                    dan optional args yang dapat diganti atau diperbarui sesuai kebutuhan pengguna apabila
                    terjadi pembaruan koneksi pada perangkat.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Delete
                </CCardHeader>
                <CCardBody>
                    Tombol delete akan menampilkan informasi ip address terkait perangkat atau sebagai konfirmasi terhadap
                    perangkat yang akan dihapus, bila sesuai dengan perangkat yang akan dihapus maka
                    tinggal memilih OK, namun apabila tidak sesuai maka pilih Cancel.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Contoh
                </CCardHeader>
                <CCardBody>
                    Pilih perangkat yang tersedia, pilih tombol sesuai dengan nama kolom.<br>
                    <img src="../../../../public/img/help/devicelist/device_list.png" style="width:100%; height:auto;"/>
                    <br>
                    Ketika memilih tombol detail informasi perangkat maka akan menampilkan
                    informasi dalam menu pop up memuat informasi seperti fqdn, hostname, interface list,
                    model, os version, serial number, uptime, dan vendor.<br>
                    Apabila akan memperbarui data atau informasi detail perangkat dapat menekan tombol Sync.<br>
                    <img src="../../../../public/img/help/devicelist/informations.png" style="width:100%; height:auto;"/>
                    <br>
                    Kemudian apabila memilih tombol detail interface perangkat maka akan
                    menampilkan informasi dalam menu pop up memuat informasi seperti name, enabled, up,
                    description, mac address, MTU, dan speed<br>
                    Bila akan memperbarui data atau informasi interface perangkat dapat menekan tombol Sync.<br>
                    <img src="../../../../public/img/help/devicelist/interfaces.png" style="width:100%; height:auto;"/>
                    <br>
                    Selanjutnya apabila memilih tombol tabel ARP maka akan menampilkan informasi
                    dalam menu pop up memuat informasi seperti nama interface, mac address, ip address, dan age. <br>
                    Bila akan memperbarui data atau informasi tabel ARP perangkat dapat menekan tombol Sync.<br>
                    <img src="../../../../public/img/help/devicelist/arp.png" style="width:100%; height:auto;"/>
                    <br>
                    Bila akan memperbarui data atau informasi perangkat dapat menekan tombol atau icon edit pada kolom action.<br>
                    <img src="../../../../public/img/help/devicelist/edit.png" style="width:100%; height:auto;"/>
                    <br>
                    Bila akan menghapus perangkat dapat menekan tombol atau icon delete pada kolom action.<br>
                    <img src="../../../../public/img/help/devicelist/delete.png" style="width:100%; height:auto;"/>
                </CCardBody>
            </CCard>

        </CCardBody>
    </CCard>
</template>

export default {
    name:'HelpDeviceLists'
}