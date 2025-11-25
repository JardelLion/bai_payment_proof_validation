from odoo.addons.mail.controllers.attachment import AttachmentController
from odoo import fields, api, http
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
from odoo.http import request

class AttachmentControllerInherit(AttachmentController):

    @http.route("/mail/attachment/upload", methods=["POST"], type="http", auth="public")
    @add_guest_to_context
    def mail_attachment_upload(self, ufile, thread_id, thread_model, is_pending=False, **kwargs):
        file_storage = request.httprequest.files.get("ufile")
        file_content = file_storage.read()
        if thread_model == 'sale.order':
            v = request.env['bai.proof.validation'].sudo().extract_text_from_pdf(file_content)
            print(v)

        return super().mail_attachment_upload(ufile, thread_id, thread_model, is_pending=False, **kwargs)

