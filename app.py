from flask import Flask, render_template, request, jsonify
import qrcode
import io
import base64

app = Flask(__name__)

# --- Helper Function ---
def generate_qr_base64(text, size, color):
    """Generates a Base64 string for a QR code."""
    try:
        # Scale size logic: 1-20 slider maps to box_size
        box_size = int(size)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=color, back_color="white")

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
    # We no longer handle POST here for the main page, 
    # because we are doing it via the API below.
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """This endpoint handles the Real-Time updates via JavaScript"""
    data = request.json
    text = data.get('text', '')
    size = data.get('size', 10)
    color = data.get('color', '#000000')

    if not text:
        return jsonify({'success': False})

    qr_image = generate_qr_base64(text, size, color)
    return jsonify({'success': True, 'image': qr_image})

@app.route('/batch', methods=['GET', 'POST'])
def batch():
    qr_codes = []
    error = None
    
    if request.method == 'POST':
        raw_text = request.form.get('batch_text')
        size = request.form.get('size', 10)
        color = request.form.get('color', '#000000')

        # Split lines and filter empty ones
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

        if len(lines) > 10:
            error = "Limit exceeded: Please enter maximum 10 lines."
            lines = lines[:10] # Enforce limit on processing anyway
        
        for line in lines:
            img = generate_qr_base64(line, size, color)
            if img:
                qr_codes.append({'text': line, 'image': img})

    return render_template('batch.html', qr_codes=qr_codes, error=error)

@app.route('/instructions')
def page1():
    return render_template('page1.html')

@app.route('/about')
def page2():
    return render_template('page2.html')

if __name__ == '__main__':
    app.run(debug=True)