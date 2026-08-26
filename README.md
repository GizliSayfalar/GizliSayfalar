# Gizli Sayfalar — Edebiyat Dergisi

GitHub Pages üzerinde çalışacak statik e-dergi sitesi.

## Özellikler
- Responsive: telefon / tablet / bilgisayar
- Koyu, samimi, editorial tasarım
- E-Dergi bölümü
- HTML tabanlı web dergi okuma altyapısı
- Şiir ve öykü sayfaları
- Yazarlar ve ekip sayfaları
- Eser gönderim alanı için hazır sayfa
- Discord / Substack / Reddit bağlantıları
- Instagram bağlantısı sonradan eklenebilir

## GitHub Pages'e yayınlama

1. GitHub'da yeni bir repository oluştur.
2. Bu klasördeki dosyaların tamamını repository'ye yükle.
3. Repository → **Settings → Pages**
4. **Build and deployment → Deploy from a branch**
5. Branch: `main`, folder: `/ (root)`
6. Save.
7. GitHub birkaç dakika içinde siteni yayınlar.

## Sonradan içerik eklemek

- Ana sayfa: `index.html`
- Stil: `css/style.css`
- JavaScript: `js/main.js`
- E-Dergi: `dergi/sayi-01/`
- Sayfa içerikleri: `pages/`

Yeni sayı için örneğin:
`dergi/sayi-02/index.html`

PDF dosyaları da `dergi/sayi-01/` içine eklenebilir.

## Not
Site başlığında kullanıcının gönderdiği dairesel sanat görseli amblem olarak kullanılıyor. Amblem `assets/logo-emblem.png` dosyasında.

## Yeni yazı ekleme — kolay yöntem

Artık içerikleri doğrudan Markdown dosyalarıyla yönetebilirsin.

1. `icerik/siir`, `icerik/oyku`, `icerik/deneme` veya `icerik/elestiri` klasörüne gir.
2. Yeni bir `.md` dosyası oluştur.
3. Üstteki bilgi alanını doldur.
4. Altına eserin metnini yaz.
5. GitHub'a `Commit changes` ile yükle.
6. GitHub Actions otomatik olarak HTML sayfasını oluşturur.

Örnek dosya:

```markdown
---
baslik: Günümüzün Deliliği: Bireyselleşme
yazar: Kuzey
kategori: Deneme
tarih: 2026-08-27
ozet: Modern bireyselleşme üzerine bir deneme.
---

İlk paragraf.

İkinci paragraf.
```

İçerik oluşturma işlemi `scripts/build_content.py` tarafından otomatik yapılır.

## Ana sayfa görseli
Ana sayfadaki büyük görsel `assets/hero.jpg` dosyasıdır. Yeni bir görsel kullanmak istersen aynı isimle bu dosyanın üzerine yükle.
