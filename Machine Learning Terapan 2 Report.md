# Laporan Proyek Machine Learning - Muhammad Zaki Fuadi
## _Submission Kedua_

Proyek ini bertujuan untuk menentukan rekomendasi film dari seorang user dengan menggunakan collaborative filtering, metode ini memberikan skor untuk setiap film berdasarkan tingkat kemiripannya dengan preferensi pengguna dan merekomendasikan film dengan skor tertinggi. Dalam praktiknya, metode ini sering digunakan di platform streaming film untuk memberikan rekomendasi yang personal dan relevan kepada setiap pengguna, subjek pada proyek ini adalah seorang yang menonton film kemudian memberikan rating. 

## Domain Proyek

> Sistem rekomendasi film memungkinkan pengguna menemukan film yang sesuai dengan preferensi mereka dengan lebih cepat dan mudah, meningkatkan pengalaman menonton mereka.[1].
> Meningkatkan keterlibatan pengguna: Ketika pengguna menemukan film yang mereka sukai, mereka cenderung menghabiskan lebih banyak waktu menonton dan mengeksplorasi film lain di platform tersebut. Menurut sebuah studi oleh Netflix, 75% dari semua tontonan di platform mereka berasal dari rekomendasi[2].
> Meningkatkan pendapatan: Dengan memperbaiki pengalaman pengguna dan meningkatkan keterlibatan, sistem rekomendasi film juga dapat meningkatkan pendapatan. Sebuah studi oleh Deloitte menunjukkan bahwa, dengan menggunakan sistem rekomendasi, penjualan produk dapat meningkat hingga 60%[3].

## Business Understanding
### - Problem Statement
- Bagaimana cara memberikan rekomendasi film yang tepat pada penonton ?
- Apa strategi yang efektif untuk memperkuat loyalitas penonton ?

### - Goals
- Membangun model rekomendasi yang akurat, dengan memiliki model prediksi yang akurat, sehingga perusahaan dapat menyediakan rekomendasi film yang lebih akurat dan relevan kepada setiap pengguna, meningkatkan pengalaman pengguna dan keterlibatan.
- Menentukan strategi yang efektif untuk memperkuat loyalitas penonton, dengan mmemperkenalkan fitur personalisasi lainnya seperti daftar tontonan, rekomendasi film berdasarkan genre atau sutradara favorit, dan pemberitahuan film baru yang diunggulkan oleh pengguna.

### - Solution Statement
- Menggunakan metode collaborative filtering dapat menemukan film yang sesuai dengan preferensi film berdasarkan rating yang diberikan.

## Data Understanding

Dataset didapat pada [kaggle]  (https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset)

Selanjutnya uraikanlah seluruh variabel atau fitur pada data. Sebagai contoh:  

#### Tabel Rating 

| Informasi | Penjelasan |
| ------ | ------ |
| Jumlah Baris | 20000262 |
| Jumlah Kolom | 4 |
| Missing Value | 0 |

Keterangan kolom data :

| Nama | Keterangan |
| ------ | ------ |
| userId | ID User |
| movieId | ID Film |
| rating | Rating Film |
| timestamp | Waktu diberikan Rating |

#### Tabel Movie

| Informasi | Penjelasan |
| ------ | ------ |
| Jumlah Baris | 27277 |
| Jumlah Kolom | 3 |
| Missing Value | 0 |

Keterangan kolom data :

| Nama | Keterangan |
| ------ | ------ |
| movieId | ID Film |
| title | Judul Film |
| genre | Genre Film |

Dikarenakan data yang diambil data user, film dan ratingnya, hanya melihat apakah ada nilai missing value, namun pada dataset tidak ada missing value.

## Data Preparation
Pada bagian ini Anda menerapkan dan menyebutkan teknik data preparation yang dilakukan. 

