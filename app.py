import streamlit as st
import joblib
import pandas as pd
import os

# Inisialisasi session
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Soal pilihan ganda
soal_pilgan = [
    {
        "soal": "1. Sari, Budi, Citra, Doni, dan Eka bermain Cublak-Cublak Suweng. Setelah hompimpa, Sari menjadi penebak dan duduk tengkurap di tengah, sedangkan 4 temannya duduk melingkar. Jika Sari menebak secara acak, berapakah peluang tebakannya benar?",
        "opsi": ["A. 1/4", "B. 1/5", "C. 1/3", "D. 1/2"],
        "jawaban": "B"
    },
    {
        "soal": "2. Ada sekelompok anak kecil terdiri dari 8 orang: Maya, Fajar, Lia, Riko, Arif, Bayu, Fito, dan Davin. Mereka hendak bermain “Cublak-cublak Suweng”. Untuk menentukan 1 orang yang tengkurap sebagai penebak batu/kecik, mereka melakukan hompimpa. Tentukan peluang kejadian bahwa Riko akan terpilih sebagai orang yang tengkurap!",
        "opsi": ["A. 2/8", "B. 0", "C. 1/8", "D. 1/6"],
        "jawaban": "C"
    },
    {
        "soal": "3. Dalam permainan Cublak-cublak Suweng yang dimainkan oleh 6 anak, 1 anak tengkurap menebak siapa yang menyembunyikan batu. Jika ia menebak salah, ia kalah. Tentukan peluang anak yang tengkurap kalah!",
        "opsi": ["A. 1/6", "B. 2/5", "C. 1/2", "D. 4/5"],
        "jawaban": "D"
    },
    {
        "soal": "4. Jika sebuah kotak berisi 6 bola merah, 2 bola biru, dan 4 bola hijau, berapakah peluang diambilnya bola biru atau hijau?",
        "opsi": ["A. 1/3", "B. 1/4", "C. 5/12", "D. 1/2"],
        "jawaban": "D"
    },
    {
        "soal": "5. Dalam sebuah undian terdapat 10 tiket, di mana 3 tiket adalah pemenang. Jika satu tiket diambil secara acak, berapakah peluang tiket yang diambil adalah tiket pemenang?",
        "opsi": ["A. 3/10", "B. 1/3", "C. 2/5", "D. 1/2"],
        "jawaban": "A"
    }
]

# ================= HEADER =================
st.set_page_config(page_title="Kuis Etnomatematika", page_icon="🎓")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Wayang_Kulit_-_Museum_Sonobudoyo.jpg/640px-Wayang_Kulit_-_Museum_Sonobudoyo.jpg", use_column_width=True)
st.markdown("## 🎭 Kuis Etnomatematika: Cublak-Cublak Suweng")
st.caption("📚 Materi: Peluang - Konteks Budaya Jawa (Kegiatan 2)")

# ================= FORM INPUT NAMA =================
nama = st.text_input("Masukkan nama kamu:")

if nama:
    with st.form("kuis_form"):
        st.subheader("📋 Soal Pilihan Ganda")
        jawaban_siswa = []
        for i, soal in enumerate(soal_pilgan):
            pilihan = st.radio(soal["soal"], soal["opsi"], key=f"soal_{i}")
            jawaban_siswa.append(pilihan)
        submit = st.form_submit_button("✅ Kirim Jawaban")

    if submit:
        st.session_state.submitted = True
        benar = 0
        pembahasan = []

        for i, soal in enumerate(soal_pilgan):
            jawaban_user = jawaban_siswa[i][0]  # A/B/C/D
            kunci = soal["jawaban"]
            if jawaban_user == kunci:
                benar += 1
                pembahasan.append(f"✅ Soal {i+1}: Benar")
            else:
                pembahasan.append(f"❌ Soal {i+1}: Salah. Jawaban benar: {kunci}")

        nilai = int((benar / len(soal_pilgan)) * 100)

        # ================= ANIMASI =================
        if nilai == 100:
            st.balloons()
        elif nilai >= 80:
            st.snow()

        # ================= FEEDBACK =================
        st.success(f"🎉 {nama}, kamu menjawab benar {benar} dari {len(soal_pilgan)} soal.")
        st.info(f"📊 Nilai akhir kamu: {nilai}/100")

        with st.expander("🔍 Lihat Pembahasan"):
            for p in pembahasan:
                st.write(p)

        # ================= SIMPAN .PKL =================
        hasil = {
            "nama": nama,
            "skor": nilai,
            "jawaban_benar": benar,
            "jumlah_soal": len(soal_pilgan),
            "jawaban_siswa": jawaban_siswa
        }
        joblib.dump(hasil, "hasil_kuis2.pkl")
        with open("hasil_kuis2.pkl", "rb") as f:
            st.download_button("📥 Unduh Hasil Individu (.pkl)", data=f, file_name="hasil_kuis2.pkl")

        # ================= REKAP .CSV =================
        csv_file = "rekap_nilai.csv"
        if not os.path.exists(csv_file):
            df_init = pd.DataFrame(columns=["Nama", "Skor", "Benar", "Total", "Jawaban"])
            df_init.to_csv(csv_file, index=False)

        # Tambahkan ke CSV
        data = pd.read_csv(csv_file)
        data.loc[len(data)] = [nama, nilai, benar, len(soal_pilgan), str(jawaban_siswa)]
        data.to_csv(csv_file, index=False)

        # Tombol download CSV
        with open(csv_file, "rb") as f:
            st.download_button("📄 Unduh Rekap Semua Siswa (.csv)", data=f, file_name="rekap_nilai.csv")
