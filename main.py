import cv2

def kamera_listele():
    index = 0
    kameralar = []
    
    while True:
        kamera = cv2.VideoCapture(index)
        if not kamera.read()[0]:
            break
        else:
            ret, frame = kamera.read()
            if ret:
                kamera_adi = f"Kamera {index}"
                try:
                    kamera_adi = f"Kamera {index} - {int(kamera.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(kamera.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
                except:
                    kamera_adi = f"Kamera {index}"
                kameralar.append((index, kamera_adi))
        kamera.release()
        index += 1
    
    return kameralar

def ascii_kamera_goster(kamera_index):
    kamera = cv2.VideoCapture(kamera_index)
    if not kamera.isOpened():
        print(f"Kamera {kamera_index} açılamadı")
        return
    
    print(f"Kamera {kamera_index} başlatılıyor... (Çıkmak için 'q' tuşuna basın)")
    
    while True:
        ret, cerceve = kamera.read()
        if not ret:
            break
        
        gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
        yukseklik, genislik = gri.shape
        en_orani = genislik / yukseklik
        yeni_genislik = 120
        yeni_yukseklik = int(yeni_genislik / en_orani / 2)
        yeniden_boyutlandirilmis = cv2.resize(gri, (yeni_genislik, yeni_yukseklik))
        
        ascii_karakterler = "@%#*+=-:. "
        ascii_cerceve = ""
        
        for satir in yeniden_boyutlandirilmis:
            for piksel in satir:
                ascii_cerceve += ascii_karakterler[piksel // 32]
            ascii_cerceve += "\n"
        
        print("\033[2J\033[H")
        print(f"=== Kamera {kamera_index} ===")
        print(ascii_cerceve)
        print("Çıkmak için 'q' tuşuna basın")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    kamera.release()
    print("Kamera kapatıldı")

def main():
    kameralar = kamera_listele()
    
    if not kameralar:
        print("Hiç kamera bulunamadı")
        return
    
    print("\n=== MEVCUT KAMERALAR ===")
    for index, ad in kameralar:
        print(f"{index}: {ad}")
    
    try:
        secim = int(input("\nKamera numarası seçin: "))
        secilen_kamera = None
        for index, ad in kameralar:
            if index == secim:
                secilen_kamera = index
                break
        
        if secilen_kamera is not None:
            ascii_kamera_goster(secilen_kamera)
        else:
            print("Geçersiz kamera numarası!")
    except ValueError:
        print("Geçersiz giriş! Lütfen bir sayı girin.")

if __name__ == "__main__":
    main()
