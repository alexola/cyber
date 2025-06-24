import unittest 
from unittest.mock import patch
from port_scanner import scan_ports

class TestPortScanner(unittest.TestCase):
    @patch("socket.socket")
    def test_scan_ports_normal_mode(self, mock_socket):
        # Mock socket to always return closed ports except for port 80
        instance = mock_socket.return_value
        def connect_ex_side_effect(addr): #Simulate connect_ex behavior
            return 0 if addr[1] == 80 else 1
        instance.connect_ex.side_effect = connect_ex_side_effect

        open_ports = scan_ports("127.0.0.1", start_port=79, end_port=81, mode="normal") #Scan ports 79 to 81 in normal mode
        self.assertIsInstance(open_ports, list)
        self.assertIn(80, open_ports) #Port 80 should be open
        self.assertNotIn(79, open_ports) #Port 79 should not be open
        self.assertNotIn(81, open_ports) #Port 81 should not be open

    def test_invalid_host(self):
        # Should handle invalid host gracefully and return an empty list
        result = scan_ports("notarealhost", start_port=79, end_port=81, mode="normal")
        self.assertEqual(result, [])  # Should return an empty list

if __name__ == "__main__":
    unittest.main()