from fpdf import FPDF
import re
import json

class PDFCreator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        self.pdf.set_y(20)

    def add_title(self, text):
        self.pdf.set_font("Arial", 'B', 18)
        self.pdf.cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
        self.pdf.ln(10)
        self.pdf.set_font("Arial", size=12)

    def add_text(self, text):
        if text.startswith("- ") or text.startswith("• "):
            self.pdf.set_x(20)
            self.pdf.multi_cell(0, 6, f"• {text[2:]}")
        elif "```" in text:
            self.add_code(text)
        else:
            self.pdf.multi_cell(0, 6, text)
        self.pdf.ln(3)

    def add_code(self, text):
        match = re.search(r"```(?:\w+)?\n?([\s\S]*?)```", text)
        if match:
            code = match.group(1).strip()
            self.pdf.set_font("Courier", size=10)
            self.pdf.set_fill_color(245, 245, 245)
            self.pdf.multi_cell(0, 6, code, border=1, fill=True)
            self.pdf.set_font("Arial", size=12)
            self.pdf.ln(5)

    def generate(self, data, filename="output.pdf"):
        if isinstance(data, str):
            data = json.loads(data) if data.startswith("{") else {"response": data}

        if data.get("title"):
            self.add_title(data["title"])

        content = data.get("response") or data.get("content") or ""
        for line in content.split("\n"):
            if line.strip():
                self.add_text(line)

        self.pdf.output(filename)
        return filename

def tool_pdf_creator(input_json: str) -> dict:
    creator = PDFCreator()
    pdf_file = creator.generate(input_json)
    return {
        "pdf_url": f"https://storage.playai.network/{pdf_file}",
        "filename": pdf_file,
        "message": "PDF généré ! Téléchargez ici.",
        "download": True
    }
