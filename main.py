from flask import Flask, request, send_file, render_template, jsonify
import qrcode
import shortuuid
import os
import argparse
from werkzeug.utils import secure_filename

def create_app(port=8000):
    app = Flask(__name__)
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    class FileShare:
        def __init__(self):
            self.files = {}  # Store file mappings
            
        def generate_unique_id(self):
            return shortuuid.uuid()[:8]  # 8 character unique ID
            
        def save_file(self, file):
            try:
                file_id = self.generate_unique_id()
                filename = secure_filename(file.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                self.files[file_id] = path
                return file_id
            except Exception as e:
                return None

    file_share = FileShare()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/qr/<file_id>')
    def serve_qr(file_id):
        qr_file = os.path.join(UPLOAD_FOLDER, f'{file_id}_qr.png')
        if os.path.exists(qr_file):
            return send_file(qr_file, mimetype='image/png')
        return 'QR code not found', 404

    @app.route('/upload', methods=['POST'])
    def upload():
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            file_id = file_share.save_file(file)
            
            if not file_id:
                return jsonify({'error': 'Failed to save file'}), 500
                
            share_url = request.host_url + 'download/' + file_id
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(share_url)
            qr.make(fit=True)
            
            # Save QR code with proper path
            qr_file = os.path.join(UPLOAD_FOLDER, f'{file_id}_qr.png')
            qr.make_image(fill_color="black", back_color="white").save(qr_file)
            
            return jsonify({
                'file_id': file_id,
                'share_url': share_url,
                'qr_code': f'/qr/{file_id}'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/download/<file_id>')
    def download(file_id):
        if file_id not in file_share.files:
            return 'File not found', 404
        return send_file(file_share.files[file_id])

    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File Sharing Server')
    parser.add_argument('--port', type=int, default=8000, help='Port number')
    args = parser.parse_args()
    
    app = create_app(port=args.port)
    app.run(host='0.0.0.0', port=args.port, debug=True)