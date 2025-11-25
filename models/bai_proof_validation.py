from odoo import models, fields
import pdfplumber
import io

class BaiProofValidation(models.Model):
    _name = 'bai.proof.validation'

    name = fields.Char("Name")
    bank = fields.Char("Bank")

    def extract_text_from_pdf(self,file_content):
        text = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def validate_transaction(self, key, pin):
        pass