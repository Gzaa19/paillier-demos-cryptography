"""
PAILLIER DEMOS - Demonstrasi dan Contoh Penggunaan
=================================================

File ini berisi berbagai demonstrasi praktis penggunaan algoritma Paillier
untuk aplikasi real-world seperti healthcare analytics, financial computation,
dan privacy-preserving statistics.

Dependencies: paillier_core.py
"""

import time
import random
from typing import List, Dict, Any
from paillier_core import PaillierCore


class HealthcareAnalytics:
    """
    Demonstrasi privacy-preserving analytics untuk data kesehatan.
    
    Skenario: Beberapa rumah sakit ingin melakukan analisis bersama
    tanpa sharing data pasien individual.
    """
    
    def __init__(self, bit_length: int = 2048):
        """
        Inisialisasi sistem analytics dengan Paillier encryption.
        
        Args:
            bit_length: Ukuran kunci untuk keamanan
        """
        print("🏥 Inisialisasi Healthcare Analytics System...")
        self.paillier = PaillierCore(bit_length)
        self.hospitals_data = {}
        print("✅ Sistem siap untuk menerima data terenkripsi")
    
    def add_hospital_data(self, hospital_name: str, patient_data: List[Dict]) -> None:
        """
        Menambah data rumah sakit yang sudah dienkripsi.
        
        Args:
            hospital_name: Nama rumah sakit
            patient_data: List data pasien dengan fields numerik
        """
        print(f"\n🏥 Memproses data dari {hospital_name}...")
        
        encrypted_patients = []
        for i, patient in enumerate(patient_data, 1):
            encrypted_patient = {}
            
            # Enkripsi setiap field numerik
            for field, value in patient.items():
                if isinstance(value, (int, float)):
                    encrypted_patient[field] = self.paillier.encrypt(int(value))
                else:
                    # Field non-numerik disimpan apa adanya (untuk demo)
                    encrypted_patient[field] = value
            
            encrypted_patients.append(encrypted_patient)
            print(f"  ✅ Pasien {i}: Data terenkripsi dan disimpan")
        
        self.hospitals_data[hospital_name] = encrypted_patients
        print(f"  📊 Total {len(patient_data)} pasien dari {hospital_name}")
    
    def calculate_national_average_age(self) -> float:
        """
        Hitung rata-rata usia pasien nasional tanpa melihat data individual.
        
        Returns:
            Rata-rata usia nasional
        """
        print("\n🔍 Menghitung rata-rata usia nasional (privacy-preserving)...")
        
        total_age_encrypted = None
        patient_count = 0
        
        for hospital, patients in self.hospitals_data.items():
            print(f"  📡 Memproses data dari {hospital}...")
            
            for patient in patients:
                if 'age' in patient:
                    if total_age_encrypted is None:
                        total_age_encrypted = patient['age']
                    else:
                        # Homomorphic addition
                        total_age_encrypted = self.paillier.homomorphic_add(
                            total_age_encrypted, patient['age']
                        )
                    patient_count += 1
        
        if total_age_encrypted is None:
            raise ValueError("Tidak ada data usia tersedia")
        
        # Dekripsi hanya hasil akhir
        total_age = self.paillier.decrypt(total_age_encrypted)
        average_age = total_age / patient_count
        
        print(f"  👥 Total pasien dianalisis: {patient_count}")
        print(f"  🎯 Rata-rata usia nasional: {average_age:.1f} tahun")
        print("  🔒 Privasi terjaga: Tidak ada data individual yang diakses!")
        
        return average_age
    
    def calculate_total_healthcare_cost(self) -> int:
        """
        Hitung total biaya healthcare tanpa melihat data individual.
        
        Returns:
            Total biaya healthcare nasional
        """
        print("\n💰 Menghitung total biaya healthcare nasional...")
        
        total_cost_encrypted = None
        
        for hospital, patients in self.hospitals_data.items():
            print(f"  💳 Memproses biaya dari {hospital}...")
            
            for patient in patients:
                if 'treatment_cost' in patient:
                    if total_cost_encrypted is None:
                        total_cost_encrypted = patient['treatment_cost']
                    else:
                        total_cost_encrypted = self.paillier.homomorphic_add(
                            total_cost_encrypted, patient['treatment_cost']
                        )
        
        if total_cost_encrypted is None:
            raise ValueError("Tidak ada data biaya tersedia")
        
        total_cost = self.paillier.decrypt(total_cost_encrypted)
        
        print(f"  💵 Total biaya healthcare nasional: Rp {total_cost:,}")
        print("  🔒 Data finansial individual tetap rahasia!")
        
        return total_cost
    
    def detect_regional_anomaly(self, field: str, threshold_multiplier: float = 2.0) -> Dict:
        """
        Deteksi anomali regional berdasarkan field tertentu.
        
        Args:
            field: Field yang akan dianalisis (misal: 'treatment_cost')
            threshold_multiplier: Multiplier untuk menentukan anomali
            
        Returns:
            Dictionary hasil analisis anomali
        """
        print(f"\n🚨 Deteksi anomali untuk field '{field}'...")
        
        hospital_averages = {}
        
        for hospital, patients in self.hospitals_data.items():
            print(f"  📊 Menganalisis {hospital}...")
            
            total_encrypted = None
            count = 0
            
            for patient in patients:
                if field in patient:
                    if total_encrypted is None:
                        total_encrypted = patient[field]
                    else:
                        total_encrypted = self.paillier.homomorphic_add(
                            total_encrypted, patient[field]
                        )
                    count += 1
            
            if total_encrypted is not None and count > 0:
                total_value = self.paillier.decrypt(total_encrypted)
                average = total_value / count
                hospital_averages[hospital] = {
                    'average': average,
                    'patient_count': count
                }
        
        # Hitung rata-rata global
        global_total = sum(data['average'] * data['patient_count'] 
                          for data in hospital_averages.values())
        global_count = sum(data['patient_count'] for data in hospital_averages.values())
        global_average = global_total / global_count if global_count > 0 else 0
        
        # Deteksi anomali
        anomalies = {}
        threshold = global_average * threshold_multiplier
        
        for hospital, data in hospital_averages.items():
            if data['average'] > threshold:
                anomalies[hospital] = {
                    'average': data['average'],
                    'global_average': global_average,
                    'ratio': data['average'] / global_average,
                    'severity': 'HIGH' if data['average'] > threshold * 1.5 else 'MEDIUM'
                }
        
        print(f"  🎯 Rata-rata global {field}: {global_average:,.0f}")
        print(f"  ⚠️  Threshold anomali: {threshold:,.0f}")
        print(f"  🚨 Anomali terdeteksi: {len(anomalies)} rumah sakit")
        
        return {
            'global_average': global_average,
            'threshold': threshold,
            'anomalies': anomalies,
            'hospital_count': len(hospital_averages)
        }


