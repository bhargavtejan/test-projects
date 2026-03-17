# Word to PDF Converter

Convert `.docx` and `.doc` files to PDF using LibreOffice.

## Requirements

- Python 3.8+
- LibreOffice (`libreoffice` or `soffice` in PATH)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Web App

Start the Flask server:

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

- Drag and drop or click to upload a `.docx` / `.doc` file
- Click **Convert to PDF** — the PDF downloads automatically

---

## CLI Tool

Convert a single file:

```bash
python cli.py document.docx
```

Convert to a specific output directory:

```bash
python cli.py document.docx -o ./output
```

Convert multiple files at once:

```bash
python cli.py file1.docx file2.doc -o ./pdfs
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT`   | `5000`  | Port for the web server |
