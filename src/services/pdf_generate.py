from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
import platform
import os

def create_pdf(video_title: str, transcript_text, output_dir="", calback_func=None):
    """
    PDF oluşturur.
    Args:
        video_title: PDF dosyası ve içindeki başlık için video başlığı
        transcript_text: PDF içinde yazılacak metin
        output_dir: PDF'in kaydedileceği klasör (opsiyonel)
        calback : geri dönüşümlü function
    
    Returns:
        PDF dosya adı (tam yol)
    """
    # Güvenli dosya adı
    new_transcript_text = ""
    calback_func(0.2, "Pdf Creating . . .") # type: ignore
    
    safe_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_.')
    file_name_safe = "".join(c if c in safe_chars else '_' for c in video_title).strip()
    if len(file_name_safe) > 100:
        file_name_safe = file_name_safe[:100]
    
    calback_func(0.4, "Pdf Creating . . .") # type: ignore
    
    pdf_file = os.path.join(output_dir, f"{file_name_safe}.pdf")
    
    # PDF oluşturucu
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    # ✅ Font yolu - Önce proje içinden, sonra sistem fontlarından
    font_name = 'Helvetica'  # Varsayılan
    
    # Font yolu sıralaması
    font_paths = [
        'assets/fonts/arial.ttf',  # ✅ Proje içi (mobil için)
        'assets/fonts/Arial.ttf',  # Büyük A ile de dene
        r'C:\Windows\Fonts\arial.ttf',  # Windows
        '/Library/Fonts/Arial.ttf',  # macOS
    ]
    
    try:
        for font_path in font_paths:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Arial', font_path))
                font_name = 'Arial'
                print(f"✅ Font yüklendi: {font_path}")
                break
    except Exception as e:
        print(f"⚠️ Font yüklenemedi, varsayılan font kullanılıyor: {e}")
    
    calback_func(0.7, "text convertations . . .") # type: ignore
    new_transcript_text = " ".join(entry["text"] for entry in transcript_text)
    
    # Stil ayarları
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    normal_style.fontName = font_name
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    calback_func(0.9, "Pdf Creating . . .") # type: ignore
    
    # PDF içeriği
    story = []
    story.append(Paragraph(new_transcript_text.replace("\n", "<br/>"), normal_style))
    
    # PDF kaydet
    doc.build(story)
    calback_func(1.0, "Pdf Created") # type: ignore