class FinancialComputation:
    """
    Demonstrasi privacy-preserving computation untuk data finansial.
    """
    
    def __init__(self, bit_length: int = 2048):
        """Inisialisasi sistem financial computation."""
        print("🏦 Inisialisasi Financial Computation System...")
        self.paillier = PaillierCore(bit_length)
        self.banks_data = {}
        print("✅ Sistem siap untuk analisis finansial terenkripsi")
    
    def add_bank_transactions(self, bank_name: str, transactions: List[int]) -> None:
        """
        Menambah data transaksi bank yang terenkripsi.
        
        Args:
            bank_name: Nama bank
            transactions: List jumlah transaksi (dalam rupiah)
        """
        print(f"\n🏦 Memproses transaksi dari {bank_name}...")
        
        encrypted_transactions = []
        for i, amount in enumerate(transactions, 1):
            if amount < 0:
                print(f"  ⚠️  Transaksi {i}: Jumlah negatif diabaikan")
                continue
            
            encrypted_amount = self.paillier.encrypt(amount)
            encrypted_transactions.append(encrypted_amount)
            
            # Show progress untuk transaksi besar
            if i % 100 == 0:
                print(f"  📊 Progress: {i}/{len(transactions)} transaksi dienkripsi")
        
        self.banks_data[bank_name] = encrypted_transactions
        print(f"  ✅ {len(encrypted_transactions)} transaksi terenkripsi dari {bank_name}")
    
    def calculate_total_transaction_volume(self) -> int:
        """
        Hitung total volume transaksi lintas bank tanpa melihat data individual.
        
        Returns:
            Total volume transaksi dalam rupiah
        """
        print("\n💰 Menghitung total volume transaksi nasional...")
        
        total_volume_encrypted = None
        transaction_count = 0
        
        for bank, transactions in self.banks_data.items():
            print(f"  🏦 Memproses volume dari {bank}...")
            
            for transaction in transactions:
                if total_volume_encrypted is None:
                    total_volume_encrypted = transaction
                else:
                    total_volume_encrypted = self.paillier.homomorphic_add(
                        total_volume_encrypted, transaction
                    )
                transaction_count += 1
        
        if total_volume_encrypted is None:
            raise ValueError("Tidak ada data transaksi tersedia")
        
        total_volume = self.paillier.decrypt(total_volume_encrypted)
        
        print(f"  📊 Total transaksi dianalisis: {transaction_count:,}")
        print(f"  💵 Total volume nasional: Rp {total_volume:,}")
        print("  🔒 Detail transaksi individual tetap rahasia!")
        
        return total_volume
    
    def calculate_average_transaction(self) -> float:
        """
        Hitung rata-rata nilai transaksi lintas bank.
        
        Returns:
            Rata-rata nilai transaksi
        """
        print("\n📊 Menghitung rata-rata nilai transaksi...")
        
        total_volume = self.calculate_total_transaction_volume()
        total_count = sum(len(transactions) for transactions in self.banks_data.values())
        
        if total_count == 0:
            raise ValueError("Tidak ada transaksi untuk dianalisis")
        
        average_transaction = total_volume / total_count
        
        print(f"  🎯 Rata-rata nilai transaksi: Rp {average_transaction:,.0f}")
        
        return average_transaction
    
    def fraud_detection_scoring(self, suspicious_threshold: int = 100_000_000) -> Dict:
        """
        Sistem scoring untuk deteksi fraud berdasarkan pola transaksi.
        
        Args:
            suspicious_threshold: Threshold untuk transaksi mencurigakan (default: 100 juta)
            
        Returns:
            Dictionary hasil analisis fraud
        """
        print(f"\n🕵️ Analisis fraud detection (threshold: Rp {suspicious_threshold:,})...")
        
        bank_scores = {}
        
        for bank, transactions in self.banks_data.items():
            print(f"  🔍 Menganalisis {bank}...")
            
            # Hitung jumlah transaksi "besar" menggunakan homomorphic comparison
            # Note: Ini simplified version, real implementation butuh secure comparison
            suspicious_count = 0
            total_transactions = len(transactions)
            
            # Untuk demo, kita dekripsi dan hitung (dalam real app, gunakan secure comparison)
            for transaction in transactions:
                amount = self.paillier.decrypt(transaction)
                if amount > suspicious_threshold:
                    suspicious_count += 1
            
            # Hitung fraud risk score
            if total_transactions > 0:
                risk_ratio = suspicious_count / total_transactions
                risk_score = min(risk_ratio * 100, 100)  # Cap at 100
                
                risk_level = 'LOW'
                if risk_score > 20:
                    risk_level = 'HIGH'
                elif risk_score > 10:
                    risk_level = 'MEDIUM'
                
                bank_scores[bank] = {
                    'total_transactions': total_transactions,
                    'suspicious_count': suspicious_count,
                    'risk_ratio': risk_ratio,
                    'risk_score': risk_score,
                    'risk_level': risk_level
                }
                
                print(f"    📈 Risk score: {risk_score:.1f}% ({risk_level})")
        
        print(f"  🎯 Analisis selesai untuk {len(bank_scores)} bank")
        
        return bank_scores


