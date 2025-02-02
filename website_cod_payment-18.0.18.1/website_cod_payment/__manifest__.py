# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.cfis.store/>
#################################################################################

{
    "name": "Website Cash on Delivery COD | COD | Website COD | Cash on Delivery",
    "summary": """
        This Odoo app enables the Cash On Delivery (COD) payment method option in website transactions. If you operate an Odoo website, ecommerce platform, 
        or online store and wish to offer your customers the option to pay via cash on delivery, this module is a suitable choice. With this app, customers 
        or visitors to your webshop can purchase products using the cash on delivery payment method. This payment method is integrated as a separate payment 
        provider in the Odoo backend. Additionally, you can customize delivery charges associated with the COD payment method to meet your business requirements.
        """,
    "version": "18.1",
    "description": """
        This Odoo app enables the Cash On Delivery (COD) payment method option in website transactions. If you operate an Odoo website, ecommerce platform, 
        or online store and wish to offer your customers the option to pay via cash on delivery, this module is a suitable choice. With this app, customers 
        or visitors to your webshop can purchase products using the cash on delivery payment method. This payment method is integrated as a separate payment 
        provider in the Odoo backend. Additionally, you can customize delivery charges associated with the COD payment method to meet your business requirements.
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/website_cod_payment.png"],
    "category": "Website",
    "depends": [
        "sale",
        "sale_management", 
        "account", 
        "website",
        "website_sale",
        "payment",
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/report_cod_collection_template.xml",     
        "report/report_cod_collection.xml",     
        "views/payment_cod_templates.xml",
        "views/payment_provider_views.xml",
        "views/templates.xml",
        "views/sale_order_views.xml",
        "views/cod_payment_collection_views.xml",
        "views/product_template_views.xml",
        "data/cod_delivery_fee_data.xml", 
        "data/payment_method_data.xml",
        "data/payment_provider_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            'website_cod_payment/static/src/js/post_processing.js',
        ],
    },    
    "installable": True,
    "application": True,
    "price"                 :  18.00,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}