- Menerapkan dan menyebutkan teknik data preparation yang dilakukan. (downsampling, encoding)
- Downsampling adalah suatu teknik untuk mengurangi jumlah data dalam sebuah sistem atau model. Teknik ini dilakukan dengan mengambil sampel dari dataset yang lebih besar sehingga ukurannya menjadi lebih kecil. Tujuan dari downsampling adalah untuk meningkatkan efisiensi dan kinerja model, serta mengurangi kompleksitas dan biaya pengolahan data. Melakukan downsampling pada data rating, yaitu dengan memilih hanya user yang memberikan rating pada lebih dari 2000 film dan mengambil data dengan rating tertinggi hingga urutan ke-50 saja yang akan dipertahankan.
- Encoding adalah suatu teknik untuk mewakili data dalam bentuk yang dapat diproses oleh suatu sistem atau model. Encoding dilakukan dengan mengubah data mentah ke dalam format numerik atau kategorikal yang dapat diinterpretasikan oleh mesin. Dilakukan encoding pada kolom 'userId' dan 'movieId' ke dalam indeks integer. Awalnya mengambil setiap nilai unik dari kolom 'userId' pada dataframe 'preparation', kemudian mengubahnya menjadi list kemudian, mengambil setiap nilai unik dari kolom 'userId' pada dataframe 'preparation', kemudian mengubahnya menjadi list dengan mengambil setiap nilai unik dari kolom 'userId' pada dataframe 'preparation', kemudian mengubahnya menjadi list.
- Pembagian dataset training dan dataset validasi yaitu 80% banding 20% untuk mempercepat proses mesin belajar dan evaluasi model.

