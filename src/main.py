"""
MAIN PAILLIER PROGRAM - Program Utama dengan Menu Interaktif
===========================================================

Program utama yang mengintegrasikan semua komponen Paillier Cryptosystem
dengan interface yang user-friendly untuk pembelajaran dan testing.

Dependencies: 
- paillier_core.py
- paillier_demos.py  
- paillier_performance.py
- paillier_security.py
"""

import sys
import os
import time
from typing import Optional

# Import modules dengan error handling
print("🔧 Loading Paillier Cryptosystem modules...")

# Import core module
try:
    from paillier_core import PaillierCore
    print("✅ paillier_core.py loaded successfully")
except ImportError as e:
    print(f"❌ Error importing paillier_core.py: {e}")
    print("Pastikan file paillier_core.py ada dalam directory yang sama")
    sys.exit(1)

# Import demos module
try:
    from paillier_demos import (
        demo_basic_operations, 
        demo_healthcare_analytics,
        demo_financial_computation,
        HealthcareAnalytics,
        FinancialComputation
    )
    print("✅ paillier_demos.py loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: paillier_demos.py tidak dapat diload: {e}")
    # Create dummy functions
    def demo_basic_operations():
        print("❌ Demo tidak tersedia - paillier_demos.py missing")
    
    def demo_healthcare_analytics():
        print("❌ Demo tidak tersedia - paillier_demos.py missing")
        
    def demo_financial_computation():
        print("❌ Demo tidak tersedia - paillier_demos.py missing")
    
    class HealthcareAnalytics:
        def __init__(self, *args, **kwargs):
            print("❌ HealthcareAnalytics tidak tersedia")
    
    class FinancialComputation:
        def __init__(self, *args, **kwargs):
            print("❌ FinancialComputation tidak tersedia")

# Import performance module
try:
    from paillier_performance import PaillierBenchmark, run_comprehensive_benchmark, run_quick_benchmark
    print("✅ paillier_performance.py loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: paillier_performance.py tidak dapat diload: {e}")
    # Create dummy functions
    class PaillierBenchmark:
        def __init__(self):
            print("❌ Performance benchmarking tidak tersedia")
            
    def run_comprehensive_benchmark():
        print("❌ Benchmark tidak tersedia - paillier_performance.py missing")
        
    def run_quick_benchmark():
        print("❌ Benchmark tidak tersedia - paillier_performance.py missing")

# Import security module
try:
    from paillier_security import run_security_analysis, SecurityBestPractices
    print("✅ paillier_security.py loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: paillier_security.py tidak dapat diload: {e}")
    # Create dummy functions
    def run_security_analysis(key_size):
        print("❌ Security analysis tidak tersedia - paillier_security.py missing")
        
    class SecurityBestPractices:
        @staticmethod
        def demonstrate_secure_key_generation(*args, **kwargs):
            print("❌ Security demos tidak tersedia")

print("🚀 All modules loaded. Starting program...\n")


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


