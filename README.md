# 📊 UAS Pembelajaran Mesin - Clustering Project

## 📚 Deskripsi
Proyek ini merupakan bagian dari Ujian Akhir Semester (UAS) mata kuliah **Pembelajaran Mesin** yang dilakukan oleh satu kelompok. Fokus utama proyek ini adalah implementasi **algoritma clustering** untuk melakukan segmentasi data secara tidak terawasi (unsupervised learning).

Kami menggunakan tiga metode clustering:
- **K-Means**
- **Fuzzy C-Means**
- **DBSCAN**

Eksperimen dilakukan dalam dua skenario:
1. **Skenario 1:** Tanpa seleksi/ekstraksi fitur.
2. **Skenario 2:** Dengan seleksi fitur menggunakan **Linear Discriminant Analysis (LDA)**.

Evaluasi performa dilakukan menggunakan **Silhouette Score**.

---

## 👥 Anggota Kelompok
| NIM        | Nama                         |
|------------|------------------------------|
| 187231035  | Nicco Cahya Permana          |
| 187231059  | Ahmad Mirza Rafiq Azmi       |
| 187231076  | I Nengah Sutha Dharmendra    |
| 187231081  | Rheinaldy Susanto            |

---

## 🛠️ Tahapan Proyek

### 1. Input Dataset
- Dataset yang digunakan: `Nanonao`

### 2. Preprocessing Data
- Cek **missing value** dan **outlier**
- **Encoding** variabel kategorikal
- **Normalisasi** data numerik

### 3. Penentuan Jumlah Cluster
- Menggunakan metode **Elbow** pada K-Means

---

## ⚙️ Skenario 1: Tanpa Seleksi Fitur

### 4. Clustering
- K-Means
- Fuzzy C-Means
- DBSCAN

### 5. Evaluasi
- Menggunakan **Silhouette Score**

### 6. Output
- Menampilkan anggota tiap-tiap cluster
- Memberikan label klaster pada data

---

## ⚙️ Skenario 2: Dengan Seleksi Fitur (LDA)

### 4. Seleksi/Ekstraksi Fitur
- Menggunakan **Linear Discriminant Analysis (LDA)**

### 5. Clustering
- K-Means
- Fuzzy C-Means
- DBSCAN

### 6. Evaluasi
- Menggunakan **Silhouette Score**

### 7. Output
- Menampilkan anggota tiap-tiap cluster
- Memberikan label klaster pada data

---

## 📈 Evaluasi
- Visualisasi hasil clustering dengan **plot 2D/3D**
- Perbandingan performa algoritma berdasarkan nilai **Silhouette Score**

---

## 📦 Cara Menjalankan Proyek

1. Clone repository ini:
   ```bash
   git clone https://github.com/username/nanonao-clustering.git
   cd nanonao-clustering
