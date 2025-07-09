import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import dns.resolver

# Import your functions
import subdomain_enumerator

class TestSubdomainEnumerator(unittest.TestCase):
    def test_load_wordlist(self):
        # Create a temporary wordlist file
        wordlist_path = Path("test_wordlist.txt")
        wordlist_content = "www\nmail\n#comment\n\nftp\n"
        wordlist_path.write_text(wordlist_content)
        subs = subdomain_enumerator.load_wordlist(wordlist_path)
        self.assertEqual(subs, ["www", "mail", "ftp"])
        wordlist_path.unlink()

    @patch("dns.resolver.Resolver.resolve")
    def test_resolve_domain_success(self, mock_resolve):
        mock_rdata = MagicMock()
        mock_rdata.address = "1.2.3.4"
        mock_resolve.return_value = [mock_rdata]
        resolver = MagicMock()
        resolver.resolve = mock_resolve
        result = subdomain_enumerator.resolve_domain("www", "example.com", resolver)
        self.assertEqual(result, ("www.example.com", ["1.2.3.4"]))

    @patch("dns.resolver.Resolver.resolve", side_effect=dns.resolver.NXDOMAIN)
    def test_resolve_domain_failure(self, mock_resolve):
        resolver = MagicMock()
        resolver.resolve = mock_resolve
        result = subdomain_enumerator.resolve_domain("nope", "example.com", resolver)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
