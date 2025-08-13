import math
def disCalt(pixel,gambar,jarakTerdekat):
    pixelAwal = gambar.shape[1]
    jarakAwal = 0.5

    d = (pixelAwal*jarakAwal)/pixel
    h = (pixelAwal*jarakAwal)/jarakTerdekat
    h = h-(h*0.1)

    hasil = math.sqrt(abs(d**2-h**2))
    return hasil