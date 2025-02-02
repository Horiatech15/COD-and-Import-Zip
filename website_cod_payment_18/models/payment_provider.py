from odoo import _, api, fields, models
from odoo.addons.website_sale_collect import const

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cod', "Cash on Delivery")], ondelete={'cod': 'set default'})
    cod_delivery_fee = fields.Float('Add Delivery Fee')

    @api.model_create_multi
    def create(self, values_list):
        providers = super().create(values_list)
        providers.filtered(lambda p: p.code == 'cod').pending_msg = None
        return providers
    
    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'code':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES
    
    def _transfer_ensure_pending_msg_is_set(self):
        transfer_providers_without_msg = self.filtered(
            lambda p: p.code == 'cod' and not p.pending_msg
        )
        if transfer_providers_without_msg:
            transfer_providers_without_msg.action_recompute_pending_msg()

    @api.depends('code')
    def _compute_view_configuration_fields(self):
        """ Override of payment to make the `show_credentials_page` field not required.

        :return: None
        """
        super()._compute_view_configuration_fields()
        self.filtered(lambda p: p.code == 'cod').update({
            'show_credentials_page': False,
        })