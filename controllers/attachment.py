from odoo.addons.mail.controllers.attachment import AttachmentController
from odoo import fields, api, http
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
from odoo.http import request
import requests
import json
import base64

class AttachmentControllerInherit(AttachmentController):

    @http.route("/mail/attachment/upload", methods=["POST"], type="http", auth="public")
    @add_guest_to_context
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        file_storage = request.httprequest.files.get("ufile")
        file_content = file_storage.read()
        if thread_model == 'sale.order':
            BaiReceipt = request.env['bai.receipt'].sudo()
            full_text = BaiReceipt._extract_text_from_pdf(file_content)

            vals = {
                "key": BaiReceipt.extract(r"CHAVE:\s*(\d+)", full_text),
                "pin": BaiReceipt.extract(r"PIN:\s*(\d+)", full_text),
                "name": BaiReceipt.extract(r"Nome:\s*(.*)", full_text),
                "account": BaiReceipt.extract(r"Conta:\s*(\d+)", full_text),
                "iban": BaiReceipt.extract(r"IBAN:\s*([A-Z0-9]+)", full_text),
                "movement_desc": BaiReceipt.extract(r"Movimento:\s*(.*)", full_text),
                "data_movement": BaiReceipt.parse_date(BaiReceipt.extract(r"Data:\s*(.*)", full_text)),
                "amount": BaiReceipt.extract_amount(BaiReceipt.extract(r"Montante:\s*Kz\s*([\d\.,]+)", full_text)),
                "operation_number": BaiReceipt.extract(r"Número de Operação:\s*(\d+)", full_text),
                "movement_type": BaiReceipt.extract(r"Tipo de Movimento:\s*(.*)", full_text),
              #  "processed_on": BaiReceipt.parse_date(BaiReceipt.extract(r"Documento processado.*:\s*(.*)", full_text)),
                "raw_text": full_text,
            }
            bai_receipt_id = BaiReceipt.create(vals)

            payload = {
                "reference": base64.b64encode(vals["pin"].encode()).decode(),
                "key": base64.b64encode(vals["key"].encode()).decode(),
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # 5. Call external API safely
            try:
                response = requests.post(
                    "https://validador.bancobai.ao/api/validate",
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=10
                )
                result = response.json()
                print(result)
            except Exception as e:
                result = {"error": str(e)}
        return super().mail_attachment_upload(ufile, thread_id, thread_model, is_pending=False, **kwargs)