def demo_basic_operations():
    """Demo operasi dasar Paillier untuk pemahaman konsep."""
    print("=" * 60)
    print("🧪 DEMO: OPERASI DASAR PAILLIER")
    print("=" * 60)
    
    # Inisialisasi dengan kunci kecil untuk demo cepat
    paillier = PaillierCore(bit_length=1024)
    
    print("\n📊 Informasi Sistem:")
    info = paillier.get_key_info()
    print(f"  🔑 Security level: {info['security_level']}")
    print(f"  📏 n bit length: {info['n_bit_length']}")
    
    print("\n🔐 TEST 1: Enkripsi dan Dekripsi")
    print("-" * 40)
    
    test_values = [42, 1000, 999999]
    
    for value in test_values:
        print(f"\n📤 Mengenkripsi: {value}")
        
        start_time = time.time()
        encrypted = paillier.encrypt(value)
        encrypt_time = (time.time() - start_time) * 1000
        
        print(f"  ⏱️  Waktu enkripsi: {encrypt_time:.2f} ms")
        print(f"  🔒 Ciphertext: {str(encrypted)[:50]}...")
        
        start_time = time.time()
        decrypted = paillier.decrypt(encrypted)
        decrypt_time = (time.time() - start_time) * 1000
        
        print(f"  ⏱️  Waktu dekripsi: {decrypt_time:.2f} ms")
        print(f"  📥 Hasil: {decrypted}")
        print(f"  ✅ Berhasil: {value == decrypted}")
    
    print("\n🧮 TEST 2: Penjumlahan Homomorphic")
    print("-" * 40)
    
    a, b = 150, 250
    print(f"\n🔢 a = {a}, b = {b}")
    
    enc_a = paillier.encrypt(a)
    enc_b = paillier.encrypt(b)
    
    start_time = time.time()
    enc_sum = paillier.homomorphic_add(enc_a, enc_b)
    add_time = (time.time() - start_time) * 1000
    
    result = paillier.decrypt(enc_sum)
    
    print(f"  ⏱️  Waktu penjumlahan homomorphic: {add_time:.2f} ms")
    print(f"  🎯 Hasil: {result}")
    print(f"  ✅ Benar: {result == a + b}")
    
    print("\n✖️ TEST 3: Perkalian Konstanta Homomorphic")
    print("-" * 40)
    
    value = 100
    multiplier = 5
    
    print(f"\n🔢 value = {value}, multiplier = {multiplier}")
    
    enc_value = paillier.encrypt(value)
    
    start_time = time.time()
    enc_product = paillier.homomorphic_multiply_constant(enc_value, multiplier)
    mult_time = (time.time() - start_time) * 1000
    
    result = paillier.decrypt(enc_product)
    
    print(f"  ⏱️  Waktu perkalian homomorphic: {mult_time:.2f} ms")
    print(f"  🎯 Hasil: {result}")
    print(f"  ✅ Benar: {result == value * multiplier}")


