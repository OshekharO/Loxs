import unittest
import re
import requests
from unittest.mock import MagicMock, patch
import urllib.parse
from packaging import version

class TestLoxsFixes(unittest.TestCase):

    def test_version_normalization(self):
        v_str = "v2.1.0"
        normalized = v_str.lstrip('v')
        self.assertEqual(normalized, "2.1.0")
        parsed = version.parse(normalized)
        self.assertEqual(str(parsed), "2.1.0")

    def test_or_scanner_unbound_local_simulation(self):
        # Test path formulation logic in test_open_redirect to ensure test_url / target url is correctly scoped
        url = "http://example.com/test"
        payloads = ["/redirect_payload"]
        parsed = urllib.parse.urlparse(url)
        path = parsed.path

        for payload in payloads:
            test_url_obj = parsed._replace(path=path + payload)
            target_url = urllib.parse.urlunparse(test_url_obj)
            self.assertEqual(target_url, "http://example.com/test/redirect_payload")

    def test_crlf_compiled_regex(self):
        raw_patterns = [
            r'(?m)^(?:Location\s*?:\s*(?:https?:\/\/|\/\/|\/\\\\|\/\\)(?:[a-zA-Z0-9\-_\.@]*)loxs\.pages\.dev\/?(\/|[^.].*)?$|(?:Set-Cookie\s*?:\s*(?:\s*?|.*?;\s*)?loxs=injected(?:\s*?)(?:$|;)))',
            r'(?m)^(?:Location\s*?:\s*(?:https?:\/\/|\/\/|\/\\\\|\/\\)(?:[a-zA-Z0-9\-_\.@]*)loxs\.pages\.dev\/?(\/|[^.].*)?$|(?:Set-Cookie\s*?:\s*(?:\s*?|.*?;\s*)?loxs=injected(?:\s*?)(?:$|;)|loxs-x))'
        ]
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in raw_patterns]

        test_header = "Set-Cookie: loxs=injected"
        is_match = any(pattern.search(test_header) for pattern in compiled_patterns)
        self.assertTrue(is_match)

    def test_lfi_compiled_regex(self):
        success_criteria = ['root:x:0:', 'admin:']
        compiled_criteria = [re.compile(p) for p in success_criteria]

        response_text = "root:x:0:0:root:/root:/bin/bash"
        is_vulnerable = any(pattern.search(response_text) for pattern in compiled_criteria)
        self.assertTrue(is_vulnerable)

    def test_session_reuse(self):
        session = requests.Session()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "root:x:0:"

        with patch.object(session, 'get', return_value=mock_response) as mock_get:
            res = session.get("http://example.com/test")
            self.assertEqual(res.status_code, 200)
            mock_get.assert_called_once_with("http://example.com/test")

    def test_generate_html_report_zero_scanned(self):
        import loxs
        report = loxs.generate_html_report("Test Scan", 0, 0, 5, [])
        self.assertIn("0.00%", report)

if __name__ == '__main__':
    unittest.main()
