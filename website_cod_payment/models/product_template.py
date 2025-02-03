from odoo import api, models, fields, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cod_delivery_fee = fields.Float('Delivery Fees', compute='_compute_cod_delivery_fee')

    def _compute_cod_delivery_fee(self):
        provider_id = self.env['ir.model.data']._xmlid_to_res_id('website_cod_payment.payment_provider_cod')
        provider = self.env['payment.provider'].search([('id', '=', int(provider_id))])
        for product in self:
            product.cod_delivery_fee = provider.cod_delivery_fee if provider.cod_delivery_fee > 0.0 else 0.0