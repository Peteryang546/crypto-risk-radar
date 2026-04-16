#!/usr/bin/env python3
"""
Test SSL fix for API calls
"""

import requests
import urllib3
import ssl
import certifi

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("="*70)
print("TESTING SSL FIXES")
print("="*70)

# Method 1: Try with verify=False
print("\n[Method 1] verify=False")
try:
    resp = requests.get(
        "https://api.coingecko.com/api/v3/ping",
        verify=False,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ SUCCESS - verify=False works")
    else:
        print(f"⚠️  Status {resp.status_code}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Method 2: Try with custom SSL context
print("\n[Method 2] Custom SSL context")
try:
    import ssl
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.poolmanager import PoolManager
    
    class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            kwargs['ssl_context'] = context
            return super().init_poolmanager(*args, **kwargs)
    
    session = requests.Session()
    session.mount('https://', SSLAdapter())
    
    resp = session.get(
        "https://api.coingecko.com/api/v3/ping",
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("✅ SUCCESS - Custom SSL context works")
    else:
        print(f"⚠️  Status {resp.status_code}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Method 3: Check SSL/TLS version
print("\n[Method 3] SSL/TLS Info")
print(f"Python SSL Version: {ssl.OPENSSL_VERSION}")
print(f"Certifi version: {certifi.__version__ if hasattr(certifi, '__version__') else 'N/A'}")
print(f"Certifi path: {certifi.where()}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
If Method 1 or 2 works, we can use that approach.
If both fail, the issue is at the system/network level.

Possible causes:
1. Corporate firewall/proxy blocking HTTPS
2. Outdated SSL certificates
3. Network configuration issues
4. TLS version mismatch

Solutions:
1. Update certificates: pip install --upgrade certifi
2. Use HTTP proxy
3. Contact network administrator
4. Run on different network (e.g., GitHub Actions)
""")