def demo_healthcare_analytics():
    """Demo lengkap healthcare analytics."""
    print("\n" + "=" * 60)
    print("🏥 DEMO: HEALTHCARE ANALYTICS")
    print("=" * 60)
    
    # Inisialisasi sistem
    healthcare = HealthcareAnalytics(bit_length=1024)
    
    # Data dummy rumah sakit
    hospital_data = {
        "RSUP Dr. Sardjito": [
            {"age": 45, "treatment_cost": 5000000, "length_of_stay": 3, "diagnosis": "Diabetes"},
            {"age": 62, "treatment_cost": 8500000, "length_of_stay": 7, "diagnosis": "Hipertensi"},
            {"age": 38, "treatment_cost": 3200000, "length_of_stay": 2, "diagnosis": "Gastritis"},
            {"age": 55, "treatment_cost": 12000000, "length_of_stay": 10, "diagnosis": "Stroke"}
        ],
        "RS Cipto Mangunkusumo": [
            {"age": 41, "treatment_cost": 7500000, "length_of_stay": 5, "diagnosis": "Pneumonia"},
            {"age": 67, "treatment_cost": 15000000, "length_of_stay": 14, "diagnosis": "Kanker"},
            {"age": 29, "treatment_cost": 2800000, "length_of_stay": 1, "diagnosis": "Appendisitis"},
            {"age": 52, "treatment_cost": 9200000, "length_of_stay": 6, "diagnosis": "Diabetes"}
        ],
        "RSUD Dr. Soetomo": [
            {"age": 48, "treatment_cost": 6700000, "length_of_stay": 4, "diagnosis": "Hipertensi"},
            {"age": 71, "treatment_cost": 18000000, "length_of_stay": 18, "diagnosis": "Jantung"},
            {"age": 33, "treatment_cost": 4100000, "length_of_stay": 2, "diagnosis": "Pneumonia"},
            {"age": 59, "treatment_cost": 11500000, "length_of_stay": 8, "diagnosis": "Stroke"}
        ]
    }
    
    # Input data ke sistem
    for hospital, patients in hospital_data.items():
        healthcare.add_hospital_data(hospital, patients)
    
    # Analisis nasional
    avg_age = healthcare.calculate_national_average_age()
    total_cost = healthcare.calculate_total_healthcare_cost()
    
    # Deteksi anomali
    cost_anomaly = healthcare.detect_regional_anomaly('treatment_cost', 1.5)
    
    print("\n📋 RINGKASAN ANALISIS NASIONAL:")
    print("=" * 40)
    print(f"🎯 Rata-rata usia pasien: {avg_age:.1f} tahun")
    print(f"💰 Total biaya healthcare: Rp {total_cost:,}")
    print(f"🚨 Rumah sakit dengan anomali biaya: {len(cost_anomaly['anomalies'])}")
    
    for hospital, anomaly in cost_anomaly['anomalies'].items():
        print(f"  ⚠️  {hospital}: {anomaly['ratio']:.1f}x rata-rata ({anomaly['severity']})")


