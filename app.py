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
            'square': SquareModuleDrawer(),
            'gapped': GappedSquareModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'vertical': VerticalBarsDrawer(),
            'horizontal': HorizontalBarsDrawer()
        }
        selected_drawer = drawers.get(shape, SquareModuleDrawer())

        # Colors
        front_rgb = hex_to_rgb(color)
        back_rgb = hex_to_rgb(bg_color)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border_size,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage, 
            module_drawer=selected_drawer, 
            color_mask=SolidFillColorMask(front_color=front_rgb, back_color=back_rgb)
        )
        
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
    # Home / Single Generator
    return render_template('index.html')

@app.route('/batch')
def batch():
    # Batch Generator
    return render_template('page1.html')

@app.route('/instructions')
def instructions():
    # Instructions
    return render_template('page2.html')

@app.route('/about')
def about():
    # About
    return render_template('page3.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    text = data.get('text', '')
    if not text: return jsonify({'success': False})
    
    qr_image = generate_qr_base64(
        text=text, 
        size=data.get('size', 10), 
        color=data.get('color', '#000000'), 
        bg_color=data.get('bg_color', '#ffffff'), 
        border=data.get('border', 4), 
        shape=data.get('shape', 'square')
    )
    return jsonify({'success': True, 'image': qr_image})

if __name__ == '__main__':
    app.run(debug=True)