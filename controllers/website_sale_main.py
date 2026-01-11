from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route

import requests
import json
import base64

def bai_base64(value: str) -> str:
    first = base64.b64encode(value.encode("utf-8")).decode("utf-8")
    second = base64.b64encode(first.encode("utf-8")).decode("utf-8")
    return second

class WebsiteSaleMain(WebsiteSale):

    @route("/shop/confirmation/upload_attachment", type="http", auth="public", methods=["POST"], csrf=True)
    def upload_attachment(self, order_id=None, attachment=None, **kwargs):
        file_storage = request.httprequest.files.get("attachment")
        bank = request.httprequest.form.get("bank_selected")
        file_content = file_storage.read()
        BaiReceipt = request.env['bai.receipt'].sudo()
        sale_order_id = request.env['sale.order'].sudo().browse(int(order_id))
        if bank == 'bai':
            full_text = BaiReceipt._extract_text_from_pdf(file_content)
            vals = {
                "key": BaiReceipt.extract(r"CHAVE:\s*(\d+)", full_text),
                "pin": BaiReceipt.extract(r"PIN:\s*(\d+)", full_text),
                "name": BaiReceipt.extract(r"Nome:\s*(.*)", full_text),
                "account": BaiReceipt.extract(r"Conta:\s*(\d+)", full_text),
                "iban": BaiReceipt.extract(r"IBAN:\s*([A-Z0-9]+)", full_text),
                "movement_desc": BaiReceipt.extract(r"Movimento:\s*(.*)", full_text),
                "data_movement": BaiReceipt.parse_date(BaiReceipt.extract(r"Data:\s*(.*)", full_text)),
                'amount': f'KZ {BaiReceipt.extract(r"Montante:\s*Kz\s*([-–\d\s\.,]+)", full_text)}',
                "operation_number": BaiReceipt.extract(r"Número de Operação:\s*(\d+)", full_text),
                "movement_type": BaiReceipt.extract(r"Tipo de Movimento:\s*(.*)", full_text),
                #  "processed_on": BaiReceipt.parse_date(BaiReceipt.extract(r"Documento processado.*:\s*(.*)", full_text)),
                "raw_text": full_text,
            }

            if vals['pin'] and vals['key']:
                bai_receipt_id = BaiReceipt.create(vals)
                payload = {
                    "VR0001": bai_base64(vals["pin"]),
                    "VK0001": bai_base64(vals["key"]),
                }

                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }

                try:
                    response = requests.post(
                        "https://validador.bancobai.ao/api/validate",
                        data=json.dumps(payload),
                        headers=headers,
                        timeout=10
                    )
                    result = response.json()
                    pdf_url = result.get("document")
                    if pdf_url:
                        pdf_response = requests.get(pdf_url)
                        pdf_content = pdf_response.content
                        attachment_vals = {
                            'name': file_storage.filename,
                            'type': 'binary',
                            'datas': base64.b64encode(pdf_content),
                            'res_model': 'sale.order',
                            'res_id': int(order_id),
                            'mimetype': 'application/pdf',
                        }
                        sale_order_id.write({'bai_receipt_id': bai_receipt_id.id})
                        sale_order_id.write({'bai_receipt_state': 'bai_valid'})
                        request.env['ir.attachment'].sudo().create(attachment_vals)

                except Exception as e:
                    pass
            else:
                sale_order_id.write({'bai_receipt_state': 'not_valid'})
        else:
            sale_order_id.write({'bai_receipt_state': 'other_bank'})
            attachment_vals = {
                'name': file_storage.filename,
                'type': 'binary',
                'datas': base64.b64encode(file_content),
                'res_model': 'sale.order',
                'res_id': int(order_id),
                'mimetype': 'application/pdf',
            }
            request.env['ir.attachment'].sudo().create(attachment_vals)

        return request.redirect(f"/shop/confirmation")