def demo_financial_computation():
    """Demo financial computation dengan data transaksi."""
    print("\n" + "=" * 60)
    print("🏦 DEMO: FINANCIAL COMPUTATION")
    print("=" * 60)
    
    # Inisialisasi sistem
    financial = FinancialComputation(bit_length=1024)
    
    # Generate data transaksi dummy
    banks_transactions = {
        "Bank Mandiri": [random.randint(10000, 50000000) for _ in range(50)],
        "Bank BCA": [random.randint(5000, 100000000) for _ in range(45)],
        "Bank BRI": [random.randint(15000, 25000000) for _ in range(60)]
    }
    
    # Tambahkan beberapa transaksi "mencurigakan"
    banks_transactions["Bank Mandiri"].extend([150000000, 200000000])
    banks_transactions["Bank BCA"].extend([180000000])
    
    # Input data ke sistem
    for bank, transactions in banks_transactions.items():
        financial.add_bank_transactions(bank, transactions)
    
    # Analisis finansial
    total_volume = financial.calculate_total_transaction_volume()
    avg_transaction = financial.calculate_average_transaction()
    fraud_scores = financial.fraud_detection_scoring(100000000)
    
    print("\n📋 RINGKASAN ANALISIS FINANSIAL:")
    print("=" * 40)
    print(f"💵 Total volume transaksi: Rp {total_volume:,}")
    print(f"📊 Rata-rata transaksi: Rp {avg_transaction:,.0f}")
    print(f"🕵️ Bank dengan risk tinggi: {sum(1 for s in fraud_scores.values() if s['risk_level'] == 'HIGH')}")
    
    for bank, score in fraud_scores.items():
        print(f"  🏦 {bank}: {score['risk_score']:.1f}% risk ({score['risk_level']})")


def run_all_demos():
    """Jalankan semua demonstrasi secara berurutan."""
    print("🚀 MEMULAI SEMUA DEMONSTRASI PAILLIER")
    print("=" * 60)
    print("Estimasi waktu: 3-5 menit")
    
    input("\n🎯 Tekan ENTER untuk memulai...")
    
    try:
        demo_basic_operations()
        demo_healthcare_analytics()
        demo_financial_computation()
        
        print("\n" + "=" * 60)
        print("🎉 SEMUA DEMO SELESAI!")
        print("=" * 60)
        print("✅ Algoritma Paillier berhasil didemonstrasikan")
        print("✅ Privacy-preserving computation terbukti efektif")
        print("✅ Aplikasi real-world dapat diimplementasikan")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    run_all_demos()