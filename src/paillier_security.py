"""
PAILLIER SECURITY - Analisis Keamanan dan Best Practices
=======================================================

File ini berisi tools untuk analisis keamanan algoritma Paillier,
validasi implementasi, dan demonstrasi best practices.

Dependencies: paillier_core.py
"""

import random
import math
import hashlib
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from paillier_core import PaillierCore


@dataclass
class SecurityTestResult:
    """Data class untuk hasil security testing."""
    test_name: str
    passed: bool
    details: str
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    recommendation: str


class PaillierSecurityAnalyzer:
    """
    Kelas untuk analisis keamanan implementasi Paillier.
    """
    
    def __init__(self, paillier_instance: PaillierCore):
        """
        Inisialisasi security analyzer.
        
        Args:
            paillier_instance: Instance Paillier yang akan dianalisis
        """
        self.paillier = paillier_instance
        self.test_results = []
    
    def test_probabilistic_encryption(self, iterations: int = 100) -> SecurityTestResult:
        """
        Test apakah enkripsi bersifat probabilistic (menghasilkan output berbeda).
        
        Args:
            iterations: Jumlah enkripsi yang akan ditest
            
        Returns:
            Hasil test probabilistic encryption
        """
        print("🎲 Testing probabilistic encryption...")
        
        message = 12345
        ciphertexts = set()
        
        for i in range(iterations):
            encrypted = self.paillier.encrypt(message)
            ciphertexts.add(encrypted)
        
        unique_ratio = len(ciphertexts) / iterations
        
        if unique_ratio > 0.95:  # Hampir semua enkripsi unik
            result = SecurityTestResult(
                test_name="Probabilistic Encryption",
                passed=True,
                details=f"{len(ciphertexts)}/{iterations} enkripsi unik ({unique_ratio:.1%})",
                risk_level="LOW",
                recommendation="Probabilistic encryption berfungsi dengan baik"
            )
        elif unique_ratio > 0.8:
            result = SecurityTestResult(
                test_name="Probabilistic Encryption",
                passed=True,
                details=f"{len(ciphertexts)}/{iterations} enkripsi unik ({unique_ratio:.1%})",
                risk_level="MEDIUM",
                recommendation="Periksa quality random number generator"
            )
        else:
            result = SecurityTestResult(
                test_name="Probabilistic Encryption",
                passed=False,
                details=f"Hanya {len(ciphertexts)}/{iterations} enkripsi unik ({unique_ratio:.1%})",
                risk_level="HIGH",
                recommendation="CRITICAL: Random number generator tidak memadai!"
            )
        
        print(f"  📊 Unique ciphertexts: {len(ciphertexts)}/{iterations} ({unique_ratio:.1%})")
        self.test_results.append(result)
        return result
    
    def test_homomorphic_correctness(self, test_cases: int = 50) -> SecurityTestResult:
        """
        Test correctness operasi homomorphic.
        
        Args:
            test_cases: Jumlah test cases
            
        Returns:
            Hasil test homomorphic correctness
        """
        print("🧮 Testing homomorphic correctness...")
        
        failed_cases = []
        
        for i in range(test_cases):
            # Generate random test values
            a = random.randint(1, min(1000000, self.paillier.public_key['n'] // 10))
            b = random.randint(1, min(1000000, self.paillier.public_key['n'] // 10))
            k = random.randint(2, 100)
            
            try:
                # Test homomorphic addition
                enc_a = self.paillier.encrypt(a)
                enc_b = self.paillier.encrypt(b)
                enc_sum = self.paillier.homomorphic_add(enc_a, enc_b)
                result_sum = self.paillier.decrypt(enc_sum)
                expected_sum = (a + b) % self.paillier.public_key['n']
                
                if result_sum != expected_sum:
                    failed_cases.append(f"Addition: {a}+{b} = {result_sum} != {expected_sum}")
                
                # Test homomorphic scalar multiplication
                enc_mult = self.paillier.homomorphic_multiply_constant(enc_a, k)
                result_mult = self.paillier.decrypt(enc_mult)
                expected_mult = (a * k) % self.paillier.public_key['n']
                
                if result_mult != expected_mult:
                    failed_cases.append(f"Multiplication: {a}*{k} = {result_mult} != {expected_mult}")
                    
            except Exception as e:
                failed_cases.append(f"Exception in case {i}: {str(e)}")
        
        if not failed_cases:
            result = SecurityTestResult(
                test_name="Homomorphic Correctness",
                passed=True,
                details=f"Semua {test_cases} test cases berhasil",
                risk_level="LOW",
                recommendation="Operasi homomorphic berfungsi dengan benar"
            )
        else:
            result = SecurityTestResult(
                test_name="Homomorphic Correctness",
                passed=False,
                details=f"{len(failed_cases)} dari {test_cases} test cases gagal",
                risk_level="CRITICAL",
                recommendation=f"CRITICAL: Implementasi bermasalah - {failed_cases[:3]}"
            )
        
        print(f"  📊 Test cases passed: {test_cases - len(failed_cases)}/{test_cases}")
        self.test_results.append(result)
        return result
    
    def test_key_strength(self) -> SecurityTestResult:
        """
        Analisis kekuatan kunci yang digunakan.
        
        Returns:
            Hasil analisis key strength
        """
        print("🔑 Testing key strength...")
        
        n = self.paillier.public_key['n']
        bit_length = n.bit_length()
        
        # Analisis ukuran kunci
        if bit_length >= 3072:
            security_level = "VERY HIGH"
            risk_level = "LOW"
            recommendation = "Kunci sangat kuat untuk semua aplikasi"
        elif bit_length >= 2048:
            security_level = "HIGH"
            risk_level = "LOW"
            recommendation = "Kunci memadai untuk aplikasi production"
        elif bit_length >= 1024:
            security_level = "MEDIUM"
            risk_level = "MEDIUM"
            recommendation = "Kunci cukup untuk development, upgrade untuk production"
        else:
            security_level = "LOW"
            risk_level = "HIGH"
            recommendation = "PERINGATAN: Kunci terlalu lemah untuk penggunaan serius"
        
        # Check apakah n adalah produk dari dua prima (basic check)
        is_valid_composite = True
        
        # Test dengan small primes
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        small_factors = [p for p in small_primes if n % p == 0]
        
        if small_factors:
            is_valid_composite = False
            risk_level = "CRITICAL"
            recommendation = f"CRITICAL: n memiliki faktor kecil {small_factors}"
        
        result = SecurityTestResult(
            test_name="Key Strength Analysis",
            passed=bit_length >= 1024 and is_valid_composite,
            details=f"{bit_length}-bit key, security level: {security_level}",
            risk_level=risk_level,
            recommendation=recommendation
        )
        
        print(f"  📊 Key size: {bit_length} bits ({security_level})")
        if small_factors:
            print(f"  ⚠️  Small factors found: {small_factors}")
        
        self.test_results.append(result)
        return result
    
    def test_semantic_security(self, iterations: int = 50) -> SecurityTestResult:
        """
        Test semantic security dengan analyzing ciphertext patterns.
        
        Args:
            iterations: Jumlah iterasi test
            
        Returns:
            Hasil test semantic security
        """
        print("🔒 Testing semantic security...")
        
        # Test 1: Enkripsi nilai yang sama menghasilkan ciphertext berbeda
        message = 12345
        ciphertexts = [self.paillier.encrypt(message) for _ in range(iterations)]
        unique_ciphertexts = len(set(ciphertexts))
        
        # Test 2: Ciphertext dari nilai berbeda tidak memiliki pola yang obvious
        messages = list(range(1, iterations + 1))
        encrypted_messages = [self.paillier.encrypt(msg) for msg in messages]
        
        # Analisis distribusi bit (simplified test)
        bit_distributions = []
        for enc in encrypted_messages:
            # Hitung distribusi bit 1 dan 0
            binary_str = bin(enc)[2:]  # Remove '0b' prefix
            ones_ratio = binary_str.count('1') / len(binary_str)
            bit_distributions.append(ones_ratio)
        
        # Statistical analysis
        avg_ones_ratio = sum(bit_distributions) / len(bit_distributions)
        variance = sum((x - avg_ones_ratio) ** 2 for x in bit_distributions) / len(bit_distributions)
        
        # Evaluasi
        unique_ratio = unique_ciphertexts / iterations
        bit_balance = abs(avg_ones_ratio - 0.5)  # Ideal adalah 0.5 (balanced)
        
        if unique_ratio > 0.95 and bit_balance < 0.1:
            result = SecurityTestResult(
                test_name="Semantic Security",
                passed=True,
                details=f"Unique ratio: {unique_ratio:.1%}, Bit balance: {bit_balance:.3f}",
                risk_level="LOW",
                recommendation="Semantic security properties baik"
            )
        elif unique_ratio > 0.8:
            result = SecurityTestResult(
                test_name="Semantic Security",
                passed=True,
                details=f"Unique ratio: {unique_ratio:.1%}, Bit balance: {bit_balance:.3f}",
                risk_level="MEDIUM",
                recommendation="Semantic security memadai, monitor randomness quality"
            )
        else:
            result = SecurityTestResult(
                test_name="Semantic Security",
                passed=False,
                details=f"Unique ratio: {unique_ratio:.1%}, Bit balance: {bit_balance:.3f}",
                risk_level="HIGH",
                recommendation="PERINGATAN: Possible issues dengan semantic security"
            )
        
        print(f"  📊 Unique ciphertexts: {unique_ciphertexts}/{iterations}")
        print(f"  📊 Bit balance: {bit_balance:.3f} (closer to 0 is better)")
        
        self.test_results.append(result)
        return result
    
    def test_input_validation(self) -> SecurityTestResult:
        """
        Test input validation untuk mencegah serangan.
        
        Returns:
            Hasil test input validation
        """
        print("🛡️ Testing input validation...")
        
        validation_issues = []
        
        # Test 1: Negative values
        try:
            self.paillier.encrypt(-1)
            validation_issues.append("Accepts negative values")
        except ValueError:
            pass  # Expected behavior
        
        # Test 2: Values >= n
        try:
            large_value = self.paillier.public_key['n'] + 1
            self.paillier.encrypt(large_value)
            validation_issues.append("Accepts values >= n")
        except ValueError:
            pass  # Expected behavior
        
        # Test 3: Non-integer values (if applicable)
        try:
            self.paillier.encrypt(3.14)
            validation_issues.append("Accepts non-integer values")
        except (ValueError, TypeError):
            pass  # Expected behavior
        
        # Test 4: Very large values that could cause overflow
        try:
            huge_value = 2 ** 4096  # Extremely large
            if huge_value < self.paillier.public_key['n']:
                self.paillier.encrypt(huge_value)
        except (ValueError, OverflowError, MemoryError):
            pass  # Expected behavior for very large values
        
        if not validation_issues:
            result = SecurityTestResult(
                test_name="Input Validation",
                passed=True,
                details="Semua input validation tests passed",
                risk_level="LOW",
                recommendation="Input validation implementation baik"
            )
        else:
            result = SecurityTestResult(
                test_name="Input Validation",
                passed=False,
                details=f"Issues found: {', '.join(validation_issues)}",
                risk_level="MEDIUM",
                recommendation="Perbaiki input validation untuk mencegah serangan"
            )
        
        print(f"  📊 Validation issues: {len(validation_issues)}")
        for issue in validation_issues:
            print(f"    ⚠️  {issue}")
        
        self.test_results.append(result)
        return result
    
    def test_side_channel_resistance(self, iterations: int = 100) -> SecurityTestResult:
        """
        Basic test untuk resistance terhadap timing attacks.
        
        Args:
            iterations: Jumlah timing measurements
            
        Returns:
            Hasil test side-channel resistance
        """
        print("⏱️ Testing side-channel resistance...")
        
        # Test timing variance untuk enkripsi values yang berbeda
        small_values = [random.randint(1, 1000) for _ in range(iterations // 2)]
        large_values = [random.randint(100000, min(1000000, self.paillier.public_key['n'] // 10)) 
                       for _ in range(iterations // 2)]
        
        small_times = []
        large_times = []
        
        # Measure encryption times untuk small values
        for value in small_values:
            start_time = time.perf_counter()
            self.paillier.encrypt(value)
            end_time = time.perf_counter()
            small_times.append(end_time - start_time)
        
        # Measure encryption times untuk large values
        for value in large_values:
            start_time = time.perf_counter()
            self.paillier.encrypt(value)
            end_time = time.perf_counter()
            large_times.append(end_time - start_time)
        
        # Statistical analysis
        avg_small = sum(small_times) / len(small_times)
        avg_large = sum(large_times) / len(large_times)
        
        timing_difference = abs(avg_large - avg_small) / avg_small
        
        # Evaluate
        if timing_difference < 0.1:  # Less than 10% difference
            result = SecurityTestResult(
                test_name="Side-Channel Resistance",
                passed=True,
                details=f"Timing difference: {timing_difference:.1%}",
                risk_level="LOW",
                recommendation="Low timing variance, good resistance"
            )
        elif timing_difference < 0.3:
            result = SecurityTestResult(
                test_name="Side-Channel Resistance",
                passed=True,
                details=f"Timing difference: {timing_difference:.1%}",
                risk_level="MEDIUM",
                recommendation="Moderate timing variance, consider constant-time implementation"
            )
        else:
            result = SecurityTestResult(
                test_name="Side-Channel Resistance",
                passed=False,
                details=f"Timing difference: {timing_difference:.1%}",
                risk_level="HIGH",
                recommendation="PERINGATAN: Significant timing variance, vulnerable to timing attacks"
            )
        
        print(f"  📊 Avg small value time: {avg_small*1000:.2f}ms")
        print(f"  📊 Avg large value time: {avg_large*1000:.2f}ms")
        print(f"  📊 Timing difference: {timing_difference:.1%}")
        
        self.test_results.append(result)
        return result


class SecurityBestPractices:
    """
    Kelas untuk demonstrasi dan validasi security best practices.
    """
    
    @staticmethod
    def demonstrate_secure_key_generation(bit_length: int = 2048) -> Dict[str, any]:
        """
        Demonstrasi secure key generation dengan best practices.
        
        Args:
            bit_length: Ukuran kunci yang akan dibuat
            
        Returns:
            Dictionary dengan informasi key generation
        """
        print(f"🔐 SECURE KEY GENERATION DEMO ({bit_length}-bit)")
        print("=" * 50)
        
        # Best Practice 1: Adequate key size
        if bit_length < 2048:
            print("  ⚠️  WARNING: Key size < 2048 bits tidak direkomendasikan untuk production")
        
        # Best Practice 2: Secure random number generation
        print("  🎲 Using secure random number generation...")
        start_time = time.time()
        
        paillier = PaillierCore(bit_length)
        
        generation_time = time.time() - start_time
        
        # Best Practice 3: Key validation
        print("  ✅ Validating generated keys...")
        
        # Validate key components
        n = paillier.public_key['n']
        g = paillier.public_key['g']
        lambda_val = paillier.private_key['lambda']
        
        validations = {
            'n_bit_length': n.bit_length(),
            'n_is_odd': n % 2 == 1,
            'g_value': g,
            'lambda_positive': lambda_val > 0,
            'gcd_check': math.gcd(lambda_val, n) == 1
        }
        
        print(f"  📊 Key validation results:")
        for check, result in validations.items():
            status = "✅" if result else "❌"
            print(f"    {status} {check}: {result}")
        
        # Best Practice 4: Key strength assessment
        security_bits = bit_length // 2  # Approximate security level
        print(f"  🔒 Estimated security level: ~{security_bits} bits")
        
        return {
            'paillier_instance': paillier,
            'generation_time': generation_time,
            'validations': validations,
            'security_level': security_bits
        }
    
    @staticmethod
    def demonstrate_secure_key_storage() -> Dict[str, str]:
        """
        Demonstrasi best practices untuk key storage.
        
        Returns:
            Dictionary dengan recommendations untuk key storage
        """
        print("\n🔒 SECURE KEY STORAGE BEST PRACTICES")
        print("=" * 50)
        
        recommendations = {
            "Environment Separation": "Pisahkan public dan private keys, simpan private key di secure environment",
            "Encryption at Rest": "Enkripsi private keys dengan master key atau password",
            "Access Control": "Implementasi strict access control, principle of least privilege",
            "Key Rotation": "Regular key rotation sesuai security policy organisasi",
            "Backup Strategy": "Secure backup private keys dengan encryption dan geographic distribution",
            "HSM Usage": "Gunakan Hardware Security Modules untuk production environment",
            "Audit Logging": "Log semua akses dan operasi pada private keys",
            "Key Escrow": "Implementasi key escrow untuk disaster recovery"
        }
        
        for practice, description in recommendations.items():
            print(f"  🔹 {practice}: {description}")
        
        # Contoh implementasi basic key protection
        print(f"\n💡 CONTOH: Basic Key Protection")
        
        paillier = PaillierCore(1024)  # Small key for demo
        
        # Simulate key serialization dengan hashing untuk integrity
        public_key_str = str(paillier.public_key)
        private_key_str = str(paillier.private_key)
        
        # Generate checksums
        pub_checksum = hashlib.sha256(public_key_str.encode()).hexdigest()[:16]
        priv_checksum = hashlib.sha256(private_key_str.encode()).hexdigest()[:16]
        
        print(f"  📄 Public key checksum: {pub_checksum}")
        print(f"  🔐 Private key checksum: {priv_checksum}")
        print(f"  💡 Gunakan checksum untuk verify integrity saat loading keys")
        
        return recommendations
    
    @staticmethod
    def demonstrate_secure_operations() -> List[str]:
        """
        Demonstrasi secure operations practices.
        
        Returns:
            List praktik secure operations
        """
        print("\n🛡️ SECURE OPERATIONS PRACTICES")
        print("=" * 50)
        
        paillier = PaillierCore(1024)
        
        practices = []
        
        # Practice 1: Input sanitization
        print("  1️⃣ Input Sanitization")
        try:
            # Demonstrate proper input validation
            test_inputs = [-1, 0, 12345, paillier.public_key['n'] + 1]
            for inp in test_inputs:
                try:
                    if inp < 0:
                        raise ValueError("Negative input not allowed")
                    if inp >= paillier.public_key['n']:
                        raise ValueError("Input too large")
                    
                    result = paillier.encrypt(inp)
                    print(f"    ✅ Input {inp}: Valid")
                except ValueError as e:
                    print(f"    ❌ Input {inp}: {e}")
            
            practices.append("Always validate inputs before encryption")
        
        except Exception as e:
            print(f"    ⚠️  Error in input validation demo: {e}")
        
        # Practice 2: Secure random generation
        print("  2️⃣ Secure Random Generation")
        print("    💡 Using system entropy for cryptographic randomness")
        print("    💡 Avoid predictable patterns atau user-provided randomness")
        practices.append("Use cryptographically secure random number generators")
        
        # Practice 3: Memory management
        print("  3️⃣ Memory Management")
        print("    💡 Clear sensitive data from memory after use")
        print("    💡 Avoid storing plaintext and private keys longer than necessary")
        practices.append("Implement secure memory management")
        
        # Practice 4: Error handling
        print("  4️⃣ Secure Error Handling")
        print("    💡 Don't expose sensitive information in error messages")
        print("    💡 Log security events untuk monitoring")
        practices.append("Implement secure error handling without information leakage")
        
        # Practice 5: Performance monitoring
        print("  5️⃣ Performance Monitoring")
        print("    💡 Monitor untuk unusual patterns yang might indicate attacks")
        print("    💡 Implement rate limiting untuk prevent abuse")
        practices.append("Monitor performance patterns untuk security anomalies")
        
        return practices


def run_security_analysis(bit_length: int = 2048) -> None:
    """
    Jalankan analisis keamanan lengkap.
    
    Args:
        bit_length: Ukuran kunci untuk testing
    """
    print("🛡️ PAILLIER SECURITY ANALYSIS SUITE")
    print("=" * 60)
    
    # Create Paillier instance
    print(f"🔧 Creating Paillier instance ({bit_length}-bit)...")
    paillier = PaillierCore(bit_length)
    
    # Initialize security analyzer
    analyzer = PaillierSecurityAnalyzer(paillier)
    
    print("\n🔍 Running security tests...")
    
    # Run all security tests
    test_functions = [
        analyzer.test_probabilistic_encryption,
        analyzer.test_homomorphic_correctness,
        analyzer.test_key_strength,
        analyzer.test_semantic_security,
        analyzer.test_input_validation,
        analyzer.test_side_channel_resistance
    ]
    
    for test_func in test_functions:
        try:
            test_func()
            print("  ✅ Test completed")
        except Exception as e:
            print(f"  ❌ Test failed: {e}")
        print()
    
    # Generate security report
    print("📋 SECURITY ANALYSIS REPORT")
    print("=" * 50)
    
    passed_tests = sum(1 for result in analyzer.test_results if result.passed)
    total_tests = len(analyzer.test_results)
    
    print(f"📊 Overall Score: {passed_tests}/{total_tests} tests passed")
    print()
    
    # Categorize by risk level
    risk_levels = {"LOW": [], "MEDIUM": [], "HIGH": [], "CRITICAL": []}
    
    for result in analyzer.test_results:
        risk_levels[result.risk_level].append(result)
    
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if risk_levels[level]:
            emoji = {"CRITICAL": "🚨", "HIGH": "⚠️", "MEDIUM": "🟡", "LOW": "✅"}[level]
            print(f"{emoji} {level} RISK ({len(risk_levels[level])} items):")
            
            for result in risk_levels[level]:
                status = "✅" if result.passed else "❌"
                print(f"  {status} {result.test_name}: {result.details}")
                if not result.passed or level in ["CRITICAL", "HIGH"]:
                    print(f"    💡 {result.recommendation}")
            print()
    
    # Best practices demonstration
    print("🏆 SECURITY BEST PRACTICES DEMONSTRATION")
    print("=" * 50)
    
    SecurityBestPractices.demonstrate_secure_key_generation(bit_length)
    SecurityBestPractices.demonstrate_secure_key_storage()
    SecurityBestPractices.demonstrate_secure_operations()
    
    print(f"\n🎯 SECURITY RECOMMENDATIONS SUMMARY")
    print("=" * 50)
    
    if bit_length >= 3072:
        print("✅ Excellent key size untuk all applications")
    elif bit_length >= 2048:
        print("✅ Good key size untuk production use")
    else:
        print("⚠️  Consider upgrading key size untuk production")
    
    print("🔹 Implement proper key management dan storage")
    print("🔹 Regular security audits dan penetration testing")
    print("🔹 Monitor untuk unusual patterns atau attacks")
    print("🔹 Keep implementation updated dengan latest security patches")
    print("🔹 Train staff pada cryptographic best practices")


if __name__ == "__main__":
    print("🔒 PAILLIER SECURITY TESTING")
    print("=" * 40)
    
    key_size = input("Enter key size for security analysis (default 2048): ").strip()
    
    try:
        key_size = int(key_size) if key_size else 2048
        if key_size < 512:
            print("⚠️  Minimum key size is 512 bits")
            key_size = 512
        
        run_security_analysis(key_size)
        
    except ValueError:
        print("Invalid input, using default 2048-bit keys")
        run_security_analysis(2048)
    except KeyboardInterrupt:
        print("\n⏹️  Security analysis interrupted")
    except Exception as e:
        print(f"\n❌ Error during security analysis: {e}")