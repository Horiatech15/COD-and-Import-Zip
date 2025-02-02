from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CODPaymentCollection(models.Model):
    _name = 'cod.payment.collection'
    _rec_name = 'sale_order_id'
    _order = "id desc"
    
    sale_order_id = fields.Many2one('sale.order','Sale Order', required=True)
    company_id = fields.Many2one(related="sale_order_id.company_id",string="Company")
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency')
    transaction_ids = fields.Many2many(related="sale_order_id.transaction_ids", string='Transactions')
    partner_id = fields.Many2one(related="sale_order_id.partner_id",string="Customer")
    order_amount = fields.Monetary(related="sale_order_id.amount_total", string="Order Amount", currency_field="currency_id")
    collection_amount = fields.Monetary("Collection Amount", required=True)
    delivery_person_id = fields.Many2one('res.partner','Delivery Company/Person')
    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirmed'),
        ('cancel', 'Cancelled'),
        ('done','Done')
        ], default='draft', string='State')
    notes = fields.Text('Notes')

    def cancel_collection(self):
        for transaction in self.transaction_ids:
            transaction.sudo()._set_canceled()
        for collection in self:
            collection.sale_order_id.action_cancel()
        self.update({'state': 'cancel', 'notes': 'Order Cancelled'})

    def confirm_collection(self):
        self.update({'state': 'confirm'})
    
    def draft_collection(self):
        self.update({'state': 'draft'})

    def done_collection(self):
        if self.collection_amount < self.order_amount:
            raise ValidationError(_("The collected amount must correspond to the order amount."))
        for transaction in self.transaction_ids:
            transaction.sudo()._set_done()
        self.update({'state': 'done'})