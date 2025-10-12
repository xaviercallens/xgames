#!/usr/bin/env python3
"""
Simple HTTP Testing for Bomberman Web Demo
Tests the demo files are accessible via HTTP requests
"""

import http.server
import socketserver
import threading
import time
import sys
from pathlib import Path
import urllib.request
import urllib.error


class HTTPDemoTester:
    """Test web demo via HTTP requests"""
    
    def __init__(self, base_url="http://localhost:8000"):
        """Initialize tester with base URL."""
        self.base_url = base_url
        self.results = []
    
    def log_result(self, test_name, passed, message=""):
        """Log a test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.results.append({
            'test': test_name,
            'passed': passed,
            'message': message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def test_url(self, path, expected_status=200):
        """Test if a URL is accessible."""
        url = f"{self.base_url}/{path}"
        try:
            response = urllib.request.urlopen(url, timeout=10)
            status = response.getcode()
            content_length = len(response.read())
            
            if status == expected_status:
                self.log_result(f"GET {path}", True, 
                              f"Status: {status}, Size: {content_length} bytes")
                return True
            else:
                self.log_result(f"GET {path}", False, 
                              f"Expected {expected_status}, got {status}")
                return False
        except urllib.error.HTTPError as e:
            self.log_result(f"GET {path}", False, f"HTTP Error: {e.code}")
            return False
        except urllib.error.URLError as e:
            self.log_result(f"GET {path}", False, f"URL Error: {e.reason}")
            return False
        except Exception as e:
            self.log_result(f"GET {path}", False, str(e))
            return False
    
    def test_file_content(self, path, expected_content):
        """Test if a file contains expected content."""
        url = f"{self.base_url}/{path}"
        try:
            response = urllib.request.urlopen(url, timeout=10)
            content = response.read().decode('utf-8')
            
            if expected_content in content:
                self.log_result(f"Content Check: {path}", True, 
                              f"Found expected content")
                return True
            else:
                self.log_result(f"Content Check: {path}", False, 
                              f"Expected content not found")
                return False
        except Exception as e:
            self.log_result(f"Content Check: {path}", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all HTTP tests."""
        print("\n" + "=" * 70)
        print("🧪 BOMBERMAN WEB DEMO - HTTP TESTING")
        print("=" * 70)
        print(f"Base URL: {self.base_url}")
        
        # Test main demo page
        self.test_url("docs/play/index.html")
        
        # Test APK file
        self.test_url("docs/play/web_demo.apk")
        
        # Test favicon
        self.test_url("docs/play/favicon.png")
        
        # Test main index
        self.test_url("docs/index.html")
        
        # Test demo HTML
        self.test_url("docs/demo.html")
        
        # Check if index.html contains canvas element
        self.test_file_content("docs/play/index.html", "canvas")
        
        # Check if index.html contains pygame-web script
        self.test_file_content("docs/play/index.html", "pygame-web")
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for r in self.results if r['passed'])
        total = len(self.results)
        
        for result in self.results:
            status = "✅" if result['passed'] else "❌"
            print(f"{status} {result['test']}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed")
            return False


def start_http_server(port=8000, directory=None):
    """Start a simple HTTP server."""
    import os
    
    if directory:
        os.chdir(directory)
    
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Suppress log messages
    
    Handler = QuietHandler
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"🌐 HTTP Server running at http://localhost:{port}")
        print(f"📁 Serving: {os.getcwd()}")
        print(f"🎮 Demo URL: http://localhost:{port}/docs/play/index.html")
        httpd.serve_forever()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Bomberman Web Demo via HTTP")
    parser.add_argument("--url", default="http://localhost:8000",
                       help="Base URL to test")
    parser.add_argument("--serve", action="store_true",
                       help="Start HTTP server before testing")
    parser.add_argument("--port", type=int, default=8000,
                       help="HTTP server port (default: 8000)")
    parser.add_argument("--serve-only", action="store_true",
                       help="Only start server, don't run tests")
    
    args = parser.parse_args()
    
    project_dir = Path(__file__).parent
    
    # Start HTTP server if requested
    if args.serve or args.serve_only:
        print(f"\n🚀 Starting HTTP server from {project_dir}")
        
        if args.serve_only:
            # Run server in main thread (blocking)
            start_http_server(args.port, str(project_dir))
        else:
            # Run server in background thread
            server_thread = threading.Thread(
                target=start_http_server,
                args=(args.port, str(project_dir)),
                daemon=True
            )
            server_thread.start()
            time.sleep(2)  # Give server time to start
    
    if not args.serve_only:
        # Run tests
        tester = HTTPDemoTester(base_url=args.url)
        success = tester.run_all_tests()
        
        print("\n💡 To view the demo in your browser:")
        print(f"   {args.url}/docs/play/index.html")
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
