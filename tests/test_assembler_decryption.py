import os
import time
from dotenv import load_dotenv

# Mevcut sınıflarını import ediyoruz (dosya isimlerine göre düzenle)
from src.core.shred import Shred      # Shred sınıfının olduğu dosya yolu
from src.core.assemble import Assemble # Assemble sınıfının olduğu dosya yolu

def run_integration_test():
    load_dotenv()
    password = "test_password_123"
    original_payload = "Gizli Mesaj: Parçalanmış ve Şifrelenmiş Veri Testi 2026"
    
    print("--- 1. ADIM: Anahtar Oluşturma (Assemble Side) ---")
    assembler = Assemble(components=[])
    assembler.generate_and_save_keys(password=password)

    print("\n--- 2. ADIM: Şifreleme ve Parçalama (Shred Side) ---")
    mock_assemblers = ["addr1", "addr2", "addr3"]
    shredder = Shred(payload=original_payload, assemblers=mock_assemblers, password=password)
    
    # Public key'i yükle (Senin metodun dosyadan okuyor)
    shredder.recieve_public_key()
    
    # Veriyi önce şifrele sonra parçala
    encrypted_full = shredder.encrypt(original_payload)
    shredded_parts, encrypted_metadata = shredder.shred_encrypted_data(encrypted_full)
    
    print(f"Parça Sayısı: {len(shredded_parts)}")
    print(f"Şifreli Metadata: {encrypted_metadata.hex()[:50]}...")

    print("\n--- 3. ADIM: Veri Birleştirme Simülasyonu (Assemble Side) ---")
    
    # Demo verileri Assemble sınıfının anlayacağı formata sokuyoruz
    # Metadata çözme işlemi
    decrypted_metadata_raw = assembler.decrypt_data(encrypted_metadata, password)
    metadata_str = decrypted_metadata_raw.decode() # "POSITION-2,0,1" gibi döner
    
    # "POSITION-2,0,1" -> [2, 0, 1] listesine çevir
    order = [int(i) for i in metadata_str.replace("POSITION-", "").split(",")]
    
    # Parçaları bir sözlükte simüle et (Sanki networkten gelmiş gibi)
    # { "dist_index": [bytes, timestamp] }
    mock_received_parts = {}
    current_ts = int(time.time())
    for i, part in enumerate(shredded_parts):
        mock_received_parts[str(i)] = [part, current_ts]

    print(f"Metadata Sıralaması: {order}")

    # Manuel Assemble İşlemi (Fonksiyondaki mantığı simüle ediyoruz)
    assembled_bytes = bytearray()
    timestamps = []
    
    # Metadata sırasına göre parçaları doğru dizilimde birleştir
    for position_index in range(len(order)):
        # Metadata içindeki her bir değer aslında hangi parçanın (shredded_parts[i]) 
        # orijinal verinin hangi sırasında olduğunu söyler.
        # Bizim Shred logic'imizde: random.shuffle(parts_with_index) yapılıyor.
        
        # 'order' listesinin içindeki değer, o indexteki parçanın orjinal konumudur.
        # Örn: order = [1, 0] ise, 0. parça aslında 1. sıradadır.
        
        # Doğru birleştirme için: Metadata'daki sıralamayı takip et
        actual_part_index = -1
        for list_idx, original_pos in enumerate(order):
            if original_pos == position_index:
                actual_part_index = list_idx
                break
        
        part_data, ts = mock_received_parts[str(actual_part_index)]
        assembled_bytes.extend(part_data)
        timestamps.append(ts)

    print(f"Birleştirilen Veri Uzunluğu: {len(assembled_bytes)} bytes")

    print("\n--- 4. ADIM: Deşifreleme (Final) ---")
    final_result = assembler.decrypt_data(bytes(assembled_bytes), password)
    
    if final_result:
        print(f"BAŞARILI! Çözülen Veri: {final_result.decode()}")
        assert final_result.decode() == original_payload
    else:
        print("BAŞARISIZ! Veri çözülemedi.")

if __name__ == "__main__":
    run_integration_test()