# Gizli Sayfalar — Güncelleme Rehberi

## Canva'dan yeni dergi yüklemek

1. Canva → Paylaş → İndir → PDF.
2. Dosya adını örneğin `gizli-sayfalar-sayi-01.pdf` yap.
3. GitHub'da `dergi/sayi-01/` klasörüne gir.
4. PDF'yi **Add file → Upload files** ile yükle.
5. Commit changes yap.
6. Sayı sayfasındaki PDF bağlantısını ekle/güncelle.

## Yeni şiir/öykü eklemek

`icerik/siir/`, `icerik/oyku/`, `icerik/deneme/` veya `icerik/elestiri/` klasörüne `.md` dosyası eklenir.

Örnek:

---
baslik: Eser Başlığı
yazar: Yazar Adı
kategori: Şiir
tarih: 2026-09-01
ozet: Kısa tanıtım.
---

Eserin tam metni.

GitHub Actions aktifse HTML içerik otomatik oluşturulur.

## Ana sayfa görseli

`assets/hero.jpg` dosyasıdır. Yeni görsel kullanmak istersen aynı isimle değiştir.

## Önemli

Repository public olmalı. GitHub Pages:
Settings → Pages → Deploy from a branch → main → / (root).
