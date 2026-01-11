from odoo import models, fields

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    bai_receipt_id = fields.Many2one('bai.receipt')
    bai_receipt_state = fields.Selection([
        ('draft', 'Draft'),('bai_valid', 'Valid'),('not_valid', 'Not Valid'),('other_bank', 'Other')
    ], default='draft')