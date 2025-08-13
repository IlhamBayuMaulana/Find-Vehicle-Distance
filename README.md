Kode bekerja dengan urutan seperti berikut:
- Area spesifik akan digambar ke citra
- Hanya kendaraan di area tersebut yang akan dihitung jaraknya
- Jarak dihitung dengan menggunakan persamaan segitiga dengan input berupa lebar pixel citra, lebar pixel kendaraan yang terdeteksi, dan panjang kamera ke kendaraan sebagai referensi
- Kemudian dicari tinggi kamera ke tanah, berupa panjang jarak antara kamera ke kendaraan terdekat yang dikurangi sebanyak 10%
- Dari panjang jarak antara kemera ke kendaraan dan tinggi kamera, dihitung panjang dari lampu lalu lintas (tanah) ke kendaraan menggunakan rumus pitagoras.
- Setelah semua kendaraan yang terdeteksi telah dihitung jaraknya, dipilih n jarak terjauh berdasarkan y terendah
- Kemudian dari n jarak tersebut diambil rata-ratanya, rata-rata tersebut digunakan sebagai jarak terjauh
