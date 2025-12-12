from flask import Flask, render_template, request, jsonify
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
import io
import base64

app = Flask(__name__)

# --- Helper: Hex to RGB ---
def hex_to_rgb(hex_color):
    """Converts #RRGGBB to (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# --- Helper: Generate Base64 ---
def generate_qr_base64(text, size, color, bg_color, border, shape):
    """Generates a Base64 string for a QR code with shapes and colors."""
    try:
        box_size = int(size)
        border_size = int(border)
        
        # Map shape names to Drawer objects
        drawers = {
            'square': SquareModuleDrawer(),
            'gapped': GappedSquareModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'vertical': VerticalBarsDrawer(),
            'horizontal': HorizontalBarsDrawer()
        }
        selected_drawer = drawers.get(shape, SquareModuleDrawer())

        # Convert colors for StyledPilImage
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

        # Use StyledPilImage to support Shapes (Drawers)
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=selected_drawer,
            color_mask=SolidFillColorMask(front_color=front_rgb, back_color=back_rgb)
        )

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error: {e}")
        return None

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    text = data.get('text', '')
    size = data.get('size', 10)
    color = data.get('color', '#000000')
    bg_color = data.get('bg_color', '#ffffff')
    border = data.get('border', 4)
    shape = data.get('shape', 'square') # Default to square

    if not text:
        return jsonify({'success': False})

    qr_image = generate_qr_base64(text, size, color, bg_color, border, shape)
    return jsonify({'success': True, 'image': qr_image})

@app.route('/batch', methods=['GET', 'POST'])
def batch():
    qr_codes = []
    error = None
    
    # Defaults
    form_data = {
        'batch_text': '', 'size': 10, 'color': '#000000', 
        'bg_color': '#ffffff', 'border': 4, 'shape': 'square'
    }

    if request.method == 'POST':
        form_data['batch_text'] = request.form.get('batch_text')
        form_data['size'] = request.form.get('size', 10)
        form_data['color'] = request.form.get('color', '#000000')
        form_data['bg_color'] = request.form.get('bg_color', '#ffffff')
        form_data['border'] = request.form.get('border', 4)
        form_data['shape'] = request.form.get('shape', 'square')

        raw_text = form_data['batch_text']
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

        if len(lines) > 10:
            error = "Limit exceeded: Maximum 10 QR codes allowed at once."
            lines = lines[:10]
        
        for line in lines:
            img = generate_qr_base64(
                line, 
                form_data['size'], 
                form_data['color'], 
                form_data['bg_color'],
                form_data['border'],
                form_data['shape']
            )
            if img:
                qr_codes.append({'text': line, 'image': img})

    return render_template('batch.html', qr_codes=qr_codes, error=error, form=form_data)

@app.route('/instructions')
def page1():
    return render_template('page1.html')

@app.route('/about')
def page2():
    return render_template('page2.html')

if __name__ == '__main__':
    app.run(debug=True)