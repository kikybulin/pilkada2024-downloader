# Pilkada 2024 C1 Downloader

Proyek ini adalah alat otomatisasi untuk mengunduh data dan gambar dari TPS (Tempat Pemungutan Suara) di Pilkada 2024. Pengguna dapat memilih provinsi, kota, kecamatan, kelurahan, hingga TPS tertentu untuk mengunduh gambar terkait. Program ini mendukung multithreading untuk mempercepat proses pengunduhan.

# Cara Penggunaan

```bash
  python main.py
```
# Struktur Folder
Setiap unduhan akan diorganisir dalam folder sebagai berikut:

```
 ├─<Provinsi>
 │    ├── <Kota>
 │    │    ├── <Kecamatan>
 │    │    │    ├── <Kelurahan>
 │    │    │    │    ├── <TPS 1>
 │    │    │    │    │    ├── gambar1.jpg
 │    │    │    │    │    ├── gambar2.jpg
 │    │    │    │    ├── <TPS 2>
 │    │    │    │    │    ├── gambar1.jpg
```

![Screenshot_1](https://github.com/user-attachments/assets/1b7f9b79-17e5-49a5-89fc-5052664bac07)
![Screenshot_3](https://github.com/user-attachments/assets/38f5bb75-adaa-42d9-b382-623e974de54c)
![Screenshot_2](https://github.com/user-attachments/assets/3f71f5c6-20b4-4034-a405-7eb958e13143)
![Screenshot_4](https://github.com/user-attachments/assets/48d33777-ba2a-4bd3-8c72-a960639a7b0d)
![Screenshot_5](https://github.com/user-attachments/assets/c1b9ec6c-19ab-41fd-a34f-a924090e25b0)
