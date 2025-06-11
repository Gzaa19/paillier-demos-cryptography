"""
PAILLIER CORE - Implementasi Inti Algoritma Paillier Cryptosystem
================================================================

File ini berisi implementasi core dari algoritma Paillier tanpa demo atau testing.
Fokus pada algoritma murni dengan penjelasan matematika yang detail.

Author: Gaza Al Ghozali Chansa
Date: 2025
License: MIT
"""

import random
import math
from typing import Tuple, Optional


class PaillierCore:
    """
    Implementasi inti algoritma Paillier Cryptosystem.
    
    Algoritma Paillier adalah sistem kriptografi kunci publik yang memiliki
    sifat additive homomorphic, memungkinkan operasi penjumlahan pada data
    terenkripsi tanpa perlu mendekripsi terlebih dahulu.
    
    Mathematical Foundation:
    - Keamanan berdasarkan Composite Residuosity Problem
    - Operasi dilakukan dalam grup Z*_{n²}
    - Homomorphic property: E(m₁) x E(m₂) = E(m₁ + m₂)
    
    Attributes:
        bit_length (int): Panjang bit kunci (default: 2048)
        public_key (dict): Kunci publik {n, g}
        private_key (dict): Kunci privat {lambda, mu, n}
        n_squared (int): Nilai n² untuk optimisasi
    """
    
    def __init__(self, bit_length: int = 2048):
        """
        Inisialisasi Paillier Cryptosystem.
        
        Args:
            bit_length: Panjang bit untuk bilangan prima p dan q.
                       Total ukuran n akan menjadi 2 × bit_length.
                       Rekomendasi: 1024 (testing), 2048 (production), 
                       3072+ (high security)
        """
        if bit_length < 512:
            raise ValueError("Bit length minimal 512 untuk keamanan dasar")
        
        self.bit_length = bit_length
        self.public_key = None
        self.private_key = None
        self.n_squared = None
        
        # Generate keypair saat inisialisasi
        self._generate_keypair()
    
    def _miller_rabin_test(self, n: int, rounds: int = 10) -> bool:
        """
        Miller-Rabin Primality Test - Algoritma probabilistik untuk test prima.
        
        Algoritma ini berdasarkan Fermat's Little Theorem dan properti dari
        quadratic residues. Dengan k rounds, probabilitas error adalah (1/4)^k.
        
        Mathematical Background:
        - Jika n prima dan a^(n-1) ≡ 1 (mod n), maka untuk n-1 = d×2^r,
          sequence a^d, a^(2d), a^(4d), ..., a^((2^(r-1))d) mod n
          harus berakhir dengan 1, dan elemen sebelum 1 harus -1.
        
        Args:
            n: Bilangan yang akan ditest
            rounds: Jumlah test rounds (default: 10, error prob < 10^-6)
            
        Returns:
            True jika n kemungkinan besar prima, False jika komposit
        """
        # Handle edge cases
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        
        # Tulis n-1 = d × 2^r dengan d ganjil
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Lakukan rounds test
        for _ in range(rounds):
            # Pilih witness a secara random
            a = random.randrange(2, n - 1)
            
            # Hitung a^d mod n
            x = pow(a, d, n)
            
            # Jika x ≡ 1 atau x ≡ -1 (mod n), lanjut ke round berikutnya
            if x == 1 or x == n - 1:
                continue
            
            # Square x sebanyak r-1 kali
            composite_found = True
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    composite_found = False
                    break
            
            # Jika tidak pernah mendapat -1, maka n komposit
            if composite_found:
                return False
        
        return True
    
    def _generate_prime(self, bit_length: int) -> int:
        """
        Generate bilangan prima dengan panjang bit tertentu.
        
        Menggunakan pendekatan generate-and-test:
        1. Generate random odd number dengan bit length yang tepat
        2. Test primality menggunakan Miller-Rabin
        3. Jika tidak prima, coba bilangan ganjil berikutnya
        
        Optimisasi:
        - Set bit tertinggi untuk memastikan exact bit length
        - Set bit terendah untuk memastikan bilangan ganjil
        - Skip bilangan yang divisible oleh small primes
        
        Args:
            bit_length: Panjang bit prima yang diinginkan
            
        Returns:
            Bilangan prima dengan bit length yang diminta
        """
        while True:
            # Generate candidate dengan bit length yang tepat
            candidate = random.getrandbits(bit_length)
            
            # Set bit tertinggi (MSB) untuk memastikan exact bit length
            candidate |= (1 << (bit_length - 1))
            
            # Set bit terendah (LSB) untuk memastikan ganjil
            candidate |= 1
            
            # Quick check: skip jika divisible by small primes
            small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
            if any(candidate % p == 0 for p in small_primes if candidate != p):
                continue
            
            # Test primality dengan Miller-Rabin
            if self._miller_rabin_test(candidate):
                return candidate
    
    def _compute_lcm(self, a: int, b: int) -> int:
        """
        Compute Least Common Multiple menggunakan formula LCM(a,b) = |ab|/GCD(a,b).
        
        LCM diperlukan untuk menghitung λ = lcm(p-1, q-1) dalam key generation.
        
        Args:
            a, b: Dua bilangan integer
            
        Returns:
            LCM dari a dan b
        """
        return abs(a * b) // math.gcd(a, b)
    
    def _extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm untuk menghitung GCD dan koefisien Bézout.
        
        Mengembalikan (gcd, x, y) sedemikian hingga ax + by = gcd(a, b).
        Digunakan untuk menghitung modular inverse.
        
        Args:
            a, b: Dua bilangan integer
            
        Returns:
            Tuple (gcd, x, y) dimana ax + by = gcd
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    def _modular_inverse(self, a: int, m: int) -> int:
        """
        Hitung modular multiplicative inverse dari a modulo m.
        
        Mencari x sedemikian hingga a x x ≡ 1 (mod m).
        Inverse ada jika dan hanya jika gcd(a, m) = 1.
        
        Args:
            a: Bilangan yang akan dicari inversenya
            m: Modulus
            
        Returns:
            Modular inverse dari a mod m
            
        Raises:
            ValueError: Jika modular inverse tidak ada
        """
        gcd, x, _ = self._extended_gcd(a % m, m)
        
        if gcd != 1:
            raise ValueError(f"Modular inverse dari {a} mod {m} tidak ada (gcd = {gcd})")
        
        return (x % m + m) % m
    
    def _generate_keypair(self) -> None:
        """
        Generate pasangan kunci publik dan privat untuk Paillier Cryptosystem.
        
        Key Generation Algorithm:
        1. Pilih dua bilangan prima p, q dengan ukuran bit_length/2
        2. Hitung n = p × q
        3. Hitung λ = lcm(p-1, q-1)
        4. Pilih g = n + 1 (untuk efisiensi, memenuhi kondisi keamanan)
        5. Hitung μ = λ^(-1) mod n
        6. Public key: (n, g), Private key: (λ, μ)
        
        Security Requirements:
        - p ≠ q (untuk mencegah trivial factorization)
        - gcd(pq, (p-1)(q-1)) = 1 (dipenuhi otomatis jika p, q prima)
        - g harus generate subgroup yang tepat (dipenuhi dengan g = n + 1)
        """
        # Step 1: Generate dua bilangan prima p dan q
        p = self._generate_prime(self.bit_length // 2)
        q = self._generate_prime(self.bit_length // 2)
        
        # Pastikan p ≠ q
        while p == q:
            q = self._generate_prime(self.bit_length // 2)
        
        # Step 2: Hitung n = p × q
        n = p * q
        self.n_squared = n * n
        
        # Step 3: Hitung λ = lcm(p-1, q-1)
        lambda_n = self._compute_lcm(p - 1, q - 1)
        
        # Step 4: Pilih generator g
        # Menggunakan g = n + 1 untuk efisiensi dan keamanan
        # Properti: L(g^λ mod n²) = λ, sehingga μ = λ^(-1) mod n
        g = n + 1
        
        # Step 5: Hitung μ = λ^(-1) mod n
        mu = self._modular_inverse(lambda_n, n)
        
        # Step 6: Simpan kunci
        self.public_key = {'n': n, 'g': g}
        self.private_key = {'lambda': lambda_n, 'mu': mu, 'n': n}
    
    def _L_function(self, x: int) -> int:
        """
        Fungsi L(x) = (x-1)/n yang digunakan dalam dekripsi.
        
        Fungsi ini well-defined karena dalam konteks Paillier,
        x selalu berbentuk 1 + k×n untuk beberapa integer k.
        
        Args:
            x: Input untuk fungsi L (harus ≡ 1 mod n)
            
        Returns:
            (x-1)/n
        """
        return (x - 1) // self.public_key['n']
    
    def encrypt(self, plaintext: int) -> int:
        """
        Enkripsi plaintext menggunakan Paillier algorithm.
        
        Encryption Formula: c = g^m × r^n mod n²
        
        Dimana:
        - m adalah plaintext (0 ≤ m < n)
        - r adalah bilangan acak (1 ≤ r < n, gcd(r,n) = 1)
        - c adalah ciphertext
        
        Probabilistic Property:
        Setiap enkripsi menghasilkan ciphertext yang berbeda karena
        randomness r yang berbeda, memberikan semantic security.
        
        Args:
            plaintext: Pesan yang akan dienkripsi (integer, 0 ≤ m < n)
            
        Returns:
            Ciphertext sebagai integer
            
        Raises:
            ValueError: Jika plaintext invalid atau kunci belum ada
        """
        if self.public_key is None:
            raise ValueError("Kunci publik belum dibuat")
        
        n = self.public_key['n']
        g = self.public_key['g']
        
        # Validasi input
        if not isinstance(plaintext, int) or plaintext < 0:
            raise ValueError("Plaintext harus bilangan non-negatif")
        
        if plaintext >= n:
            raise ValueError(f"Plaintext ({plaintext}) harus < n ({n})")
        
        # Generate randomness r
        # r harus coprime dengan n untuk memastikan r^n invertible mod n²
        while True:
            r = random.randrange(1, n)
            if math.gcd(r, n) == 1:
                break
        
        # Hitung ciphertext: c = g^m × r^n mod n²
        # Menggunakan modular exponentiation untuk efisiensi
        g_power_m = pow(g, plaintext, self.n_squared)
        r_power_n = pow(r, n, self.n_squared)
        ciphertext = (g_power_m * r_power_n) % self.n_squared
        
        return ciphertext
    
    def decrypt(self, ciphertext: int) -> int:
        """
        Dekripsi ciphertext menggunakan private key.
        
        Decryption Formula: m = L(c^λ mod n²) × μ mod n
        
        Dimana:
        - c adalah ciphertext
        - λ adalah lambda dari private key
        - μ adalah mu dari private key
        - m adalah plaintext hasil dekripsi
        
        Mathematical Correctness:
        Untuk ciphertext valid c = g^m × r^n mod n²:
        c^λ ≡ g^(mλ) × r^(nλ) ≡ g^(mλ) × 1 ≡ g^(mλ) (mod n²)
        Dengan g = n + 1: g^(mλ) ≡ 1 + mλn (mod n²)
        Sehingga L(c^λ mod n²) = mλ, dan mλμ ≡ m (mod n)
        
        Args:
            ciphertext: Pesan terenkripsi yang akan didekripsi
            
        Returns:
            Plaintext asli sebagai integer
            
        Raises:
            ValueError: Jika private key tidak tersedia
        """
        if self.private_key is None:
            raise ValueError("Private key tidak tersedia")
        
        lambda_n = self.private_key['lambda']
        mu = self.private_key['mu']
        n = self.private_key['n']
        
        # Hitung c^λ mod n²
        c_lambda = pow(ciphertext, lambda_n, self.n_squared)
        
        # Aplikasikan fungsi L
        l_result = self._L_function(c_lambda)
        
        # Hitung plaintext: L(c^λ mod n²) × μ mod n
        plaintext = (l_result * mu) % n
        
        return plaintext
    
    def homomorphic_add(self, ciphertext1: int, ciphertext2: int) -> int:
        """
        Penjumlahan homomorphic pada dua ciphertext.
        
        Homomorphic Property: E(m₁) × E(m₂) mod n² = E(m₁ + m₂ mod n)
        
        Mathematical Proof:
        E(m₁) = g^m₁ × r₁^n mod n²
        E(m₂) = g^m₂ × r₂^n mod n²
        E(m₁) × E(m₂) = g^(m₁+m₂) × (r₁r₂)^n mod n²
        
        Ini setara dengan E(m₁ + m₂) dengan randomness r = r₁r₂ mod n.
        
        Args:
            ciphertext1: Ciphertext pertama
            ciphertext2: Ciphertext kedua
            
        Returns:
            Ciphertext hasil penjumlahan E(m₁ + m₂)
        """
        if self.public_key is None:
            raise ValueError("Public key tidak tersedia")
        
        # Penjumlahan homomorphic: perkalian modular
        result = (ciphertext1 * ciphertext2) % self.n_squared
        return result
    
    def homomorphic_multiply_constant(self, ciphertext: int, constant: int) -> int:
        """
        Perkalian homomorphic ciphertext dengan konstanta.
        
        Homomorphic Property: E(m)^k mod n² = E(k × m mod n)
        
        Mathematical Proof:
        E(m) = g^m × r^n mod n²
        E(m)^k = g^(km) × r^(kn) = g^(km) × (r^k)^n mod n²
        
        Ini setara dengan E(k×m) dengan randomness r' = r^k mod n.
        
        Args:
            ciphertext: Ciphertext yang akan dikalikan
            constant: Konstanta pengali (harus non-negatif)
            
        Returns:
            Ciphertext hasil perkalian E(k × m)
            
        Raises:
            ValueError: Jika konstanta negatif
        """
        if self.public_key is None:
            raise ValueError("Public key tidak tersedia")
        
        if constant < 0:
            raise ValueError("Konstanta harus non-negatif")
        
        # Perkalian dengan konstanta: exponentiasi modular
        result = pow(ciphertext, constant, self.n_squared)
        return result
    
    def get_public_key(self) -> dict:
        """
        Mendapatkan kunci publik untuk sharing.
        
        Returns:
            Dictionary berisi public key components {n, g}
        """
        if self.public_key is None:
            raise ValueError("Kunci belum dibuat")
        
        return self.public_key.copy()
    
    def get_key_info(self) -> dict:
        """
        Mendapatkan informasi tentang kunci yang dibuat.
        
        Returns:
            Dictionary berisi metadata kunci
        """
        if self.public_key is None:
            return {"status": "Keys not generated"}
        
        return {
            "bit_length": self.bit_length,
            "n_bit_length": self.public_key['n'].bit_length(),
            "security_level": f"{self.bit_length}-bit",
            "n_value": self.public_key['n'],
            "g_value": self.public_key['g'],
            "status": "Ready"
        }


def create_paillier_instance(bit_length: int = 2048) -> PaillierCore:
    """
    Factory function untuk membuat instance Paillier dengan error handling.
    
    Args:
        bit_length: Panjang bit untuk kunci (default: 2048)
        
    Returns:
        Instance PaillierCore yang siap digunakan
        
    Raises:
        ValueError: Jika bit_length tidak valid
    """
    if bit_length < 512:
        raise ValueError("Bit length minimal 512")
    
    if bit_length % 2 != 0:
        raise ValueError("Bit length harus genap")
    
    return PaillierCore(bit_length)


# Contoh penggunaan dasar
if __name__ == "__main__":
    # Demonstrasi sederhana
    print("🔧 Membuat instance Paillier (2048-bit)...")
    paillier = create_paillier_instance(2048)
    
    print("📊 Info kunci:")
    info = paillier.get_key_info()
    print(f"  - Security level: {info['security_level']}")
    print(f"  - n bit length: {info['n_bit_length']}")
    
    # Test enkripsi/dekripsi
    message = 12345
    print(f"\n🔐 Test enkripsi: {message}")
    encrypted = paillier.encrypt(message)
    print(f"  Ciphertext: {encrypted}")
    
    decrypted = paillier.decrypt(encrypted)
    print(f"  Decrypted: {decrypted}")
    print(f"  ✅ Success: {message == decrypted}")
    
    # Test homomorphic
    a, b = 100, 200
    enc_a = paillier.encrypt(a)
    enc_b = paillier.encrypt(b)
    enc_sum = paillier.homomorphic_add(enc_a, enc_b)
    result = paillier.decrypt(enc_sum)
    
    print(f"\n🧮 Test homomorphic: {a} + {b}")
    print(f"  Result: {result}")
    print(f"  ✅ Success: {result == a + b}")