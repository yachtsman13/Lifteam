"""
Утилиты для LiftTeam v2.2.
"""
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64


def generate_barcode_image(text):
    """Генерация штрихкода Code 128 из текста адреса ячейки."""
    try:
        code128 = barcode.get_barcode_class('code128')
        barcode_obj = code128(text, writer=ImageWriter())
        buffer = BytesIO()
        barcode_obj.write(buffer, options={
            'write_text': True,
            'module_width': 0.3,
            'module_height': 15,
            'font_size': 10,
            'text_distance': 3,
        })
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    except Exception:
        return None
