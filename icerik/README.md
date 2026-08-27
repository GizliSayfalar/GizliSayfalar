# Gizli Sayfalar İçerik Sistemi

Yeni bir eser eklemek için uygun klasörde `.md` dosyası oluştur.

## Örnek

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

Üçüncü paragraf.
```

### Klasörler

- `icerik/siir/`
- `icerik/oyku/`
- `icerik/deneme/`
- `icerik/elestiri/`

GitHub'a dosyayı eklediğinde içerik kaynağı hazır olur.

> Not: GitHub Pages tek başına Markdown'ı otomatik olarak sitenin mevcut özel tasarımına dönüştürmez. Bu proje, sonraki aşamada GitHub Actions ile Markdown dosyalarını otomatik HTML'e çevirip yayınlayacak şekilde genişletilebilir.
