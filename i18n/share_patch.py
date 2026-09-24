"""Ajoute les textes du partage (réseaux, cartes) à chaque langue."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent
K = ['share_lead', 'copy_link', 'card_post', 'card_story', 'card_wide', 'card_dl', 'card_share', 'close']
T = {
 'fr': ["Partage ta question", "Copier le lien", "Carte Instagram", "Story", "Carte paysage", "Télécharger", "Partager l'image", "Fermer"],
 'en': ["Share your question", "Copy link", "Instagram card", "Story", "Landscape card", "Download", "Share image", "Close"],
 'es': ["Comparte tu pregunta", "Copiar enlace", "Tarjeta Instagram", "Historia", "Tarjeta horizontal", "Descargar", "Compartir imagen", "Cerrar"],
 'pt': ["Compartilhe sua pergunta", "Copiar link", "Card Instagram", "Story", "Card paisagem", "Baixar", "Compartilhar imagem", "Fechar"],
 'ru': ["Поделись вопросом", "Скопировать ссылку", "Карточка Instagram", "Сторис", "Широкая карточка", "Скачать", "Поделиться картинкой", "Закрыть"],
 'zh': ["分享你的问题", "复制链接", "Instagram 卡片", "快拍", "横版卡片", "下载", "分享图片", "关闭"],
 'ja': ["問いをシェアする", "リンクをコピー", "Instagram カード", "ストーリー", "横長カード", "ダウンロード", "画像をシェア", "閉じる"],
 'hi': ["अपना सवाल शेयर करें", "लिंक कॉपी करें", "Instagram कार्ड", "स्टोरी", "लैंडस्केप कार्ड", "डाउनलोड", "तस्वीर शेयर करें", "बंद करें"],
 'bn': ["আপনার প্রশ্ন শেয়ার করুন", "লিংক কপি করুন", "Instagram কার্ড", "স্টোরি", "ল্যান্ডস্কেপ কার্ড", "ডাউনলোড", "ছবি শেয়ার করুন", "বন্ধ করুন"],
 'ar': ["شارك سؤالك", "نسخ الرابط", "بطاقة Instagram", "قصة", "بطاقة أفقية", "تنزيل", "مشاركة الصورة", "إغلاق"],
}
for c, v in T.items():
    f = root / f'{c}.json'
    d = json.loads(f.read_text(encoding='utf-8')); d.update(dict(zip(K, v)))
    f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8'); print('ok', c)
