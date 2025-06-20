# -*- coding: utf-8 -*-
"""UAS ML PRAK_SKENARIO 1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13qN2U3PnOF7n_5lf7269Y7F6zX2i4aqs
"""

#-----UAS PEMBELAJARAN MESIN-----#
#BAGIAN 5 CLUSTERING

#SKENARIO PERTAMA

#Anggota:
#1. 187231035 / Nicco Cahya Permana
#2. 187231059 / Ahmad Mirza Rafiq Azmi
#3. 187231076 / I Nengah Sutha Dharmendra
#4. 187231081 / Rheinaldy Susanto

#-----UAS PEMBELAJARAN MESIN-----#

#-----Persiapan Tools-----#

# Install Tools yang Diperlukan
!pip install scikit-fuzzy

# Import Tools yang Diperlukan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from scipy import stats
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import skfuzzy as fuzz
from collections import Counter
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

#-----Persiapan Tools-----#

#-----Persiapan Dataset-----#

# Import Dataset Nanonano
df = pd.read_excel('Nanonano.xlsx')
df.head()

#-----Persiapan Dataset-----#

#-----Preprocessing Data-----#

# Melihat Bentuk Data
df.shape

# Melihat Ringkasan Statistik Data
df.describe()

# Memperbaiki Tipe Data Desimal
kolom_koma = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

for kolom in kolom_koma:
    df[kolom] = df[kolom].astype(str).str.replace(',', '.', regex=False).astype(float)

# Menampilakn Data Setelah Memperbaiki Tipe Data Desimal
df.head()

# Cek Missing Values Pada Data
df.isna().sum()

# Menangani Missing Values
# Karena tidak ada missing values maka tidak perlu dilakukan penanganan

# Cek Outlier Pada Data
kolom_numerik = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
z_scores = np.abs(stats.zscore(df[kolom_numerik]))
outliers_z = df[(z_scores > 3).any(axis=1)]
print("Outlier berdasarkan Z-score:\n", outliers_z)

# Menangani Outlier Dengan menghapusnya
df_cleaned = df[(z_scores <= 3).all(axis=1)].copy()
print("Dataset setelah menghapus outlier:\n", df_cleaned)

#-----Preprocessing Data-----#

#-----Encoding-----#

# Melakukan Encoding untuk Kolom Label
label_map = {
    'breakfast': 1,
    'lunch': 2,
    'snack': 3,
    'diner': 4
}
df_cleaned['L'] = df['L'].map(label_map)

# Menampilkan Data Setelah Encoding
print("Dataset setelah menghapus encoding:\n")
df_cleaned.head()

#-----Encoding-----#

#-----Normalisasi-----#

#Melakukan Normalisasi untuk Kolom Numerik (Kolom B - K) Mengggunakan Z-Score Normalization
kolom_fitur = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
scaler = StandardScaler()
df_cleaned[kolom_fitur] = scaler.fit_transform(df_cleaned[kolom_fitur])

print("Dataset setelah menghapus normalisasi:\n")
df_cleaned.head()

#-----Normalisasi-----#

#-----Elbow Method-----#

kolom_fitur = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

# 1. Cluster Optimal K-Means
# Elbow Method Untuk Mencari Cluster Optimal K-Means
X_all = df_cleaned[kolom_fitur].values
inertia = []
for n in range(1, 11):
    model = KMeans(
        n_clusters=n,
        init='k-means++',
        n_init=10,
        max_iter=300,
        random_state=111
    )
    model.fit(X_all)
    inertia.append(model.inertia_)
plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), inertia, 'o-')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.grid(True)
plt.show()

# Mengambil Jumlah Cluster Optimal Berdasarkan Elbow Method
cluster_optimal_kmeans = 2
print(f"Jumlah cluster optimal berdasarkan FPC: {cluster_optimal_kmeans}")

# 2. Cluster Optimal Fuzzy C-Means
# FCP Plot Untuk Mencari Cluster Optimal Fuzzy C-Means
n_clusters_range = range(2, 11)
fpcs = []

for n_clusters in n_clusters_range:
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        X_all.T,
        c=n_clusters,
        m=2,
        error=0.005,
        maxiter=1000,
        init=None
    )
    fpcs.append(fpc)
plt.figure(figsize=(10, 6))
plt.plot(n_clusters_range, fpcs, 'o-')
plt.xlabel('Number of Clusters')
plt.ylabel('Fuzzy Partition Coefficient (FPC)')
plt.title('FPC to Determine Optimal Number of Clusters (FCM)')
plt.grid(True)
plt.show()

