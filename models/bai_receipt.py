from odoo import models, fields
import pdfplumber
import io
import re
from datetime import datetime

class BaiReceipt(models.Model):
    _name = "bai.receipt"
    _description = "BAI Direct Receipt"

    key = fields.Char("Key")
    pin = fields.Char("PIN")
    name = fields.Char("Name")
    account = fields.Char("Account")
    iban = fields.Char("IBAN")
    movement_desc = fields.Char("Movement Description")
    data_movement = fields.Datetime("Movement Date")
    amount = fields.Float("Amount")
    operation_number = fields.Char("Operation Number")
    movement_type = fields.Char("Movement Type")
    processed_on = fields.Datetime("Processed On")
    validade_dias = fields.Integer("Validity (days)", default=90)
    raw_text = fields.Text("Extracted Raw Text")   # optional for auditing


    def _extract_text_from_pdf(self,file_content):
        text = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text


    def extract(self, pattern, text):
        match = re.search(pattern, text, re.MULTILINE)
        return match.group(1).strip() if match else False

    def extract_amount(self, value):
        if not value:
            return 0.0
        value = value.replace(".", "").replace(",", ".")
        return float(value)

    def parse_date(self, date_text):
        if not date_text:
            return False
        # format DD/MM/YYYY HH:MM:SS
        return datetime.strptime(date_text, "%d/%m/%Y %H:%M:%S")