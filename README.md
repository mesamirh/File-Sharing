# File-Sharing

A simple file sharing web application built with Flask that allows users to:

- Upload files through drag-and-drop or file selection
- Generate unique shareable links
- Create QR codes for easy mobile access

## Features

- Clean, modern UI
- Drag-and-drop file upload
- Automatic QR code generation
- Secure file handling
- Unique short URLs for each file

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/mesamirh/File-Sharing.git
   cd File-Sharing
   ```
2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the server:

```bash
python main.py
```

Access the web interface at `http://localhost:8000`

## Dependencies

- Flask
- qrcode
- shortuuid
- Werkzeug

## Security Notes

- Files are stored locally in an 'uploads' directory
- Basic file validation is implemented
- No built-in file expiration
