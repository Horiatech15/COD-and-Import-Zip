import logging
import pprint

from odoo import http, SUPERUSER_ID, _
from odoo.http import Controller, request, route

_logger = logging.getLogger(__name__)

from odoo.addons.website_sale.controllers.main import WebsiteSale

class CODController(Controller):
    _process_url = '/payment/cod/process'

    @route(_process_url, type='http', auth='public', methods=['POST'], csrf=False)
    def cod_process_transaction(self, **post):
        _logger.info("Handling custom processing with data:\n%s", pprint.pformat(post))
        request.env['payment.transaction'].sudo()._handle_notification_data('cod', post)
        return request.redirect('/payment/status')
    

class WebsiteSaleCOD(WebsiteSale):

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def shop_payment_validate(self, sale_order_id=None, **post):
        """ Method that should be called by the server when receiving an update
        for a transaction. State at this point :

         - UDPATE ME
        """

        if sale_order_id is None:
            order = request.website.sale_get_order()
            if not order and 'sale_last_order_id' in request.session:
                # Retrieve the last known order from the session if the session key `sale_order_id`
                # was prematurely cleared. This is done to prevent the user from updating their cart
                # after payment in case they don't return from payment through this route.
                last_order_id = request.session['sale_last_order_id']
                order = request.env['sale.order'].sudo().browse(last_order_id).exists()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        tx_sudo = order.get_portal_last_transaction() if order else order.env['payment.transaction']

        if tx_sudo.provider_id.code == 'cod' and  order:
            product_cod_delivery_fee = request.env['ir.model.data']._xmlid_to_res_model_res_id('website_cod_payment.product_cod_payment_fee')[1]
            product_id = request.env['product.product'].sudo().search([('product_tmpl_id.id', '=', product_cod_delivery_fee)],limit=1)
            
            existing_line = request.env['sale.order.line'].sudo().search([
                ('product_id', '=', product_id.id),
                ('order_id', '=', order.id)
            ])

            if not existing_line:
                request.env['sale.order.line'].sudo().create({
                    'name': 'Extra Fees',
                    'order_id': order.id,
                    'price_unit': tx_sudo.provider_id.cod_delivery_fee,
                    'product_id': product_id.id,
                    'product_uom_qty': 1,
                    'product_uom': request.env.ref('uom.product_uom_unit').id,
                })
                order.order_line._compute_tax_id()
            sale_order_id = request.session.get('sale_last_order_id')
            if sale_order_id:
                order = request.env['sale.order'].sudo().browse(sale_order_id)
                order.with_context(send_email=True).with_user(SUPERUSER_ID).action_confirm()
                request.website.sale_reset()
                values = self._prepare_shop_payment_confirmation_values(order)
                return request.render("website_sale.confirmation", values)
            else:
                return request.redirect('/shop')

        if not order or (order.amount_total and not tx_sudo):
            return request.redirect('/shop')

        if order and not order.amount_total and not tx_sudo:
            order.with_context(send_email=True).with_user(SUPERUSER_ID).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx_sudo and tx_sudo.state == 'draft':
            return request.redirect('/shop')

        return request.redirect('/shop/confirmation')
