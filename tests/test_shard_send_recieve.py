import unittest
import requests
import time

class TestshredExchange(unittest.TestCase):
    # Bu URL'leri makinelerinin gerçek IP/Port adreslerine göre güncelle
    SENDER_URL = "http://127.0.0.1:5002/send_shred"
    RECEIVER_URL = "http://127.0.0.1:5003/recieve_shred"

    def test_01_get_shred_from_sender(self):
        """Test if the node returns the shred via GET"""
        response = requests.get(self.SENDER_URL)
        
        self.assertEqual(response.status_code, 200, "Node shred bilgisini donemedi.")
        data = response.json()
        
        self.assertIn("shred", data, "JSON icinde 'shred' anahtari yok.")
        self.assertIn("timestamp", data, "JSON icinde 'timestamp' anahtari yok.")
        print(f"\n[GET Test] shred alindi. Timestamp: {data['timestamp']}")

    def test_02_post_shred_to_receiver(self):
        """Test if the Receiver node saves the incoming shred"""
        test_payload = {
            "shred": "test_shred_data_001",
            "timestamp": f"test_time_{int(time.time())}"
        }
        
        response = requests.post(self.RECEIVER_URL, json=test_payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        print(f"[POST Test] shred basariyla kaydedildi: {data['message']}")

    def test_03_full_flow_forwarding(self):
        """Test if Sender successfully forwards its latest shred to the Receiver"""
        # Sender'a "elindeki shred'i su adrese (Receiver) gonder" diyoruz
        payload = {"address": self.RECEIVER_URL}
        
        response = requests.post(self.SENDER_URL, json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Sender'in kendi cevabi
        self.assertEqual(data["status"], "success")
        # Alıcıdan (Receiver) donen cevap (remote_response)
        self.assertEqual(data["remote_response"]["status"], "success")
        
        print(f"[Full Flow] shred '{data['address']}' adresine basariyla iletildi.")

    def test_04_invalid_request_handling(self):
        """Test if the Receiver rejects invalid JSON"""
        invalid_payload = {"only_shred": "no_timestamp"}
        response = requests.post(self.RECEIVER_URL, json=invalid_payload)
        
        self.assertEqual(response.status_code, 400)
        print("[Error Handling Test] Eksik veri 400 ile reddedildi.")

if __name__ == "__main__":
    print("--- shred Sistemi Entegrasyon Testleri Baslatiliyor ---")
    print("Note: Please Make Sure You Have Flask Applications Running On The Correct Ports\n")
    unittest.main()