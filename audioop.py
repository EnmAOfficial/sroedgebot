# sroedgebot/audioop.py
# Python 3.13'te kaldırılan audioop modülü için
# dummy (boş) implementasyon.
# Ses özelliklerini kullanmıyoruz, bu yüzden fonksiyonlar
# sadece orijinal veriyi geri döndürüyor veya 0 veriyor.

def mul(fragment, width, factor):
    # Ses seviyesini çarpanla değiştirirdi, biz dokunmuyoruz.
    return fragment

def add(fragment1, fragment2, width):
    # İki audio parçasını toplardı, biz sadece birincisini dönüyoruz.
    return fragment1

def lin2lin(fragment, width, newwidth):
    # Örnek genişliğini dönüştürürdü, biz aynen geri veriyoruz.
    return fragment

def ratecv(fragment, width, nchannels, inrate, outrate, state=None):
    # Sample rate dönüşümü, biz hiçbir şey yapmadan geri dönüyoruz.
    return fragment, state

def getsample(fragment, width, index):
    # Belirli sample'ı döndürürdü, biz 0 veriyoruz.
    return 0

def max(fragment, width):
    # Maksimum genlik, biz 0 diyoruz.
    return 0

def rms(fragment, width):
    # RMS hesaplar, biz 0 diyoruz.
    return 0

def tomono(fragment, width, lfactor, rfactor):
    # Stereo → mono çevirirdi, biz dokunmuyoruz.
    return fragment

def tostereo(fragment, width, lfactor, rfactor):
    # Mono → stereo çevirirdi, biz dokunmuyoruz.
    return fragment