# Mengambil jumlah cluster optimal berdasarkan FPC tertinggi
cluster_optimal_fcm = n_clusters_range[fpcs.index(max(fpcs))]
print(f"Jumlah cluster optimal berdasarkan FPC: {cluster_optimal_fcm}")

# 3. Cluster Optimal DBScan
# K-Distance Graph Untuk Menentukan Nilai Epsilon Optimal
neighbors = NearestNeighbors(n_neighbors=4)
neighbors_fit = neighbors.fit(X_all)
distances, indices = neighbors_fit.kneighbors(X_all)
distances = np.sort(distances[:, 3], axis=0)
plt.figure(figsize=(10, 6))
plt.plot(range(len(distances)), distances)
plt.xlabel('Points sorted by distance')
plt.ylabel('k-distance (k=4)')
plt.title('k-distance Graph for Optimal Epsilon Selection')
plt.grid(True)
plt.show()

# Menentukan nilai epsilon optimal dan minimal sample berdasarkan plot K-Distance
eps_optimal = 1.2
min_samples = 3
print(f"Parameter DBScan yang dipilih: eps={eps_optimal}, min_samples={min_samples}")

#-----Elbow Method-----#

#-----Clustering-----#

# 1. K-Means Clustering

# Membangun Algoritma KMeans
algorithm = KMeans(
    n_clusters=cluster_optimal_kmeans,
    init='k-means++',
    n_init=10,
    max_iter=300,
    tol=0.0001,
    random_state=111,
    algorithm='elkan'
)
labels2 = algorithm.fit_predict(X_all)
centroids2 = algorithm.cluster_centers_

# PCA untuk Mereduksi Fitur Ke 2 Dimensi
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_all)
centroids_pca = pca.transform(centroids2)

# Melihat Bentuk Visual Cluster K-Means
plt.figure(figsize=(15, 7))
colors = ['blue', 'orange', 'green', 'red', 'purple']

for j in range(cluster_optimal_kmeans):
    plt.scatter(
        X_pca[labels2 == j, 0],
        X_pca[labels2 == j, 1],
        c=colors[j],
        s=200,
        alpha=0.7,
        label=f'Cluster {j}'
    )

plt.scatter(
    centroids_pca[:, 0],
    centroids_pca[:, 1],
    s=300,
    c='red',
    marker='o',
    linewidths=3,
    label='Centroids'
)

plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('KMeans Clustering (Visualized with PCA)')
plt.legend()
plt.grid(True)
plt.show()

# Mendapatkan Nilai Silhouette Score K-Means
silhouette_kmeans = silhouette_score(X_all, labels2)
print(f"Silhouette Score K-Means: {silhouette_kmeans:.4f}")

# 2. Fuzzy C-Means Clustering

# PCA untuk Mereduksi Fitur Ke 2 Dimensi
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_all)

# Transpose Data Agar Sesuai Format Input skfuzzy
X_fuzzy = X_all.T

# Membangun Algoritma Fuzzy C-Means
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    X_fuzzy, c=2, m=2, error=0.005, maxiter=1000, init=None
)

# Mendapatkan Cluster Membership Berdasarkan Probabilitas Tertinggi
cluster_membership = np.argmax(u, axis=0)

# Menampilkan Cluster Fuzzy C-Means
plt.figure(figsize=(15, 7))
colors = ['blue', 'orange', 'green', 'red', 'purple']
for j in range(2):
    plt.scatter(X_pca[cluster_membership == j, 0],
                X_pca[cluster_membership == j, 1],
                c=colors[j], s=200, alpha=0.7, label=f'Cluster {j}')

# Menampilkan centroid Fuzzy C-Means dalam ruang PCA
cntr_pca = pca.transform(cntr)
plt.scatter(cntr_pca[:, 0], cntr_pca[:, 1],
            c='red', marker='o', s=300, linewidths=3, label='Centroids')

plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Fuzzy C-Means Clustering')
plt.legend()
plt.grid(True)
plt.show()

# Mendapatkan Nilai Silhouette Score Fuzzy C-Means
silhouette_fuzzy = silhouette_score(X_all, cluster_membership)
print(f"Silhouette Score Fuzzy C-Means: {silhouette_fuzzy:.4f}")

# PCA untuk mereduksi fitur ke 2 dimensi
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_all)

# Menjalankan DBSCAN
dbscan = DBSCAN(eps=eps_optimal, min_samples=min_samples)
dbscan_labels = dbscan.fit_predict(X_all)

# Menghitung jumlah cluster (tanpa noise)
n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise = list(dbscan_labels).count(-1)

print(f"Jumlah cluster DBSCAN: {n_clusters_dbscan}")
print(f"Jumlah noise points: {n_noise}")