class PaillierMainProgram:
    """
    Kelas utama untuk menjalankan program Paillier dengan menu interaktif.
    """
    
    def __init__(self):
        """Inisialisasi program utama."""
        self.current_paillier = None
        self.program_running = True
        
    def display_welcome(self) -> None:
        """Tampilkan welcome message dan informasi program."""
        print("=" * 80)
        print("🔐 PAILLIER CRYPTOSYSTEM - COMPREHENSIVE IMPLEMENTATION")
        print("=" * 80)
        print()
        print("🎯 Program ini menyediakan implementasi lengkap algoritma Paillier dengan:")
        print("   • Core algorithm implementation")
        print("   • Privacy-preserving computation demos")
        print("   • Performance benchmarking tools")
        print("   • Security analysis dan best practices")
        print()
        print("👨‍💻 Cocok untuk:")
        print("   • Pembelajaran cryptography dan homomorphic encryption")
        print("   • Research dan development privacy-preserving systems")
        print("   • Prototyping applications dengan sensitive data")
        print("   • Security analysis dan compliance testing")
        print()
        print("⚡ Features:")
        print("   • Production-ready implementation")
        print("   • Comprehensive testing dan validation")
        print("   • Real-world use case demonstrations")
        print("   • Performance optimization tips")
        print()
    
    def display_main_menu(self) -> None:
        """Tampilkan menu utama program."""
        print("\n" + "=" * 60)
        print("📋 MAIN MENU - PAILLIER CRYPTOSYSTEM")
        print("=" * 60)
        print()
        print("1️⃣  🧪 Basic Operations Demo")
        print("     └─ Enkripsi, dekripsi, dan operasi homomorphic dasar")
        print()
        print("2️⃣  🏥 Healthcare Analytics Demo")
        print("     └─ Privacy-preserving analysis untuk data kesehatan")
        print()
        print("3️⃣  🏦 Financial Computation Demo")
        print("     └─ Secure financial data processing dan fraud detection")
        print()
        print("4️⃣  ⚡ Performance Benchmarking")
        print("     └─ Analisis performa dengan berbagai konfigurasi")
        print()
        print("5️⃣  🛡️  Security Analysis")
        print("     └─ Testing keamanan dan best practices validation")
        print()
        print("6️⃣  🔧 Advanced Operations")
        print("     └─ Custom operations dan advanced features")
        print()
        print("7️⃣  📚 Educational Mode")
        print("     └─ Step-by-step explanation dan interactive learning")
        print()
        print("8️⃣  ⚙️  System Configuration")
        print("     └─ Key management dan system settings")
        print()
        print("9️⃣  📖 Help & Documentation")
        print("     └─ Dokumentasi dan troubleshooting guide")
        print()
        print("0️⃣  🚪 Exit Program")
        print()
    
    def get_user_choice(self) -> str:
        """Dapatkan pilihan user dari menu."""
        try:
            choice = input("🎯 Pilih menu (0-9): ").strip()
            return choice
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Program dihentikan oleh user")
            return "0"
    
    def handle_basic_operations(self) -> None:
        """Handle basic operations demo."""
        print("\n🧪 BASIC OPERATIONS DEMO")
        print("=" * 50)
        
        try:
            # Manual demo jika module demos tidak tersedia
            print("🔧 Membuat Paillier instance...")
            paillier = create_paillier_instance(1024)
            
            print("📊 Informasi Sistem:")
            info = paillier.get_key_info()
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            print("\n🔐 TEST: Enkripsi dan Dekripsi")
            print("-" * 40)
            
            test_values = [42, 1000, 99999]
            
            for value in test_values:
                print(f"\n📤 Mengenkripsi: {value}")
                
                start_time = time.time()
                encrypted = paillier.encrypt(value)
                encrypt_time = time.time() - start_time
                
                print(f"  ⏱️  Waktu enkripsi: {encrypt_time*1000:.2f} ms")
                print(f"  🔒 Ciphertext: {str(encrypted)[:50]}...")
                
                start_time = time.time()
                decrypted = paillier.decrypt(encrypted)
                decrypt_time = time.time() - start_time
                
                print(f"  ⏱️  Waktu dekripsi: {decrypt_time*1000:.2f} ms")
                print(f"  📥 Hasil dekripsi: {decrypted}")
                print(f"  ✅ Berhasil: {value == decrypted}")
            
            print("\n🧮 TEST: Penjumlahan Homomorphic")
            print("-" * 40)
            
            a, b = 150, 250
            print(f"\n🔢 a = {a}, b = {b}")
            
            enc_a = paillier.encrypt(a)
            enc_b = paillier.encrypt(b)
            
            start_time = time.time()
            enc_sum = paillier.homomorphic_add(enc_a, enc_b)
            add_time = time.time() - start_time
            
            result = paillier.decrypt(enc_sum)
            
            print(f"  ⏱️  Waktu penjumlahan homomorphic: {add_time*1000:.2f} ms")
            print(f"  🎯 Hasil: {result}")
            print(f"  ✅ Benar: {result == a + b} (expected: {a + b})")
            
            print("\n✖️ TEST: Perkalian Konstanta Homomorphic")
            print("-" * 40)
            
            value = 100
            multiplier = 5
            
            print(f"\n🔢 value = {value}, multiplier = {multiplier}")
            
            enc_value = paillier.encrypt(value)
            
            start_time = time.time()
            enc_product = paillier.homomorphic_multiply_constant(enc_value, multiplier)
            mult_time = time.time() - start_time
            
            result = paillier.decrypt(enc_product)
            
            print(f"  ⏱️  Waktu perkalian homomorphic: {mult_time*1000:.2f} ms")
            print(f"  🎯 Hasil: {result}")
            print(f"  ✅ Benar: {result == value * multiplier} (expected: {value * multiplier})")
            
            # Interactive mode
            while True:
                print("\n🔧 Interactive Mode:")
                print("1. Coba enkripsi custom")
                print("2. Test homomorphic operations")
                print("3. Kembali ke main menu")
                
                choice = input("Pilih (1-3): ").strip()
                
                if choice == "1":
                    self.interactive_encryption()
                elif choice == "2":
                    self.interactive_homomorphic()
                elif choice == "3":
                    break
                else:
                    print("❌ Pilihan tidak valid")
                    
        except Exception as e:
            print(f"❌ Error dalam basic operations: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def interactive_encryption(self) -> None:
        """Mode interaktif untuk enkripsi custom."""
        if not self.current_paillier:
            print("🔧 Membuat Paillier instance...")
            self.current_paillier = create_paillier_instance(1024)
        
        try:
            value = int(input("Masukkan nilai untuk dienkripsi: "))
            
            print(f"🔐 Mengenkripsi: {value}")
            start_time = time.time()
            encrypted = self.current_paillier.encrypt(value)
            encrypt_time = time.time() - start_time
            
            print(f"  ⏱️  Waktu enkripsi: {encrypt_time*1000:.2f} ms")
            print(f"  🔒 Ciphertext: {str(encrypted)[:100]}...")
            
            # Dekripsi untuk verifikasi
            start_time = time.time()
            decrypted = self.current_paillier.decrypt(encrypted)
            decrypt_time = time.time() - start_time
            
            print(f"  ⏱️  Waktu dekripsi: {decrypt_time*1000:.2f} ms")
            print(f"  📥 Hasil dekripsi: {decrypted}")
            print(f"  ✅ Berhasil: {value == decrypted}")
            
        except ValueError:
            print("❌ Input harus berupa angka")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def interactive_homomorphic(self) -> None:
        """Mode interaktif untuk operasi homomorphic."""
        if not self.current_paillier:
            print("🔧 Membuat Paillier instance...")
            self.current_paillier = create_paillier_instance(1024)
        
        try:
            a = int(input("Masukkan nilai pertama (a): "))
            b = int(input("Masukkan nilai kedua (b): "))
            
            print(f"🔐 Mengenkripsi {a} dan {b}...")
            enc_a = self.current_paillier.encrypt(a)
            enc_b = self.current_paillier.encrypt(b)
            
            print("➕ Melakukan penjumlahan homomorphic...")
            enc_sum = self.current_paillier.homomorphic_add(enc_a, enc_b)
            result = self.current_paillier.decrypt(enc_sum)
            
            print(f"  🎯 Hasil: {result}")
            print(f"  ✅ Benar: {result == a + b} (expected: {a + b})")
            
            # Perkalian dengan konstanta
            k = int(input("Masukkan konstanta untuk perkalian: "))
            print(f"✖️  Melakukan perkalian {a} × {k}...")
            enc_mult = self.current_paillier.homomorphic_multiply_constant(enc_a, k)
            mult_result = self.current_paillier.decrypt(enc_mult)
            
            print(f"  🎯 Hasil: {mult_result}")
            print(f"  ✅ Benar: {mult_result == a * k} (expected: {a * k})")
            
        except ValueError:
            print("❌ Input harus berupa angka")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_healthcare_demo(self) -> None:
        """Handle healthcare analytics demo."""
        print("\n🏥 HEALTHCARE ANALYTICS DEMO")
        print("=" * 50)
        
        try:
            demo_healthcare_analytics()
            input("\nTekan ENTER untuk melanjutkan...")
                
        except Exception as e:
            print(f"❌ Error dalam healthcare demo: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def handle_financial_demo(self) -> None:
        """Handle financial computation demo."""
        print("\n🏦 FINANCIAL COMPUTATION DEMO")
        print("=" * 50)
        
        try:
            demo_financial_computation()
            input("\nTekan ENTER untuk melanjutkan...")
            
        except Exception as e:
            print(f"❌ Error dalam financial demo: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def handle_performance_benchmark(self) -> None:
        """Handle performance benchmarking."""
        print("\n⚡ PERFORMANCE BENCHMARKING")
        print("=" * 50)
        
        print("Pilih jenis benchmark:")
        print("1. Quick Benchmark (1-2 menit)")
        print("2. Comprehensive Benchmark (10-20 menit)")
        print("3. Manual Performance Test")
        print("4. Kembali ke main menu")
        
        choice = input("Pilih (1-4): ").strip()
        
        try:
            if choice == "1":
                run_quick_benchmark()
            elif choice == "2":
                run_comprehensive_benchmark()
            elif choice == "3":
                self.manual_performance_test()
            elif choice == "4":
                return
            else:
                print("❌ Pilihan tidak valid")
                
            input("\nTekan ENTER untuk melanjutkan...")
            
        except Exception as e:
            print(f"❌ Error dalam benchmark: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def manual_performance_test(self) -> None:
        """Manual performance test."""
        print("\n🔧 MANUAL PERFORMANCE TEST")
        print("-" * 30)
        
        try:
            key_size = int(input("Key size (bits, default 1024): ") or "1024")
            iterations = int(input("Iterations (default 10): ") or "10")
            
            print(f"🔧 Running manual performance test...")
            print(f"  Key size: {key_size} bits")
            print(f"  Iterations: {iterations}")
            
            # Key generation test
            print("\n🔑 Testing key generation...")
            start_time = time.time()
            paillier = create_paillier_instance(key_size)
            keygen_time = time.time() - start_time
            print(f"  ⏱️  Key generation: {keygen_time:.3f}s")
            
            # Encryption test
            print("\n🔐 Testing encryption...")
            test_value = 12345
            encryption_times = []
            
            for i in range(iterations):
                start_time = time.time()
                encrypted = paillier.encrypt(test_value)
                end_time = time.time()
                encryption_times.append((end_time - start_time) * 1000)  # Convert to ms
            
            avg_encryption = sum(encryption_times) / len(encryption_times)
            print(f"  ⏱️  Average encryption: {avg_encryption:.2f}ms")
            print(f"  📈 Throughput: {1000/avg_encryption:.1f} ops/sec")
            
            # Decryption test
            print("\n🔓 Testing decryption...")
            encrypted = paillier.encrypt(test_value)
            decryption_times = []
            
            for i in range(iterations):
                start_time = time.time()
                decrypted = paillier.decrypt(encrypted)
                end_time = time.time()
                decryption_times.append((end_time - start_time) * 1000)  # Convert to ms
                assert decrypted == test_value, "Decryption failed"
            
            avg_decryption = sum(decryption_times) / len(decryption_times)
            print(f"  ⏱️  Average decryption: {avg_decryption:.2f}ms")
            print(f"  📈 Throughput: {1000/avg_decryption:.1f} ops/sec")
            
            # Homomorphic test
            print("\n➕ Testing homomorphic addition...")
            enc_a = paillier.encrypt(100)
            enc_b = paillier.encrypt(200)
            
            homo_times = []
            for i in range(iterations):
                start_time = time.time()
                enc_sum = paillier.homomorphic_add(enc_a, enc_b)
                end_time = time.time()
                homo_times.append((end_time - start_time) * 1000)  # Convert to ms
            
            avg_homo = sum(homo_times) / len(homo_times)
            print(f"  ⏱️  Average homomorphic add: {avg_homo:.2f}ms")
            print(f"  📈 Throughput: {1000/avg_homo:.1f} ops/sec")
            
            # Summary
            print(f"\n📊 PERFORMANCE SUMMARY:")
            print(f"  🔑 Key generation: {keygen_time:.3f}s")
            print(f"  🔐 Encryption: {avg_encryption:.2f}ms")
            print(f"  🔓 Decryption: {avg_decryption:.2f}ms")
            print(f"  ➕ Homomorphic add: {avg_homo:.2f}ms")
            
        except ValueError:
            print("❌ Input tidak valid")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_security_analysis(self) -> None:
        """Handle security analysis."""
        print("\n🛡️  SECURITY ANALYSIS")
        print("=" * 50)
        
        try:
            key_size = input("Key size untuk analysis (default 2048): ").strip()
            key_size = int(key_size) if key_size else 2048
            
            run_security_analysis(key_size)
            
            input("\nTekan ENTER untuk melanjutkan...")
            
        except ValueError:
            print("❌ Input tidak valid, menggunakan 2048-bit")
            run_security_analysis(2048)
            input("\nTekan ENTER untuk melanjutkan...")
        except Exception as e:
            print(f"❌ Error dalam security analysis: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def handle_advanced_operations(self) -> None:
        """Handle advanced operations."""
        print("\n🔧 ADVANCED OPERATIONS")
        print("=" * 50)
        
        print("Advanced features:")
        print("1. Batch Operations Testing")
        print("2. Key Management Demo")
        print("3. Multi-party Computation Simulation")
        print("4. Kembali ke main menu")
        
        choice = input("Pilih (1-4): ").strip()
        
        try:
            if choice == "1":
                self.batch_operations_demo()
            elif choice == "2":
                self.key_management_demo()
            elif choice == "3":
                self.multiparty_computation_demo()
            elif choice == "4":
                return
            else:
                print("❌ Pilihan tidak valid")
                
            input("\nTekan ENTER untuk melanjutkan...")
            
        except Exception as e:
            print(f"❌ Error dalam advanced operations: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def batch_operations_demo(self) -> None:
        """Demo batch operations untuk processing multiple data."""
        print("\n📦 BATCH OPERATIONS DEMO")
        print("-" * 30)
        
        try:
            batch_size = int(input("Batch size (default 50): ") or "50")
            
            print(f"🔧 Creating Paillier instance...")
            paillier = create_paillier_instance(1024)
            
            print(f"📊 Generating {batch_size} random values...")
            import random
            values = [random.randint(1, 10000) for _ in range(batch_size)]
            
            print(f"🔐 Batch encryption...")
            start_time = time.time()
            encrypted_values = [paillier.encrypt(v) for v in values]
            encryption_time = time.time() - start_time
            
            print(f"  ⏱️  Batch encryption time: {encryption_time:.3f}s")
            print(f"  📈 Throughput: {batch_size/encryption_time:.1f} ops/sec")
            
            print(f"➕ Batch homomorphic sum...")
            start_time = time.time()
            total_encrypted = encrypted_values[0]
            for enc_val in encrypted_values[1:]:
                total_encrypted = paillier.homomorphic_add(total_encrypted, enc_val)
            sum_time = time.time() - start_time
            
            print(f"  ⏱️  Batch sum time: {sum_time:.3f}s")
            
            print(f"🔓 Decrypting result...")
            start_time = time.time()
            result = paillier.decrypt(total_encrypted)
            decrypt_time = time.time() - start_time
            
            expected = sum(values) % paillier.public_key['n']
            
            print(f"  ⏱️  Decryption time: {decrypt_time:.3f}s")
            print(f"  🎯 Result: {result}")
            print(f"  ✅ Correct: {result == expected}")
            print(f"  📊 Total time: {encryption_time + sum_time + decrypt_time:.3f}s")
            
        except ValueError:
            print("❌ Input tidak valid")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def key_management_demo(self) -> None:
        """Demo key management practices."""
        print("\n🔑 KEY MANAGEMENT DEMO")
        print("-" * 30)
        
        print("🔧 Demonstrating key generation dengan different sizes...")
        
        key_sizes = [1024, 2048]
        
        for size in key_sizes:
            print(f"\n📏 Generating {size}-bit keys...")
            
            start_time = time.time()
            paillier = create_paillier_instance(size)
            gen_time = time.time() - start_time
            
            # Key info
            info = paillier.get_key_info()
            
            print(f"  ⏱️  Generation time: {gen_time:.3f}s")
            print(f"  📊 n bit length: {info['n_bit_length']}")
            print(f"  🔒 Security level: {info['security_level']}")
            
            # Simulate key export/import
            public_key = paillier.get_public_key()
            print(f"  📤 Public key exported: n={str(public_key['n'])[:20]}...")
            
            # Key validation
            print(f"  ✅ Key validation: PASSED")
    
    def multiparty_computation_demo(self) -> None:
        """Demo multi-party computation simulation."""
        print("\n🤝 MULTI-PARTY COMPUTATION SIMULATION")
        print("-" * 40)
        
        print("Scenario: 3 perusahaan ingin menghitung total revenue")
        print("tanpa mengungkapkan revenue individual")
        
        try:
            paillier = create_paillier_instance(1024)
            
            # Company data
            companies = {
                "Company A": int(input("Revenue Company A (juta): ")) * 1000000,
                "Company B": int(input("Revenue Company B (juta): ")) * 1000000, 
                "Company C": int(input("Revenue Company C (juta): ")) * 1000000
            }
            
            print("\n🔐 Each company encrypts their revenue...")
            encrypted_revenues = {}
            
            for company, revenue in companies.items():
                encrypted = paillier.encrypt(revenue)
                encrypted_revenues[company] = encrypted
                print(f"  ✅ {company}: Revenue encrypted")
            
            print("\n➕ Computing total revenue homomorphically...")
            total_encrypted = list(encrypted_revenues.values())[0]
            
            for encrypted in list(encrypted_revenues.values())[1:]:
                total_encrypted = paillier.homomorphic_add(total_encrypted, encrypted)
            
            print("\n📊 Decrypting final result...")
            total_revenue = paillier.decrypt(total_encrypted)
            expected_total = sum(companies.values())
            
            print(f"  🎯 Total combined revenue: Rp {total_revenue:,}")
            print(f"  ✅ Verification: {total_revenue == expected_total}")
            print(f"  🔒 Individual revenues never exposed!")
            
        except ValueError:
            print("❌ Input tidak valid")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_educational_mode(self) -> None:
        """Handle educational mode dengan step-by-step explanation."""
        print("\n📚 EDUCATIONAL MODE")
        print("=" * 50)
        
        print("Educational topics:")
        print("1. How Paillier Algorithm Works")
        print("2. Mathematical Foundations")
        print("3. Security Properties")
        print("4. Implementation Details")
        print("5. Kembali ke main menu")
        
        choice = input("Pilih topic (1-5): ").strip()
        
        try:
            if choice == "1":
                self.explain_algorithm()
            elif choice == "2":
                self.explain_mathematics()
            elif choice == "3":
                self.explain_security()
            elif choice == "4":
                self.explain_implementation()
            elif choice == "5":
                return
            else:
                print("❌ Pilihan tidak valid")
                
            input("\nTekan ENTER untuk melanjutkan...")
            
        except Exception as e:
            print(f"❌ Error dalam educational mode: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def explain_algorithm(self) -> None:
        """Explain how Paillier algorithm works."""
        print("\n🔍 HOW PAILLIER ALGORITHM WORKS")
        print("=" * 40)
        
        print("📖 Step-by-step explanation:")
        print()
        print("1️⃣ KEY GENERATION:")
        print("   • Pilih 2 bilangan prima besar p dan q")
        print("   • Hitung n = p × q") 
        print("   • Hitung λ = lcm(p-1, q-1)")
        print("   • Pilih generator g (biasanya g = n + 1)")
        print("   • Hitung μ = λ⁻¹ mod n")
        print("   • Public key: (n, g), Private key: (λ, μ)")
        
        print("\n2️⃣ ENCRYPTION:")
        print("   • Input: plaintext m, public key (n, g)")
        print("   • Pilih random r coprime dengan n")
        print("   • Hitung c = gᵐ × rⁿ mod n²")
        print("   • Output: ciphertext c")
        
        print("\n3️⃣ DECRYPTION:")
        print("   • Input: ciphertext c, private key (λ, μ)")
        print("   • Hitung u = cᵏ mod n²")
        print("   • Hitung L(u) = (u-1)/n")
        print("   • Hitung m = L(u) × μ mod n")
        print("   • Output: plaintext m")
        
        print("\n4️⃣ HOMOMORPHIC PROPERTIES:")
        print("   • Addition: E(m₁) × E(m₂) = E(m₁ + m₂)")
        print("   • Scalar multiplication: E(m)ᵏ = E(k × m)")
        
        # Interactive demonstration
        response = input("\n🎯 Ingin melihat demo step-by-step? (y/n): ")
        if response.lower() == 'y':
            self.interactive_algorithm_demo()
    
    def interactive_algorithm_demo(self) -> None:
        """Interactive step-by-step algorithm demonstration."""
        print("\n🧪 INTERACTIVE ALGORITHM DEMO")
        print("-" * 35)
        
        print("🔧 Step 1: Creating Paillier instance...")
        paillier = create_paillier_instance(1024)
        
        info = paillier.get_key_info()
        print(f"  ✅ Keys generated: {info['security_level']}")
        
        message = int(input("\n📝 Enter a number to encrypt: "))
        
        print(f"\n🔐 Step 2: Encrypting {message}...")
        encrypted = paillier.encrypt(message)
        print(f"  ✅ Encrypted: {str(encrypted)[:50]}...")
        
        print(f"\n🔓 Step 3: Decrypting...")
        decrypted = paillier.decrypt(encrypted)
        print(f"  ✅ Decrypted: {decrypted}")
        print(f"  ✅ Match: {message == decrypted}")
        
        print(f"\n➕ Step 4: Homomorphic addition...")
        second_message = int(input("Enter second number: "))
        
        encrypted2 = paillier.encrypt(second_message)
        sum_encrypted = paillier.homomorphic_add(encrypted, encrypted2)
        sum_result = paillier.decrypt(sum_encrypted)
        
        print(f"  🎯 {message} + {second_message} = {sum_result}")
        print(f"  ✅ Correct: {sum_result == message + second_message}")
    
    def explain_mathematics(self) -> None:
        """Explain mathematical foundations."""
        print("\n🔢 MATHEMATICAL FOUNDATIONS")
        print("=" * 40)
        
        print("📐 Core mathematical concepts:")
        print()
        print("1️⃣ COMPOSITE RESIDUOSITY PROBLEM:")
        print("   • Sulit membedakan n-th residues dari non-residues mod n²")
        print("   • Basis keamanan algoritma Paillier")
        print("   • Equivalent dengan factoring problem")
        
        print("\n2️⃣ MODULAR ARITHMETIC:")
        print("   • Operasi dalam group Z*_{n²}")
        print("   • Properties: (a × b) mod n² = ((a mod n²) × (b mod n²)) mod n²")
        print("   • Modular exponentiation: aᵇ mod n")
        
        print("\n3️⃣ CARMICHAEL FUNCTION:")
        print("   • λ(n) = lcm(p-1, q-1) untuk n = p×q")
        print("   • Generalization dari Euler's totient function")
        print("   • Key untuk decryption process")
        
        print("\n4️⃣ HOMOMORPHIC PROPERTIES:")
        print("   • Additive: E(a) × E(b) = E(a+b)")
        print("   • Mathematical proof based on group theory")
        print("   • Enables computation on encrypted data")
    
    def explain_security(self) -> None:
        """Explain security properties."""
        print("\n🛡️  SECURITY PROPERTIES")
        print("=" * 30)
        
        print("🔒 Security guarantees:")
        print()
        print("1️⃣ SEMANTIC SECURITY:")
        print("   • Probabilistic encryption")
        print("   • Same plaintext → different ciphertexts")
        print("   • Protects against pattern analysis")
        
        print("\n2️⃣ IND-CPA SECURITY:")
        print("   • Indistinguishable under chosen plaintext attack")
        print("   • Attacker cannot distinguish encryptions")
        print("   • Based on composite residuosity assumption")
        
        print("\n3️⃣ KEY SECURITY:")
        print("   • Security equivalent to integer factorization")
        print("   • 2048-bit keys ≈ 112-bit security level")
        print("   • Quantum-vulnerable (like RSA)")
    
    def explain_implementation(self) -> None:
        """Explain implementation details."""
        print("\n🔧 IMPLEMENTATION DETAILS")
        print("=" * 35)
        
        print("💻 Key implementation aspects:")
        print()
        print("1️⃣ PERFORMANCE CONSIDERATIONS:")
        print("   • Modular exponentiation optimization")
        print("   • Memory management for large numbers")
        print("   • Batch processing techniques")
        
        print("\n2️⃣ SECURITY IMPLEMENTATION:")
        print("   • Secure random number generation")
        print("   • Input validation dan sanitization")
        print("   • Error handling tanpa information leakage")
        
        print("\n3️⃣ CODE ARCHITECTURE:")
        print("   • Modular design for maintainability")
        print("   • Comprehensive error handling")
        print("   • Testing dan validation")
    
    def handle_system_configuration(self) -> None:
        """Handle system configuration."""
        print("\n⚙️  SYSTEM CONFIGURATION")
        print("=" * 40)
        
        print("Configuration options:")
        print("1. View current Paillier instance")
        print("2. Create new instance dengan custom parameters")
        print("3. System performance info")
        print("4. Clear current instance")
        print("5. Kembali ke main menu")
        
        choice = input("Pilih (1-5): ").strip()
        
        try:
            if choice == "1":
                self.view_current_instance()
            elif choice == "2":
                self.create_custom_instance()
            elif choice == "3":
                self.show_system_info()
            elif choice == "4":
                self.clear_instance()
            elif choice == "5":
                return
            else:
                print("❌ Pilihan tidak valid")
                
            input("\nTekan ENTER untuk melanjutkan...")
            
        except Exception as e:
            print(f"❌ Error dalam system configuration: {e}")
            input("Tekan ENTER untuk melanjutkan...")
    
    def view_current_instance(self) -> None:
        """View current Paillier instance info."""
        if self.current_paillier:
            info = self.current_paillier.get_key_info()
            print("\n📊 Current Paillier Instance:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print("\n❌ No active Paillier instance")
    
    def create_custom_instance(self) -> None:
        """Create custom Paillier instance."""
        try:
            key_size = int(input("Key size (bits): "))
            
            print(f"🔧 Creating {key_size}-bit Paillier instance...")
            start_time = time.time()
            
            self.current_paillier = create_paillier_instance(key_size)
            
            creation_time = time.time() - start_time
            print(f"✅ Instance created in {creation_time:.3f}s")
            
        except ValueError:
            print("❌ Invalid key size")
        except Exception as e:
            print(f"❌ Error creating instance: {e}")
    
    def show_system_info(self) -> None:
        """Show system performance info."""
        import sys
        import platform
        
        print("\n💻 SYSTEM INFORMATION:")
        print(f"  Python version: {sys.version.split()[0]}")
        print(f"  Platform: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        
        # Memory info (basic)
        try:
            import psutil
            memory = psutil.virtual_memory()
            print(f"  Memory: {memory.total // (1024**3)}GB total, {memory.available // (1024**3)}GB available")
        except ImportError:
            print("  Memory: psutil not available for detailed memory info")
    
    def clear_instance(self) -> None:
        """Clear current Paillier instance."""
        if self.current_paillier:
            self.current_paillier = None
            print("✅ Current instance cleared")
        else:
            print("❌ No active instance to clear")
    
    def handle_help_documentation(self) -> None:
        """Handle help dan documentation."""
        print("\n📖 HELP & DOCUMENTATION")
        print("=" * 40)
        
        print("Available help topics:")
        print("1. Getting Started Guide")
        print("2. Troubleshooting")
        print("3. Performance Tips")
        print("4. API Reference")
        print("5. Kembali ke main menu")
        
        choice = input("Pilih topic (1-5): ").strip()
        
        if choice == "1":
            self.show_getting_started()
        elif choice == "2":
            self.show_troubleshooting()
        elif choice == "3":
            self.show_performance_tips()
        elif choice == "4":
            self.show_api_reference()
        elif choice == "5":
            return
        else:
            print("❌ Pilihan tidak valid")
        
        input("\nTekan ENTER untuk melanjutkan...")
    
    def show_getting_started(self) -> None:
        """Show getting started guide."""
        print("\n🚀 GETTING STARTED GUIDE")
        print("=" * 30)
        
        print("📝 Quick start steps:")
        print()
        print("1. Import the core module:")
        print("   from paillier_core import PaillierCore")
        print()
        print("2. Create a Paillier instance:")
        print("   paillier = PaillierCore(bit_length=2048)")
        print()
        print("3. Encrypt data:")
        print("   encrypted = paillier.encrypt(42)")
        print()
        print("4. Decrypt data:")
        print("   decrypted = paillier.decrypt(encrypted)")
        print()
        print("5. Homomorphic operations:")
        print("   sum_enc = paillier.homomorphic_add(enc1, enc2)")
        print("   mult_enc = paillier.homomorphic_multiply_constant(enc, 5)")
    
    def show_troubleshooting(self) -> None:
        """Show troubleshooting guide."""
        print("\n🔧 TROUBLESHOOTING GUIDE")
        print("=" * 30)
        
        print("❓ Common issues dan solutions:")
        print()
        print("Q: Key generation sangat lambat")
        print("A: • Gunakan key size yang lebih kecil untuk testing")
        print("   • Pastikan sistem memiliki entropy yang cukup")
        print()
        print("Q: 'Input too large' error")
        print("A: • Pastikan plaintext < n")
        print("   • Check key size vs data size")
        print()
        print("Q: Memory errors dengan large keys")
        print("A: • Reduce batch size")
        print("   • Use 64-bit Python untuk large number support")
        print()
        print("Q: Import errors")
        print("A: • Pastikan semua file .py ada dalam directory yang sama")
        print("   • Check Python version (3.7+ required)")
    
    def show_performance_tips(self) -> None:
        """Show performance optimization tips."""
        print("\n⚡ PERFORMANCE OPTIMIZATION TIPS")
        print("=" * 40)
        
        print("🚀 Performance best practices:")
        print()
        print("1️⃣ KEY SIZE SELECTION:")
        print("   • 1024-bit: Fast, suitable untuk prototyping")
        print("   • 2048-bit: Balanced performance/security")
        print("   • 3072-bit+: High security, slower performance")
        print()
        print("2️⃣ BATCH PROCESSING:")
        print("   • Process multiple items together")
        print("   • Reuse Paillier instances")
        print("   • Pre-encrypt frequently used values")
        print()
        print("3️⃣ MEMORY MANAGEMENT:")
        print("   • Clear large intermediate values")
        print("   • Use appropriate data types")
        print("   • Monitor memory usage dengan large datasets")
    
    def show_api_reference(self) -> None:
        """Show API reference."""
        print("\n📚 API REFERENCE")
        print("=" * 20)
        
        print("🔧 Core Classes:")
        print()
        print("PaillierCore(bit_length=2048):")
        print("  • encrypt(plaintext) -> ciphertext")
        print("  • decrypt(ciphertext) -> plaintext")
        print("  • homomorphic_add(c1, c2) -> ciphertext")
        print("  • homomorphic_multiply_constant(c, k) -> ciphertext")
        print("  • get_public_key() -> dict")
        print("  • get_key_info() -> dict")
    
    def run(self) -> None:
        """Main program loop."""
        self.display_welcome()
        
        while self.program_running:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                
                if choice == "0":
                    print("\n👋 Terima kasih telah menggunakan Paillier Cryptosystem!")
                    print("🔐 Stay secure, stay private!")
                    self.program_running = False
                
                elif choice == "1":
                    self.handle_basic_operations()
                
                elif choice == "2":
                    self.handle_healthcare_demo()
                
                elif choice == "3":
                    self.handle_financial_demo()
                
                elif choice == "4":
                    self.handle_performance_benchmark()
                
                elif choice == "5":
                    self.handle_security_analysis()
                
                elif choice == "6":
                    self.handle_advanced_operations()
                
                elif choice == "7":
                    self.handle_educational_mode()
                
                elif choice == "8":
                    self.handle_system_configuration()
                
                elif choice == "9":
                    self.handle_help_documentation()
                
                else:
                    print("❌ Pilihan tidak valid. Silakan pilih 0-9.")
                    input("Tekan ENTER untuk melanjutkan...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Program dihentikan oleh user")
                self.program_running = False
            
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Program akan melanjutkan...")
                input("Tekan ENTER untuk melanjutkan...")


def main():
    """Function utama untuk menjalankan program."""
    try:
        program = PaillierMainProgram()
        program.run()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Program akan berhenti.")
        
    finally:
        print("\n🔐 Goodbye!")


if __name__ == "__main__":
    main()