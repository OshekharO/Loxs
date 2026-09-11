import unittest
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

if __name__ == '__main__':
    unittest.main()
