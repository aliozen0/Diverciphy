import unittest
import requests
import time

class TestPublicKeyExchange(unittest.TestCase):
    SENDER_URL = "http://127.0.0.1:5000/send_public_key"
    RECEIVER_URL = "http://127.0.0.1:5001/recieve_public_key"

    def test_01_get_public_key(self):
        """Test if the Sender returns the key via GET"""
        response = requests.get(self.SENDER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("public_key", response.json())
        print("\n[GET Test] Successfully retrieved key from Sender.")

    def test_02_full_exchange_flow(self):
        """Test if Sender successfully forwards the key to the Receiver via POST"""
        payload = {"address": self.RECEIVER_URL}
        
        # We tell the Sender to send the key to the Receiver's address
        response = requests.post(self.SENDER_URL, json=payload)
        
        # Check Sender's response
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["remote_response"]["durum"], "basarili")
        print(f"[POST Test] Key forwarded to {self.RECEIVER_URL} successfully.")

if __name__ == "__main__":
    print("Ensure both Flask apps are running before starting the test!")
    unittest.main()