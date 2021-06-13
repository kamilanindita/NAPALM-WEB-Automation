<template>
    <CCard>
        <CCardHeader>
            <p>Fitur History</p>
        </CCardHeader>
        <CCardBody>
            <CCard>
                <CListGroupItem color="info" style="text-align:justify;">
                    Fitur History merupakan proses untuk mencatat atau menyimpan hasil dari konfigurasi acl melalui sistem. Pada menu ini, pengguna dapat mengetahui konfigurasi acl yang pernah dilakukan mengguanakan sistem aplikasi baik yang berhasil atau tidak.
                </CListGroupItem>
            </CCard>
            
            <CCard>
                <CCardHeader>
                    # History
                </CCardHeader>
                <CCardBody>
                    Merupakan informasi berupa tabel riwayat restore konfigurasi perangkat jaringan yang telah dilakuakan menggunakan sistem baik yang berhasil maupun gagal. Dapat melihat langsung hasil restore konfigurasi yang telah berhasil dilakuakan.
                </CCardBody>
            </CCard>

        </CCardBody>
    </CCard>
</template>

export default {
    name:'HelpRestore'
}