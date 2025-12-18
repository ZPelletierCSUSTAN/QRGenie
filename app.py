from flask import Flask, render_template, request, jsonify
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer,
    RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
import io
import base64

app = Flask(__name__)

# --- Helper Functions ---
def hex_to_rgb(hex_color):
    if not hex_color: return (0, 0, 0)
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_base64(text, size, color, bg_color, border, shape):
    try:
        box_size = int(size)
        border_size = int(border)
        drawers = {
            'square': SquareModuleDrawer(), 'gapped': GappedSquareModuleDrawer(),
            'circle': CircleModuleDrawer(), 'rounded': RoundedModuleDrawer(),
            'vertical': VerticalBarsDrawer(), 'horizontal': HorizontalBarsDrawer()
        }
        selected_drawer = drawers.get(shape, SquareModuleDrawer())
        front_rgb = hex_to_rgb(color)
        back_rgb = hex_to_rgb(bg_color)

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=box_size, border=border_size)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(image_factory=StyledPilImage, module_drawer=selected_drawer, color_mask=SolidFillColorMask(front_color=front_rgb, back_color=back_rgb))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
    except Exception as e:
        print(f"Error: {e}")
        return None

# --- Routes ---

@app.route('/')
def index():
    # Renders the main dashboard
    return render_template('index.html')

@app.route('/batch', methods=['GET', 'POST'])
def batch():
    # Renders the Batch Generator (Page 1)
    qr_codes = []
    error = None
    form_data = {'batch_text': '', 'size': 10, 'color': '#000000', 'bg_color': '#ffffff', 'border': 4, 'shape': 'square'}

    if request.method == 'POST':
        form_data.update({
            'batch_text': request.form.get('batch_text'),
            'size': request.form.get('size', 10),
            'color': request.form.get('color', '#000000'),
            'bg_color': request.form.get('bg_color', '#ffffff'),
            'border': request.form.get('border', 4),
            'shape': request.form.get('shape', 'square')
        })
        lines = [line.strip() for line in form_data['batch_text'].split('\n') if line.strip()]
        if len(lines) > 10:
            error = "Limit exceeded: Maximum 10 QR codes allowed at once."
            lines = lines[:10]
        
        for line in lines:
            img = generate_qr_base64(line, form_data['size'], form_data['color'], form_data['bg_color'], form_data['border'], form_data['shape'])
            if img: qr_codes.append({'text': line, 'image': img})

    return render_template('page1.html', qr_codes=qr_codes, error=error, form=form_data)

@app.route('/instructions')
def instructions():
    # Renders Instructions (Page 2)
    return render_template('page2.html')

@app.route('/about')
def about():
    # Renders About (Page 3)
    return render_template('page3.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    if not data.get('text'): return jsonify({'success': False})
    qr_image = generate_qr_base64(data.get('text'), data.get('size', 10), data.get('color', '#000'), data.get('bg_color', '#fff'), data.get('border', 4), data.get('shape', 'square'))
    return jsonify({'success': True, 'image': qr_image})

if __name__ == '__main__':
    app.run(debug=True)