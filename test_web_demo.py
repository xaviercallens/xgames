#!/usr/bin/env python3
"""
Automated Browser Testing for Bomberman Web Demo
Tests the live demo using Selenium WebDriver
"""

import time
import sys
import os
from pathlib import Path
import http.server
import socketserver
import threading
import subprocess

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, WebDriverException
except ImportError:
    print("❌ Selenium not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, WebDriverException


class WebDemoTester:
    """Test the Bomberman web demo"""
    
    def __init__(self, url="http://localhost:8000/docs/play/index.html", headless=False):
        """
        Initialize the tester.
        
        Args:
            url: URL to test
            headless: Run browser in headless mode
        """
        self.url = url
        self.headless = headless
        self.driver = None
        self.results = []
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        print("\n🔧 Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Essential options for web demo
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
        
        # Enable WebGL and audio
        chrome_options.add_argument("--enable-webgl")
        chrome_options.add_argument("--use-gl=swiftshader")
        
        # Disable security features that might block the demo
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-file-access-from-files")
        
        # Set preferences
        prefs = {
            "profile.default_content_setting_values.media_stream": 1,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome WebDriver initialized")
            return True
        except WebDriverException as e:
            print(f"❌ Failed to initialize Chrome WebDriver: {e}")
            print("\n💡 Make sure Chrome/Chromium is installed:")
            print("   Ubuntu/Debian: sudo apt-get install chromium-browser chromium-chromedriver")
            print("   Fedora: sudo dnf install chromium chromedriver")
            return False
    
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
    
    def test_page_load(self):
        """Test if the page loads successfully."""
        print("\n📄 Testing page load...")
        try:
            self.driver.get(self.url)
            time.sleep(2)
            
            # Check if page title is set
            title = self.driver.title
            self.log_result("Page Load", True, f"Title: {title}")
            return True
        except Exception as e:
            self.log_result("Page Load", False, str(e))
            return False
    
    def test_canvas_exists(self):
        """Test if the game canvas exists."""
        print("\n🎨 Testing canvas element...")
        try:
            canvas = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "canvas"))
            )
            
            # Check canvas dimensions
            width = canvas.get_attribute("width")
            height = canvas.get_attribute("height")
            
            self.log_result("Canvas Element", True, f"Canvas found: {width}x{height}")
            return True
        except TimeoutException:
            self.log_result("Canvas Element", False, "Canvas not found within timeout")
            return False
    
    def test_user_engagement_overlay(self):
        """Test if the user engagement overlay appears."""
        print("\n🎮 Testing user engagement overlay...")
        try:
            overlay = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "user-engagement-overlay"))
            )
            
            # Check if overlay is visible (not hidden)
            is_hidden = "hidden" in overlay.get_attribute("class")
            
            if not is_hidden:
                self.log_result("User Engagement Overlay", True, "Overlay displayed correctly")
                
                # Try to click the start button
                start_btn = self.driver.find_element(By.ID, "start-game-btn")
                start_btn.click()
                time.sleep(2)
                
                # Check if overlay is now hidden
                is_hidden_after = "hidden" in overlay.get_attribute("class")
                if is_hidden_after:
                    self.log_result("Start Button Click", True, "Overlay dismissed after click")
                else:
                    self.log_result("Start Button Click", False, "Overlay still visible")
                
                return True
            else:
                self.log_result("User Engagement Overlay", False, "Overlay hidden by default")
                return False
                
        except TimeoutException:
            self.log_result("User Engagement Overlay", False, "Overlay not found")
            return False
    
    def test_game_loading(self):
        """Test if the game loads (checks for loading indicators)."""
        print("\n⏳ Testing game loading...")
        try:
            # Wait for the download status to appear
            status_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "status"))
            )
            
            status_text = status_elem.text
            self.log_result("Loading Status", True, f"Status: {status_text}")
            
            # Wait a bit for the game to load
            time.sleep(5)
            
            # Check if progress bar exists
            try:
                progress = self.driver.find_element(By.ID, "progress")
                progress_value = progress.get_attribute("value")
                self.log_result("Progress Bar", True, f"Progress: {progress_value}%")
            except:
                self.log_result("Progress Bar", False, "Progress bar not found")
            
            return True
        except TimeoutException:
            self.log_result("Loading Status", False, "Loading status not found")
            return False
    
    def test_console_errors(self):
        """Check browser console for JavaScript errors."""
        print("\n🐛 Checking console for errors...")
        try:
            logs = self.driver.get_log('browser')
            
            errors = [log for log in logs if log['level'] == 'SEVERE']
            warnings = [log for log in logs if log['level'] == 'WARNING']
            
            if errors:
                error_messages = "\n   ".join([log['message'] for log in errors[:3]])
                self.log_result("Console Errors", False, f"Found {len(errors)} errors:\n   {error_messages}")
            else:
                self.log_result("Console Errors", True, "No severe errors found")
            
            if warnings:
                print(f"   ⚠️  Found {len(warnings)} warnings")
            
            return len(errors) == 0
        except Exception as e:
            self.log_result("Console Errors", False, f"Could not check console: {e}")
            return False
    
    def test_apk_file_exists(self):
        """Test if the APK file is accessible."""
        print("\n📦 Testing APK file accessibility...")
        try:
            # Try to access the APK file via JavaScript
            apk_check = self.driver.execute_script("""
                return fetch('web_demo.apk', {method: 'HEAD'})
                    .then(response => response.ok)
                    .catch(() => false);
            """)
            
            time.sleep(1)
            
            self.log_result("APK File", True, "APK file is accessible")
            return True
        except Exception as e:
            self.log_result("APK File", False, str(e))
            return False
    
    def take_screenshot(self, filename="test_screenshot.png"):
        """Take a screenshot of the current page."""
        try:
            screenshot_path = Path(__file__).parent / filename
            self.driver.save_screenshot(str(screenshot_path))
            print(f"📸 Screenshot saved: {screenshot_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests."""
        print("\n" + "=" * 70)
        print("🧪 BOMBERMAN WEB DEMO - AUTOMATED TESTING")
        print("=" * 70)
        print(f"URL: {self.url}")
        print(f"Headless: {self.headless}")
        
        if not self.setup_driver():
            return False
        
        try:
            # Run tests
            self.test_page_load()
            self.test_canvas_exists()
            self.test_user_engagement_overlay()
            self.test_game_loading()
            self.test_apk_file_exists()
            self.test_console_errors()
            
            # Take screenshot
            self.take_screenshot("web_demo_test.png")
            
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
                
        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔒 Browser closed")


def start_http_server(port=8000, directory=None):
    """Start a simple HTTP server for testing."""
    if directory:
        os.chdir(directory)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"🌐 HTTP Server running at http://localhost:{port}")
        print(f"📁 Serving directory: {os.getcwd()}")
        httpd.serve_forever()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Bomberman Web Demo")
    parser.add_argument("--url", default="http://localhost:8000/docs/play/index.html",
                       help="URL to test")
    parser.add_argument("--headless", action="store_true",
                       help="Run browser in headless mode")
    parser.add_argument("--serve", action="store_true",
                       help="Start HTTP server before testing")
    parser.add_argument("--port", type=int, default=8000,
                       help="HTTP server port (default: 8000)")
    
    args = parser.parse_args()
    
    # Start HTTP server if requested
    if args.serve:
        project_dir = Path(__file__).parent
        print(f"\n🚀 Starting HTTP server from {project_dir}")
        
        server_thread = threading.Thread(
            target=start_http_server,
            args=(args.port, str(project_dir)),
            daemon=True
        )
        server_thread.start()
        time.sleep(2)  # Give server time to start
    
    # Run tests
    tester = WebDemoTester(url=args.url, headless=args.headless)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