# Visualisasi DBSCAN
plt.figure(figsize=(10, 6))
if -1 in dbscan_labels:
    plt.scatter(
        X_pca[dbscan_labels == -1, 0],
        X_pca[dbscan_labels == -1, 1],
        s=100,
        alpha=0.5,
        c='black',
        label='Noise'
    )
for i in set(dbscan_labels):
    if i != -1:
        plt.scatter(
            X_pca[dbscan_labels == i, 0],
            X_pca[dbscan_labels == i, 1],
            s=200,
            alpha=0.5,
            label=f'Cluster {i+1}'
        )
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.title(f'DBSCAN Clustering with PCA (eps={eps_optimal}, min_samples={min_samples})')
plt.legend()
plt.grid(True)
plt.show()

# Mendapatkan Nilai Silhouette Score DBSCAN (hanya jika ada cluster yang terbentuk)
if n_clusters_dbscan > 1:
    # Hanya hitung silhouette untuk non-noise points
    mask = dbscan_labels != -1
    if np.sum(mask) > 1:
        silhouette_dbscan = silhouette_score(X_all[mask], dbscan_labels[mask])
        print(f"Silhouette Score DBSCAN: {silhouette_dbscan:.4f}")
    else:
        print("DBSCAN: Tidak cukup data non-noise untuk menghitung silhouette score")
else:
    print("DBSCAN: Tidak ada cluster yang terbentuk")
    silhouette_dbscan = -1

#-----Clustering-----#

#-----Evaluasi (Silhouette Score)-----#
print(f"Silhouette Score K-Means Clustering: {silhouette_kmeans:.4f}")
print(f"Silhouette Score K-Means Fuzzy C-Means Clustering: {silhouette_fuzzy:.4f}")
print(f"Silhouette Score DBScan Clustering: {silhouette_dbscan:.4f}")

#-----Evaluasi (Silhouette Score)-----#

#-----Anggota Tiap cluster-----#

# 1. Anggota Cluster K-MeansClustering
print("Anggota Cluster K-Means Clustering:")
df_kmeans = df_cleaned.copy()
df_kmeans['KMeans_Cluster'] = labels2
kmeans_clusters = sorted(df_kmeans['KMeans_Cluster'].unique())
for cluster in kmeans_clusters:
  cluster_data = df_kmeans[df_kmeans['KMeans_Cluster'] == cluster]
  print(f"\n--- Cluster {cluster} ({len(cluster_data)} anggota) ---")
  print(cluster_data.head(5).to_string(index=False))

# 2. Anggota Cluster Fuzzy C-Means Clustering
print("Anggota Cluster Fuzzy C-Means Clustering:")
df_fuzzy = df_cleaned.copy()
df_fuzzy['Fuzzy_Cluster'] = cluster_membership
fuzzy_clusters = sorted(df_fuzzy['Fuzzy_Cluster'].unique())
for cluster in fuzzy_clusters:
  cluster_data = df_fuzzy[df_fuzzy['Fuzzy_Cluster'] == cluster]
  print(f"\n--- Cluster {cluster} ({len(cluster_data)} anggota) ---")
  print(cluster_data.head(5).to_string(index=False))

# 3. Anggota Cluster DBScan Clustering
print("Anggota Cluster Fuzzy DBScan Clustering:")
df_dbscan = df_cleaned.copy()
df_dbscan['DBSCAN_Cluster'] = dbscan_labels
if -1 in df_dbscan['DBSCAN_Cluster'].values:
  noise_data = df_dbscan[df_dbscan['DBSCAN_Cluster'] == -1]
  print(f"\n--- Noise Points ({len(noise_data)} anggota) ---")
  print(noise_data.head(5).to_string(index=False))
  print("... (data lengkap ada di file CSV)")
  regular_clusters = [c for c in df_dbscan['DBSCAN_Cluster'].unique() if c != -1]
if regular_clusters:
  for cluster in sorted(regular_clusters):
    cluster_data = df_dbscan[df_dbscan['DBSCAN_Cluster'] == cluster]
    print(f"\n--- Cluster {cluster} ({len(cluster_data)} anggota) ---")
    print(cluster_data.head(5).to_string(index=False))
    print("... (data lengkap ada di file CSV)")
  else:
    print("\nTidak ada cluster yang terbentuk (semua data adalah noise)")

#-----Anggota Tiap cluster-----#

#-----Beri Label Pada Data Cluster-----#

print("Label Clustering Untuk Dataset:")
final_df = df_cleaned.copy()
final_df['KMeans_Cluster'] = labels2
final_df['Fuzzy_Cluster'] = cluster_membership
final_df['DBSCAN_Cluster'] = dbscan_labels
print(final_df.head(5).to_string(index=False))

#-----Beri Label Pada Data Cluster-----#