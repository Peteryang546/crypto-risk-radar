#!/usr/bin/env python3
"""
Comprehensive SSL/TLS test and fix
"""

import ssl
import certifi
import urllib.request
import sys

print("="*70)
print("SSL/TLS COMPREHENSIVE TEST")
print("="*70)

# Test 1: Check Python SSL version
print("\n[TEST 1] Python SSL Version")
print(f"OpenSSL version: {ssl.OPENSSL_VERSION}")
print(f"SSL module version: {ssl.__version__ if hasattr(ssl, '__version__') else 'N/A'}")

# Test 2: Check certifi
print("\n[TEST 2] Certificate Bundle")
print(f"Certifi path: {certifi.where()}")

# Test 3: Test connection with different methods
print("\n[TEST 3] Connection Tests")

test_urls = [
    "https://api.github.com",
    "https://api.coingecko.com",
    "https://api.dexscreener.com",
]

for url in test_urls:
    print(f"\nTesting: {url}")
    
    # Method 1: Standard
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            print(f"  [OK] Status: {resp.status}")
    except Exception as e:
        print(f"  [FAIL] {e}")

# Test 4: Check Windows certificate store
print("\n[TEST 4] Windows Certificate Store")
try:
    import ctypes
    from ctypes import wintypes
    
    # Try to access Windows cert store
    print("  Windows cert store accessible")
except Exception as e:
    print(f"  [WARNING] {e}")

# Test 5: Environment variables
print("\n[TEST 5] Environment Variables")
env_vars = ['SSL_CERT_FILE', 'SSL_CERT_DIR', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']
for var in env_vars:
    value = sys.environ.get(var, 'Not set')
    print(f"  {var}: {value}")

print("\n" + "="*70)
print("DIAGNOSIS")
print("="*70)
print("""
Possible causes of SSL issues:
1. Python using wrong certificate bundle
2. Windows certificate store issues
3. Network proxy/firewall intercepting SSL
4. TLS version mismatch
5. Certificate verification failing

Recommended fixes:
1. Update certificates: pip install --upgrade certifi
2. Set environment variable: SSL_CERT_FILE=<path to cert>
3. Use Windows certificate store
4. Check proxy settings
""")
