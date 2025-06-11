"""
PAILLIER PERFORMANCE - Analisis dan Benchmarking Performa
========================================================

File ini berisi tools untuk menganalisis performa algoritma Paillier
dengan berbagai parameter dan skenario penggunaan.

Dependencies: paillier_core.py
"""
import random
import sys
import time
import statistics
import gc
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from paillier_core import PaillierCore


@dataclass
class PerformanceMetrics:
    """Data class untuk menyimpan metrics performa."""
    operation: str
    key_size: int
    min_time: float
    max_time: float
    avg_time: float
    median_time: float
    std_dev: float
    throughput: float  # operations per second
    memory_usage: Optional[int] = None


class PaillierBenchmark:
    """
    Kelas untuk benchmarking performa algoritma Paillier.
    """
    
    def __init__(self):
        """Inisialisasi benchmark suite."""
        self.results = []
        self.test_data = [1, 100, 10000, 1000000, 100000000]
    
    def benchmark_key_generation(self, key_sizes: List[int], iterations: int = 3) -> List[PerformanceMetrics]:
        """
        Benchmark key generation untuk berbagai ukuran kunci.
        
        Args:
            key_sizes: List ukuran kunci yang akan ditest
            iterations: Jumlah iterasi untuk setiap ukuran
            
        Returns:
            List metrics untuk key generation
        """
        print("🔑 BENCHMARKING KEY GENERATION")
        print("=" * 50)
        
        results = []
        
        for key_size in key_sizes:
            print(f"\n📏 Testing key size: {key_size} bits")
            
            times = []
            
            for i in range(iterations):
                print(f"  🔄 Iteration {i+1}/{iterations}...")
                
                # Force garbage collection untuk measurement yang akurat
                gc.collect()
                
                start_time = time.time()
                paillier = PaillierCore(key_size)
                end_time = time.time()
                
                elapsed = end_time - start_time
                times.append(elapsed)
                
                print(f"    ⏱️  Time: {elapsed:.3f} seconds")
                
                # Cleanup
                del paillier
                gc.collect()
            
            # Hitung statistics
            metrics = PerformanceMetrics(
                operation="key_generation",
                key_size=key_size,
                min_time=min(times),
                max_time=max(times),
                avg_time=statistics.mean(times),
                median_time=statistics.median(times),
                std_dev=statistics.stdev(times) if len(times) > 1 else 0,
                throughput=1.0 / statistics.mean(times)  # keys per second
            )
            
            results.append(metrics)
            
            print(f"  📊 Average: {metrics.avg_time:.3f}s")
            print(f"  📊 Std Dev: {metrics.std_dev:.3f}s")
            print(f"  📊 Throughput: {metrics.throughput:.3f} keys/sec")
        
        self.results.extend(results)
        return results
    
    def benchmark_encryption(self, key_sizes: List[int], iterations: int = 100) -> List[PerformanceMetrics]:
        """
        Benchmark encryption untuk berbagai ukuran kunci dan data.
        
        Args:
            key_sizes: List ukuran kunci
            iterations: Jumlah iterasi per test
            
        Returns:
            List metrics untuk encryption
        """
        print("\n🔐 BENCHMARKING ENCRYPTION")
        print("=" * 50)
        
        results = []
        
        for key_size in key_sizes:
            print(f"\n📏 Testing encryption with {key_size}-bit keys")
            
            # Inisialisasi Paillier instance
            paillier = PaillierCore(key_size)
            
            for test_value in self.test_data:
                if test_value >= paillier.public_key['n']:
                    print(f"  ⚠️  Skipping {test_value} (too large for {key_size}-bit key)")
                    continue
                
                print(f"  🔢 Testing with value: {test_value}")
                
                times = []
                
                for i in range(iterations):
                    start_time = time.perf_counter()
                    encrypted = paillier.encrypt(test_value)
                    end_time = time.perf_counter()
                    
                    times.append(end_time - start_time)
                
                # Hitung statistics
                metrics = PerformanceMetrics(
                    operation=f"encryption_value_{test_value}",
                    key_size=key_size,
                    min_time=min(times) * 1000,  # Convert to ms
                    max_time=max(times) * 1000,
                    avg_time=statistics.mean(times) * 1000,
                    median_time=statistics.median(times) * 1000,
                    std_dev=statistics.stdev(times) * 1000 if len(times) > 1 else 0,
                    throughput=1.0 / statistics.mean(times)  # operations per second
                )
                
                results.append(metrics)
                
                print(f"    📊 Avg: {metrics.avg_time:.2f}ms")
                print(f"    📊 Throughput: {metrics.throughput:.1f} ops/sec")
            
            del paillier
            gc.collect()
        
        self.results.extend(results)
        return results
    
    def benchmark_decryption(self, key_sizes: List[int], iterations: int = 100) -> List[PerformanceMetrics]:
        """
        Benchmark decryption untuk berbagai ukuran kunci.
        
        Args:
            key_sizes: List ukuran kunci
            iterations: Jumlah iterasi per test
            
        Returns:
            List metrics untuk decryption
        """
        print("\n🔓 BENCHMARKING DECRYPTION")
        print("=" * 50)
        
        results = []
        
        for key_size in key_sizes:
            print(f"\n📏 Testing decryption with {key_size}-bit keys")
            
            paillier = PaillierCore(key_size)
            
            for test_value in self.test_data:
                if test_value >= paillier.public_key['n']:
                    continue
                
                print(f"  🔢 Testing with value: {test_value}")
                
                # Pre-encrypt value
                encrypted = paillier.encrypt(test_value)
                
                times = []
                
                for i in range(iterations):
                    start_time = time.perf_counter()
                    decrypted = paillier.decrypt(encrypted)
                    end_time = time.perf_counter()
                    
                    times.append(end_time - start_time)
                    
                    # Verify correctness
                    assert decrypted == test_value, f"Decryption failed: {decrypted} != {test_value}"
                
                metrics = PerformanceMetrics(
                    operation=f"decryption_value_{test_value}",
                    key_size=key_size,
                    min_time=min(times) * 1000,
                    max_time=max(times) * 1000,
                    avg_time=statistics.mean(times) * 1000,
                    median_time=statistics.median(times) * 1000,
                    std_dev=statistics.stdev(times) * 1000 if len(times) > 1 else 0,
                    throughput=1.0 / statistics.mean(times)
                )
                
                results.append(metrics)
                
                print(f"    📊 Avg: {metrics.avg_time:.2f}ms")
                print(f"    📊 Throughput: {metrics.throughput:.1f} ops/sec")
            
            del paillier
            gc.collect()
        
        self.results.extend(results)
        return results
    
    def benchmark_homomorphic_operations(self, key_sizes: List[int], iterations: int = 100) -> List[PerformanceMetrics]:
        """
        Benchmark operasi homomorphic (addition dan scalar multiplication).
        
        Args:
            key_sizes: List ukuran kunci
            iterations: Jumlah iterasi per test
            
        Returns:
            List metrics untuk homomorphic operations
        """
        print("\n🧮 BENCHMARKING HOMOMORPHIC OPERATIONS")
        print("=" * 50)
        
        results = []
        
        for key_size in key_sizes:
            print(f"\n📏 Testing homomorphic ops with {key_size}-bit keys")
            
            paillier = PaillierCore(key_size)
            
            # Test homomorphic addition
            print("  ➕ Testing homomorphic addition...")
            
            value1, value2 = 12345, 67890
            if max(value1, value2) < paillier.public_key['n']:
                enc1 = paillier.encrypt(value1)
                enc2 = paillier.encrypt(value2)
                
                times = []
                
                for i in range(iterations):
                    start_time = time.perf_counter()
                    result_enc = paillier.homomorphic_add(enc1, enc2)
                    end_time = time.perf_counter()
                    
                    times.append(end_time - start_time)
                
                # Verify correctness
                result = paillier.decrypt(result_enc)
                assert result == value1 + value2, f"Homomorphic addition failed: {result} != {value1 + value2}"
                
                metrics = PerformanceMetrics(
                    operation="homomorphic_addition",
                    key_size=key_size,
                    min_time=min(times) * 1000,
                    max_time=max(times) * 1000,
                    avg_time=statistics.mean(times) * 1000,
                    median_time=statistics.median(times) * 1000,
                    std_dev=statistics.stdev(times) * 1000 if len(times) > 1 else 0,
                    throughput=1.0 / statistics.mean(times)
                )
                
                results.append(metrics)
                
                print(f"    📊 Avg: {metrics.avg_time:.3f}ms")
                print(f"    📊 Throughput: {metrics.throughput:.1f} ops/sec")
            
            # Test homomorphic scalar multiplication
            print("  ✖️ Testing homomorphic scalar multiplication...")
            
            value = 12345
            scalar = 5
            
            if value < paillier.public_key['n']:
                enc_value = paillier.encrypt(value)
                
                times = []
                
                for i in range(iterations):
                    start_time = time.perf_counter()
                    result_enc = paillier.homomorphic_multiply_constant(enc_value, scalar)
                    end_time = time.perf_counter()
                    
                    times.append(end_time - start_time)
                
                # Verify correctness
                result = paillier.decrypt(result_enc)
                expected = (value * scalar) % paillier.public_key['n']
                assert result == expected, f"Homomorphic multiplication failed: {result} != {expected}"
                
                metrics = PerformanceMetrics(
                    operation="homomorphic_scalar_mult",
                    key_size=key_size,
                    min_time=min(times) * 1000,
                    max_time=max(times) * 1000,
                    avg_time=statistics.mean(times) * 1000,
                    median_time=statistics.median(times) * 1000,
                    std_dev=statistics.stdev(times) * 1000 if len(times) > 1 else 0,
                    throughput=1.0 / statistics.mean(times)
                )
                
                results.append(metrics)
                
                print(f"    📊 Avg: {metrics.avg_time:.3f}ms")
                print(f"    📊 Throughput: {metrics.throughput:.1f} ops/sec")
            
            del paillier
            gc.collect()
        
        self.results.extend(results)
        return results
    
    def benchmark_batch_operations(self, key_size: int = 2048, batch_sizes: List[int] = None) -> List[PerformanceMetrics]:
        """
        Benchmark batch operations untuk mengukur throughput.
        
        Args:
            key_size: Ukuran kunci untuk testing
            batch_sizes: List ukuran batch yang akan ditest
            
        Returns:
            List metrics untuk batch operations
        """
        if batch_sizes is None:
            batch_sizes = [10, 50, 100, 500, 1000]
        
        print(f"\n📦 BENCHMARKING BATCH OPERATIONS ({key_size}-bit)")
        print("=" * 50)
        
        results = []
        paillier = PaillierCore(key_size)
        
        for batch_size in batch_sizes:
            print(f"\n📊 Testing batch size: {batch_size}")
            
            # Generate test data
            test_values = [random.randint(1, 1000000) for _ in range(batch_size)]
            
            # Benchmark batch encryption
            print("  🔐 Batch encryption...")
            start_time = time.time()
            encrypted_values = [paillier.encrypt(value) for value in test_values]
            encryption_time = time.time() - start_time
            
            # Benchmark batch decryption
            print("  🔓 Batch decryption...")
            start_time = time.time()
            decrypted_values = [paillier.decrypt(enc) for enc in encrypted_values]
            decryption_time = time.time() - start_time
            
            # Verify correctness
            assert decrypted_values == test_values, "Batch operation verification failed"
            
            # Benchmark batch homomorphic addition
            print("  ➕ Batch homomorphic addition...")
            if len(encrypted_values) >= 2:
                start_time = time.time()
                # Sum all encrypted values
                result_enc = encrypted_values[0]
                for enc in encrypted_values[1:]:
                    result_enc = paillier.homomorphic_add(result_enc, enc)
                homomorphic_time = time.time() - start_time
                
                # Verify
                expected_sum = sum(test_values) % paillier.public_key['n']
                actual_sum = paillier.decrypt(result_enc)
                assert actual_sum == expected_sum, "Batch homomorphic addition failed"
            else:
                homomorphic_time = 0
            
            # Create metrics
            enc_metrics = PerformanceMetrics(
                operation=f"batch_encryption_{batch_size}",
                key_size=key_size,
                min_time=encryption_time * 1000,
                max_time=encryption_time * 1000,
                avg_time=(encryption_time / batch_size) * 1000,
                median_time=(encryption_time / batch_size) * 1000,
                std_dev=0,
                throughput=batch_size / encryption_time
            )
            
            dec_metrics = PerformanceMetrics(
                operation=f"batch_decryption_{batch_size}",
                key_size=key_size,
                min_time=decryption_time * 1000,
                max_time=decryption_time * 1000,
                avg_time=(decryption_time / batch_size) * 1000,
                median_time=(decryption_time / batch_size) * 1000,
                std_dev=0,
                throughput=batch_size / decryption_time
            )
            
            if homomorphic_time > 0:
                homo_metrics = PerformanceMetrics(
                    operation=f"batch_homomorphic_{batch_size}",
                    key_size=key_size,
                    min_time=homomorphic_time * 1000,
                    max_time=homomorphic_time * 1000,
                    avg_time=(homomorphic_time / (batch_size - 1)) * 1000,
                    median_time=(homomorphic_time / (batch_size - 1)) * 1000,
                    std_dev=0,
                    throughput=(batch_size - 1) / homomorphic_time
                )
                results.append(homo_metrics)
            
            results.extend([enc_metrics, dec_metrics])
            
            print(f"    📊 Encryption throughput: {enc_metrics.throughput:.1f} ops/sec")
            print(f"    📊 Decryption throughput: {dec_metrics.throughput:.1f} ops/sec")
            if homomorphic_time > 0:
                print(f"    📊 Homomorphic throughput: {homo_metrics.throughput:.1f} ops/sec")
        
        self.results.extend(results)
        return results
    
    def memory_usage_analysis(self, key_sizes: List[int]) -> Dict[int, Dict[str, int]]:
        """
        Analisis penggunaan memory untuk berbagai ukuran kunci.
        
        Args:
            key_sizes: List ukuran kunci yang akan dianalisis
            
        Returns:
            Dictionary dengan informasi memory usage
        """
        print("\n💾 MEMORY USAGE ANALYSIS")
        print("=" * 50)
        
        import sys
        memory_stats = {}
        
        for key_size in key_sizes:
            print(f"\n📏 Analyzing memory for {key_size}-bit keys")
            
            # Measure key generation memory
            gc.collect()
            initial_objects = len(gc.get_objects())
            
            paillier = PaillierCore(key_size)
            
            after_keygen_objects = len(gc.get_objects())
            
            # Measure sizes
            public_key_size = sys.getsizeof(paillier.public_key)
            private_key_size = sys.getsizeof(paillier.private_key)
            n_squared_size = sys.getsizeof(paillier.n_squared)
            
            # Measure ciphertext size
            test_value = 12345
            if test_value < paillier.public_key['n']:
                encrypted = paillier.encrypt(test_value)
                ciphertext_size = sys.getsizeof(encrypted)
                ciphertext_str_size = len(str(encrypted))
            else:
                ciphertext_size = 0
                ciphertext_str_size = 0
            
            memory_stats[key_size] = {
                'public_key_bytes': public_key_size,
                'private_key_bytes': private_key_size,
                'n_squared_bytes': n_squared_size,
                'ciphertext_bytes': ciphertext_size,
                'ciphertext_str_length': ciphertext_str_size,
                'objects_created': after_keygen_objects - initial_objects,
                'total_system_bytes': public_key_size + private_key_size + n_squared_size
            }
            
            print(f"  🔑 Public key: {public_key_size:,} bytes")
            print(f"  🔒 Private key: {private_key_size:,} bytes")
            print(f"  📊 n²: {n_squared_size:,} bytes")
            print(f"  📦 Ciphertext: {ciphertext_size:,} bytes ({ciphertext_str_size:,} chars)")
            print(f"  🧠 Total system: {memory_stats[key_size]['total_system_bytes']:,} bytes")
            
            del paillier
            gc.collect()
        
        return memory_stats
    
    def scalability_analysis(self, base_key_size: int = 2048, data_sizes: List[int] = None) -> Dict:
        """
        Analisis skalabilitas untuk volume data yang berbeda.
        
        Args:
            base_key_size: Ukuran kunci untuk testing
            data_sizes: List ukuran dataset yang akan ditest
            
        Returns:
            Dictionary hasil analisis skalabilitas
        """
        if data_sizes is None:
            data_sizes = [100, 500, 1000, 5000, 10000]
        
        print(f"\n📈 SCALABILITY ANALYSIS ({base_key_size}-bit)")
        print("=" * 50)
        
        paillier = PaillierCore(base_key_size)
        scalability_results = {}
        
        for data_size in data_sizes:
            print(f"\n📊 Testing with {data_size:,} data points")
            
            # Generate test dataset
            import random
            dataset = [random.randint(1, 100000) for _ in range(data_size)]
            
            # Encryption time
            print("  🔐 Encrypting dataset...")
            start_time = time.time()
            encrypted_dataset = []
            for i, value in enumerate(dataset):
                encrypted_dataset.append(paillier.encrypt(value))
                if (i + 1) % (data_size // 10) == 0:  # Progress indicator
                    progress = ((i + 1) / data_size) * 100
                    print(f"    Progress: {progress:.0f}%")
            encryption_time = time.time() - start_time
            
            # Homomorphic aggregation time
            print("  ➕ Computing homomorphic sum...")
            start_time = time.time()
            total_encrypted = encrypted_dataset[0]
            for enc_value in encrypted_dataset[1:]:
                total_encrypted = paillier.homomorphic_add(total_encrypted, enc_value)
            aggregation_time = time.time() - start_time
            
            # Verification
            start_time = time.time()
            result = paillier.decrypt(total_encrypted)
            decryption_time = time.time() - start_time
            
            expected = sum(dataset) % paillier.public_key['n']
            assert result == expected, f"Scalability test failed: {result} != {expected}"
            
            scalability_results[data_size] = {
                'encryption_time': encryption_time,
                'aggregation_time': aggregation_time,
                'decryption_time': decryption_time,
                'total_time': encryption_time + aggregation_time + decryption_time,
                'encryption_throughput': data_size / encryption_time,
                'aggregation_throughput': (data_size - 1) / aggregation_time,
                'memory_mb': (len(encrypted_dataset) * sys.getsizeof(encrypted_dataset[0])) / (1024 * 1024)
            }
            
            print(f"  ⏱️  Encryption: {encryption_time:.2f}s ({data_size/encryption_time:.1f} ops/sec)")
            print(f"  ⏱️  Aggregation: {aggregation_time:.2f}s ({(data_size-1)/aggregation_time:.1f} ops/sec)")
            print(f"  ⏱️  Decryption: {decryption_time:.2f}s")
            print(f"  💾 Memory: {scalability_results[data_size]['memory_mb']:.1f} MB")
            
            # Cleanup
            del dataset, encrypted_dataset
            gc.collect()
        
        return scalability_results
    
    def generate_performance_report(self) -> str:
        """
        Generate comprehensive performance report.
        
        Returns:
            String berisi laporan performa lengkap
        """
        if not self.results:
            return "No benchmark results available. Run benchmarks first."
        
        report = []
        report.append("=" * 80)
        report.append("📊 PAILLIER CRYPTOSYSTEM PERFORMANCE REPORT")
        report.append("=" * 80)
        
        # Group results by operation type
        operations = {}
        for result in self.results:
            op_type = result.operation.split('_')[0]
            if op_type not in operations:
                operations[op_type] = []
            operations[op_type].append(result)
        
        # Generate report for each operation type
        for op_type, results in operations.items():
            report.append(f"\n🔧 {op_type.upper()} PERFORMANCE")
            report.append("-" * 50)
            
            # Group by key size
            key_sizes = {}
            for result in results:
                if result.key_size not in key_sizes:
                    key_sizes[result.key_size] = []
                key_sizes[result.key_size].append(result)
            
            for key_size in sorted(key_sizes.keys()):
                key_results = key_sizes[key_size]
                report.append(f"\n📏 {key_size}-bit keys:")
                
                for result in key_results:
                    if result.avg_time >= 1000:  # Show in seconds
                        time_str = f"{result.avg_time/1000:.3f}s"
                    else:  # Show in milliseconds
                        time_str = f"{result.avg_time:.2f}ms"
                    
                    report.append(f"  • {result.operation}: {time_str} "
                                f"(throughput: {result.throughput:.1f} ops/sec)")
        
        # Performance recommendations
        report.append(f"\n💡 PERFORMANCE RECOMMENDATIONS")
        report.append("-" * 50)
        
        # Find fastest key size for each operation
        fastest_configs = {}
        for result in self.results:
            op_type = result.operation.split('_')[0]
            if op_type not in fastest_configs or result.throughput > fastest_configs[op_type]['throughput']:
                fastest_configs[op_type] = {
                    'key_size': result.key_size,
                    'throughput': result.throughput,
                    'avg_time': result.avg_time
                }
        
        for op_type, config in fastest_configs.items():
            report.append(f"  🚀 Fastest {op_type}: {config['key_size']}-bit "
                         f"({config['throughput']:.1f} ops/sec)")
        
        # Security vs Performance trade-offs
        report.append(f"\n⚖️  SECURITY VS PERFORMANCE TRADE-OFFS")
        report.append("-" * 50)
        report.append("  • 1024-bit: Fast but minimal security (dev/testing only)")
        report.append("  • 2048-bit: Balanced security and performance (recommended)")
        report.append("  • 3072-bit: High security, moderate performance impact")
        report.append("  • 4096-bit: Maximum security, significant performance cost")
        
        # Use case recommendations
        report.append(f"\n🎯 USE CASE RECOMMENDATIONS")
        report.append("-" * 50)
        report.append("  • Real-time applications: 1024-2048 bit with optimizations")
        report.append("  • Batch processing: 2048-3072 bit")
        report.append("  • High-security applications: 3072+ bit")
        report.append("  • Research/prototyping: 1024 bit for speed")
        
        return "\n".join(report)


def run_comprehensive_benchmark():
    """
    Jalankan benchmark lengkap untuk algoritma Paillier.
    """
    print("🚀 STARTING COMPREHENSIVE PAILLIER BENCHMARK")
    print("=" * 60)
    print("⚠️  Warning: Comprehensive benchmark dapat memakan waktu 10-20 menit")
    print("💡 Untuk testing cepat, gunakan key sizes yang lebih kecil")
    
    # Konfigurasi benchmark
    key_sizes = [1024, 2048]  # Reduced for faster testing
    
    response = input("\n🎯 Lanjutkan dengan benchmark komprehensif? (y/n): ").lower().strip()
    if response != 'y':
        print("Benchmark dibatalkan.")
        return
    
    benchmark = PaillierBenchmark()
    
    try:
        print(f"\n⏱️  Estimated time: {len(key_sizes) * 3} minutes")
        print("📊 Starting benchmark suite...")
        
        # Run benchmarks
        print("\n" + "🔑" * 20 + " KEY GENERATION " + "🔑" * 20)
        benchmark.benchmark_key_generation(key_sizes, iterations=3)
        
        print("\n" + "🔐" * 20 + " ENCRYPTION " + "🔐" * 20)
        benchmark.benchmark_encryption(key_sizes, iterations=50)
        
        print("\n" + "🔓" * 20 + " DECRYPTION " + "🔓" * 20)
        benchmark.benchmark_decryption(key_sizes, iterations=50)
        
        print("\n" + "🧮" * 20 + " HOMOMORPHIC OPS " + "🧮" * 20)
        benchmark.benchmark_homomorphic_operations(key_sizes, iterations=50)
        
        print("\n" + "📦" * 20 + " BATCH OPERATIONS " + "📦" * 20)
        benchmark.benchmark_batch_operations(2048, [10, 50, 100])
        
        print("\n" + "💾" * 20 + " MEMORY ANALYSIS " + "💾" * 20)
        memory_stats = benchmark.memory_usage_analysis(key_sizes)
        
        print("\n" + "📈" * 20 + " SCALABILITY " + "📈" * 20)
        scalability_stats = benchmark.scalability_analysis(2048, [100, 500, 1000])
        
        # Generate and display report
        print("\n" + "📊" * 20 + " FINAL REPORT " + "📊" * 20)
        report = benchmark.generate_performance_report()
        print(report)
        
        # Save report to file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"paillier_benchmark_report_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n💾 Report saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")
        
        print("\n🎉 Benchmark completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Benchmark interrupted by user")
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


def run_quick_benchmark():
    """
    Jalankan benchmark cepat untuk testing dasar.
    """
    print("⚡ QUICK BENCHMARK MODE")
    print("=" * 40)
    
    benchmark = PaillierBenchmark()
    key_sizes = [1024]  # Only test 1024-bit for speed
    
    print("🔑 Testing key generation...")
    benchmark.benchmark_key_generation(key_sizes, iterations=1)
    
    print("\n🔐 Testing encryption...")
    benchmark.benchmark_encryption(key_sizes, iterations=10)
    
    print("\n🔓 Testing decryption...")
    benchmark.benchmark_decryption(key_sizes, iterations=10)
    
    print("\n🧮 Testing homomorphic operations...")
    benchmark.benchmark_homomorphic_operations(key_sizes, iterations=10)
    
    print("\n📊 QUICK RESULTS:")
    for result in benchmark.results:
        if result.avg_time >= 1000:
            time_str = f"{result.avg_time/1000:.3f}s"
        else:
            time_str = f"{result.avg_time:.2f}ms"
        
        print(f"  • {result.operation}: {time_str} ({result.throughput:.1f} ops/sec)")
    
    print("\n✅ Quick benchmark completed!")


if __name__ == "__main__":
    print("🧪 PAILLIER PERFORMANCE TESTING SUITE")
    print("=" * 50)
    
    mode = input("Choose benchmark mode:\n"
                "1. Quick benchmark (1-2 minutes)\n"
                "2. Comprehensive benchmark (10-20 minutes)\n"
                "Enter choice (1 or 2): ").strip()
    
    if mode == "1":
        run_quick_benchmark()
    elif mode == "2":
        run_comprehensive_benchmark()
    else:
        print("Invalid choice. Running quick benchmark...")
        run_quick_benchmark()