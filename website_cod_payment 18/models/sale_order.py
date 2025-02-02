from odoo import api, models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    collection_ids = fields.One2many('cod.payment.collection', 'sale_order_id')
    collection_count = fields.Integer(string="Collection Count", compute='_compute_collection_count')

    @api.depends('collection_ids')
    def _compute_collection_count(self):
        for order in self:
            order.collection_count = len(order.collection_ids)

    def action_view_collections(self):
        action = self.env.ref('website_cod_payment.action_cod_collection').read()[0]
        action['domain'] = [('sale_order_id', '=', self.id)]
        return action