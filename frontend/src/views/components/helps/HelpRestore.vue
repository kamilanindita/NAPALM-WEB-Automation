<template>
    <CCard>
        <CCardHeader>
            <p>Fitur Restore</p>
        </CCardHeader>
        <CCardBody>
            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                    Fitur Restore merupakan proses mengembalikan kembali sebuah data atau konfigurasi ke pengaturan/konfigurasi yang diingikan sesuai dengan file data pengembalian. Pada menu ini, pengguna dapat mengembalikan konfigurasi acl pada perangkat
                    menggunakan file backup konfigursi ACL. Pengguna dapat memilih satu atau
                    beberapa perangkat sekaligus untuk dilakuakn pengembalian konfigurasi.
                </CListGroupItem>
            </CCard>
            <CCard>
                <CCardHeader>
                    # Device
                </CCardHeader>
                <CCardBody>
                    Merupakan perangkat jaringan yang akan dilakukan proses restore. Terdapat kumpulan perangkat jaringan yang sudah terdaftar pada sistem, pilih perangkat jaringan yang diingikan.
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Sebelum melakukan proses pengembalian, sistem akan melakukan pengecekan koneksi dari
                sistem ke perangkat jaringan yang telah dipilih. Ketika perangkat yang dipilih dapat
                terhubung dengan status Connected maka pengguna dapat melakukan proses restore, 
                namun apabil statusnya Disconnected maka proses restore tidak dapat dilakukan.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Source
                </CCardHeader>
                <CCardBody>
                    Merupakan sumber cadangan data konfigurasi yang akan dikembalikan atau restore. Berupa file hasil backup konfigurasi perangkat jaringan yang pernah dilakuakan.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Tombol <CButton color="success" size="sm" disabled><CIcon name="cil-plus" /></CButton>
                </CCardHeader>
                <CCardBody style="text-align:justify;">
                    Digunakan untuk menambahkan kembali perangkat jaringan yang akan dilakukan proses restore, sehingga dapat melakukan proses restore lebih dari satu perangkat jaringan sekaligus. Batas maksimal penambahan perangkat jaringan pada proses restore adalah 4 sehingga dalam sekali proses restore total dapat melakukan restore 5 buah perangkat jaringan.
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                Tombol <CButton color="primary" size="sm" disabled>Restore</CButton> digunakan untuk melakukan proses restore terhadap perangkat jaringan yang telah dipilih.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Message, terdapat notifikasi atau pemberitahuan berupa pesan status proses restore dari masing masing perangkat yang telah dipilih dalam proses restore, apabila berhasil akan memiliki status success, namun apabila gagal memiliki status failed.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # History Restore
                </CCardHeader>
                <CCardBody>
                    Merupakan informasi berupa tabel riwayat restore konfigurasi perangkat jaringan yang telah dilakuakan menggunakan sistem baik yang berhasil maupun gagal. Dapat melihat langsung hasil restore konfigurasi yang telah berhasil dilakuakan.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Contoh
                </CCardHeader>
                <CCardBody>
                    Pilih perangkat yang akan di restore.<br>
                    <img src="../../../../public/img/help/restore/restore_select_device.png" style="width:100%; height:auto;"/>
                    Akan dilakukan pengecekan konektivitas perangkat terlebih dahulu secara otomatis, maka bila berhasil terhubung seperti di bawah ini,<br>
                    <img src="../../../../public/img/help/restore/restore_device_connected.png" style="width:100%; height:auto;"/>
                    Pilih file backup yang akan dilakukan restore ke perangkat,<br>
                    <img src="../../../../public/img/help/restore/restore_select_file.png" style="width:100%; height:auto;"/>
                    Pilih tombol Restore, lalu tunggu sampai selesai,<br>
                    <img src="../../../../public/img/help/restore/restore_loading.png" style="width:100%; height:auto;"/>
                    Apabila Restore telah selesai, akan menampilkan status success.<br>
                    <img src="../../../../public/img/help/restore/restore_success.png" style="width:100%; height:auto;"/>
                    Selesai.
                </CCardBody>
            </CCard>

        </CCardBody>
    </CCard>
</template>

export default {
    name:'HelpRestore'
}