![1](https://user-images.githubusercontent.com/70827786/236629108-548bb301-3508-4021-bc29-7b38f6435ad8.png)
Gambar 1. Heatmap dataset movie_details

> Dilihat masing-masing variabel memiliki korelasi positif, namun lemah.

## Data Modelling and Result

Model menggunakan collaboration filtering, karena di dataset hanya ada nilai rating dari user untuk menentukan sistem rekomendasi. 

> Tujuan proyek ini menghasilkan rekomendasi sejumlah film yang sesuai dengan preferensi pengguna berdasarkan rating yang telah diberikan sebelumnya. Dari data rating pengguna, kita akan mengidentifikasi film-film yang mirip dan belum pernah dikunjungi oleh pengguna untuk direkomendasikan. Pada kasus ini, menggunakan teknik collaborative filtering untuk membuat sistem rekomendasi.
> Teknik collaborative filtering untuk merekomendasikan film kepada pengguna berdasarkan preferensi film dari pengguna lain yang memiliki preferensi serupa. Collaborative filtering bekerja dengan mencari pola dalam preferensi pengguna untuk item tertentu (dalam kasus ini film) dan mencari pengguna lain yang memiliki pola preferensi serupa untuk merekomendasikan item kepada pengguna yang sedang dicari rekomendasinya. Dalam proyek ini, kita menggunakan data rating yang diberikan oleh pengguna untuk mengidentifikasi pola dan merekomendasikan film berdasarkan pola tersebut.
> Pada proses training, model menghitung skor kecocokan antara pengguna dan film dengan teknik embedding. Pertama, kita melakukan proses embedding terhadap data user dan film. Selanjutnya, lakukan operasi perkalian dot product antara embedding user dan film. Selain itu, kita juga dapat menambahkan bias untuk setiap user dan film. Skor kecocokan ditetapkan dalam skala [0,1] dengan fungsi aktivasi sigmoid.
> Selanjutnya, lakukan proses compile terhadap model. Model ini menggunakan Binary Crossentropy untuk menghitung loss function, Adam (Adaptive Moment Estimation) sebagai optimizer, dan root mean squared error (RMSE) sebagai metrics evaluation.
> Model yang dihasilkan akan dilatih menggunakan data latih (x_train dan y_train) dengan menggunakan stokastik gradient descent sebagai optimizer. Proses training akan dilakukan selama 20 epoch atau iterasi dengan setiap batch yang terdiri dari 8 sampel.
> Berikutnya Top-N recommendation sebagai output dari sistem rekomendasi collaboration filtering ini yang menyajikan daftar N item teratas yang direkomendasikan untuk pengguna berdasarkan preferensi dan perilaku pengguna serta informasi dari item-item yang telah diberi rating oleh pengguna lain. > 
> Untuk mendapatkan rekomendasi film, pertama kita ambil sampel user secara acak dan definisikan variabel film_not_watched yang merupakan daftar film yang belum pernah dikunjungi oleh pengguna. Kita menggunakan rating ini untuk membuat rekomendasi film yang mungkin cocok untuk pengguna. Nah, film yang akan direkomendasikan tentulah film yang belum pernah dikunjungi oleh pengguna. Oleh karena itu, kita perlu membuat variabel film_not_visited sebagai daftar film untuk direkomendasikan pada pengguna.

Sebagai contoh, hasil di atas adalah rekomendasi untuk user dengan id 67443. Dari output tersebut, kita dapat membandingkan antara film with high ratings from user dan Top 10 film recommendation untuk user. 

![Screenshot 2023-05-06 143957](https://user-images.githubusercontent.com/70827786/236629267-55d9e793-d266-4343-9989-65d156dc6a14.png)
Gambar 2. Top N Rekomendasi film pada user.

Pada Gambar 2. Perhatikanlah, beberapa film rekomendasi menyediakan genres yang sesuai dengan rating user. Kita memperoleh 4 rekomendasi film dengan genres Drama, 1 rekomendasi film dengan genres Documentary/War. Ada 10 rekomendasi film untuk pengguna agar pengguna tidak bingung dan memilih untuk menonton film tersebut, dan meminimalisir kekecewaan pengguna pada sistem rekomendasi ini.

## Evaluation

Pada hasil evaluasi memiih kasus rekomendasi sistem (Top N) dan menggunakan collaborative filtering. Berikut metrik penjelasan evaluasinya :

Dalam konteks top-N recommendation dan collaborative rating, RMSE dapat digunakan untuk mengevaluasi performa model dalam memberikan prediksi rating untuk item yang belum pernah dilihat oleh pengguna. Semakin rendah nilai RMSE, semakin baik performa model dalam merekomendasikan item yang relevan dan disukai oleh pengguna. Oleh karena itu, evaluasi dengan menggunakan RMSE sangat penting dalam memperbaiki kualitas rekomendasi pada sistem rekomendasi collaborative filtering.

![2](https://user-images.githubusercontent.com/70827786/236631054-a3870425-ee74-49b2-b4f4-c4894703b99a.png)
Gambar 3. Visualisasi training dan validasi dataset

Pada gambar 3. proses training model cukup smooth dan model konvergen pada epochs sekitar 20. Dari proses ini, kita memperoleh nilai error(RMSE) sebesar sekitar 0.16 dan error pada data validasi sebesar 0.17 . Nilai tersebut cukup bagus untuk sistem rekomendasi.

## Conclusion

> Dari proyek ini, dapat disimpulkan bahwa sistem rekomendasi menggunakan collaborative filtering dapat digunakan untuk merekomendasikan item-item yang relevan dan disukai oleh pengguna. Model ini menggunakan collaborative filtering untuk merekomendasikan film berdasarkan rating pengguna. Proses training menggunakan teknik embedding dan dot product, dan hasilnya dinilai dengan Binary Crossentropy dan RMSE. Dari evaluasi dengan RMSE, model ini cukup baik dalam merekomendasikan film dengan nilai RMSE sekitar 0.16. Top N recommendation digunakan untuk menyajikan daftar N item teratas yang direkomendasikan untuk pengguna. Evaluasi model dilakukan dengan melihat visualisasi training dan validasi dataset.

## REFERENCES
[1] McKinsey & Company. (2019). Personalization is not a product. Dikutip dari https://www.mckinsey.com/business-functions/marketing-and-sales/our-insights/personalization-is-not-a-product
[2] Netflix. (2017). Netflix launches new feature for better recommendations, dikutip dari https://media.netflix.com/en/press-releases/netflix-launches-new-feature-for-better-recommendations
[3] Deloitte. (2017). Machine learning unlocks the true potential of personalization, dikutip dari https://www2.deloitte.com/us/en/insights/industry/retail-distribution/machine-learning-retail-personalization.html
