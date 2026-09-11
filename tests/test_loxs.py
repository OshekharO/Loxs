import unittest
import os
import tempfile
import sys
import threading

# Import functions from loxs
import loxs

class TestLoxs(unittest.TestCase):

    def test_generate_html_report_zero_scanned(self):
        """Ensure generate_html_report does not divide by zero when total_scanned is 0."""
        html = loxs.generate_html_report(
            scan_type="Test Scan",
            total_found=0,
            total_scanned=0,
            time_taken=0,
            vulnerable_urls=[]
        )
        self.assertIn("Test Scan", html)
        self.assertIn("0.00%", html)
        self.assertIn("Vulnerability Rate", html)

    def test_generate_html_report_normal(self):
        """Ensure generate_html_report correctly formats vulnerability rate for non-zero counts."""
        html = loxs.generate_html_report(
            scan_type="SQL Injection (SQLi)",
            total_found=5,
            total_scanned=20,
            time_taken=10,
            vulnerable_urls=["http://example.com?id=1'"]
        )
        self.assertIn("25.00%", html)
        self.assertIn("http://example.com?id=1'", html)

    def test_save_html_report(self):
        """Ensure save_html_report writes file properly to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_report.html")
            content = "<html><body>Test</body></html>"
            res = loxs.save_html_report(content, filepath)
            self.assertIsNotNone(res)
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r') as f:
                saved_content = f.read()
            self.assertEqual(saved_content, content)

    def test_thread_safety_scan_state(self):
        """Test concurrent updates to scan_state dictionary using threading Lock."""
        scan_state = {
            'vulnerability_found': False,
            'vulnerable_urls': [],
            'total_found': 0,
            'total_scanned': 0
        }
        lock = threading.Lock()

        def worker(i):
            with lock:
                scan_state['vulnerability_found'] = True
                scan_state['vulnerable_urls'].append(f"http://example.com/{i}")
                scan_state['total_found'] += 1
                scan_state['total_scanned'] += 1

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(scan_state['total_found'], 100)
        self.assertEqual(scan_state['total_scanned'], 100)
        self.assertEqual(len(scan_state['vulnerable_urls']), 100)
        self.assertTrue(scan_state['vulnerability_found'])

if __name__ == '__main__':
    unittest.main()
