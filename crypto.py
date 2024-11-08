import streamlit as st 
import base64
from math import gcd

def find_e(phi_n):
    # Mulai dengan nilai umum yang sering dipakai untuk e (misalnya 3, 5, 17, atau 65537)
    # Coba angka kecil terlebih dahulu karena lebih efisien
    candidates = [3, 5, 17, 65537]
    
    # Cek kandidat pertama
    for e in candidates:
        if e < phi_n and gcd(e, phi_n) == 1:
            return e
    
    # Jika kandidat umum tidak valid, cari nilai e lainnya dari 2 ke atas
    for e in range(2, phi_n):
        if gcd(e, phi_n) == 1:
            return e

def find_d(e, phi_n):
    # Extended Euclidean Algorithm untuk menemukan d
    t, new_t = 0, 1
    r, new_r = phi_n, e
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    # Pastikan d adalah nilai positif
    if t < 0:
        t += phi_n
    return t

# Konversi karakter ke integer berdasarkan urutan ASCII
def text_to_int(text):
    return [ord(char) for char in text]

# Konversi integer kembali ke karakter teks
def int_to_text(integers):
    return ''.join(chr(i) for i in integers)

# Fungsi enkripsi menggunakan (n, e)
def encrypt_rsa(plaintext, n, e):
    plaintext_int = text_to_int(plaintext)
    encrypted_int = [(char ** e) % n for char in plaintext_int]
    # Gabungkan hasil enkripsi sebagai string dan ubah ke bytes untuk Base64
    encrypted_str = ','.join(map(str, encrypted_int))
    encrypted_base64 = base64.b64encode(encrypted_str.encode()).decode('utf-8')
    return encrypted_base64

# Fungsi dekripsi menggunakan (n, d)
def decrypt_rsa(encrypted_base64, n, d):
    # Decode dari Base64 ke string, lalu pisahkan menjadi list angka
    encrypted_str = base64.b64decode(encrypted_base64).decode('utf-8')
    encrypted_int = list(map(int, encrypted_str.split(',')))
    decrypted_int = [(char ** d) % n for char in encrypted_int]
    return int_to_text(decrypted_int)

# Nilai-nilai RSA yang diberikan
a = 61
b = 79
n = a * b 
phi_n = (a - 1) * (b - 1) 
e = find_e(phi_n)
print("Nilai e = ", e)
d = find_d(e, phi_n)
print("Nilai d = ", d)

# Tampilan aplikasi
st.title("Enkripsi dan Dekripsi RSA dengan Streamlit")

st.write("""
Aplikasi ini menggunakan algoritma RSA untuk mengenkripsi dan mendekripsi teks.
Anda bisa memasukkan teks untuk dienkripsi atau teks terenkripsi untuk didekripsi secara langsung.
""")

# Input untuk Enkripsi
st.header("Enkripsi")
plaintext = st.text_input("Masukkan teks untuk dienkripsi:")
if plaintext:
    # Enkripsi plaintext
    encrypted_message = encrypt_rsa(plaintext, n, e)
    st.write("Hasil Enkripsi (Base64):", encrypted_message)

# Input untuk Dekripsi
st.header("Dekripsi")
encrypted_base64 = st.text_input("Masukkan teks terenkripsi dalam Base64:")
d_input = st.text_input("Masukkan nilai d (private key):")

# Konversi input d ke integer jika tersedia
if encrypted_base64 and d_input.isdigit():
    d = int(d_input)
    try:
        # Dekripsi ciphertext
        decrypted_message = decrypt_rsa(encrypted_base64, n, d)
        st.write("Hasil Dekripsi:", decrypted_message)
    except Exception as e:
        st.error("Gagal mendekripsi teks. Pastikan teks terenkripsi benar, dalam format Base64, dan nilai d valid.")
else:
    if encrypted_base64:
        st.error("Masukkan nilai d yang valid untuk dekripsi.")
