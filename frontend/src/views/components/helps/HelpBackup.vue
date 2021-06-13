<template>
    <CCard>
        <CCardHeader>
            <p>Fitur Backup</p>
        </CCardHeader>
        <CCardBody>
            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                    Fitur Backup merupakan proses membuat data cadangan sehingga data cadangan tersebut dapat digunakan kembali apabila terjadi kerusakan atau kehilangan.
                    Pada menu ini, pengguna dapat menyalin konfigurasi acl
                    yang ada pada perangkat. Pengguna dapat memilih satu atau beberapa perangkat
                    sekaligus untuk dilakuakn backup.
                </CListGroupItem>
            </CCard>
            <CCard>
                <CCardHeader>
                    # Device
                </CCardHeader>
                <CCardBody>
                    Merupakan perangkat jaringan yang akan dilakukan proses backup. Terdapat kumpulan perangkat jaringan yang sudah terdaftar pada sistem, pilih perangkat jaringan yang diingikan.
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Sebelum melakukan proses backup, sistem akan
                melakukan pengecekan koneksi dari sistem ke perangkat jaringan yang telah dipilih.
                Ketika perangkat yang dipilih dapat terhubung dengan status Connected maka pengguna dapat melakukan proses backup, namun apabil statusnya Disconnected maka proses backup tidak dapat dilakukan.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Tombol <CButton color="success" size="sm" disabled><CIcon name="cil-plus" /> </CButton>
                </CCardHeader>
                <CCardBody style="text-align:justify;">
                    Digunakan untuk menambahkan kembali perangkat jaringan yang akan dilakukan proses backup, sehingga dapat melakukan proses backup lebih dari satu perangkat jaringan sekaligus. Batas maksimal penambahan perangkat jaringan pada proses backup adalah 4 sehingga dalam sekali proses backup total dapat melakukan backup 5 buah perangkat jaringan.
                </CCardBody>
            </CCard>

            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                Tombol <CButton color="primary" size="sm" disabled>Backup</CButton> digunakan untuk melakukan proses backup terhadap perangkat jaringan yang telah dipilih.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CListGroupItem color="success" style="text-align:justify;">
                Message, terdapat notifikasi atau pemberitahuan berupa pesan status proses backup dari masing masing perangkat yang telah dipilih dalam proses backup, apabila berhasil akan memiliki status success, namun apabila gagal memiliki status failed.
                </CListGroupItem>
            </CCard>

            <CCard>
                <CCardHeader>
                    # History Backup
                </CCardHeader>
                <CCardBody>
                    Merupakan informasi berupa tabel riwayat backup konfigurasi perangkat jaringan yang telah dilakuakan menggunakan sistem baik yang berhasil maupun gagal. Dapat melihat langsung hasil backup konfigurasi serta dapat melakukan pengunduhan/download file backup yang telah berhasil dilakuakan.
                </CCardBody>
            </CCard>

            <CCard>
                <CCardHeader>
                    # Contoh
                </CCardHeader>
                <CCardBody>
                    Pilih perangkat yang akan di backup.<br>
                    <img src="../../../../public/img/help/backup/backup_select_device.png" style="width:100%; height:auto;"/>
                    Secara otomatis sistem akana pengecekan konektivitas perangkat terlebih dahulu, maka bila berhasil terhubung seperti di bawah ini,<br>
                    <img src="../../../../public/img/help/backup/backup_device_connected.png" style="width:100%; height:auto;"/>
                    Pilih tombol Backup, lalu tunggu sampai proses selesai,<br>
                    <img src="../../../../public/img/help/backup/backup_loading.png" style="width:100%; height:auto;"/>
                    Bila berhasil akan menampilkan status success,<br>
                    <img src="../../../../public/img/help/backup/backup_success.png" style="width:100%; height:auto;"/>
                    Apabila ingin mengunduh file backup dapat memilih tombol atau icon download seperti di bawah ini,<br>
                    <img src="../../../../public/img/help/backup/backup_download.png" style="width:100%; height:auto;"/>
                    Hasil file backup seperti di bawah ini,<br>
                    <img src="../../../../public/img/help/backup/backup_file.png" style="width:100%; height:auto;"/>
                    4. Selesai.
                </CCardBody>
            </CCard>

        </CCardBody>
    </CCard>
</template>

export default {
    name:'HelpBackup'
}