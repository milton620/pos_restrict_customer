# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomerRestrict(models.Model):
    _inherit = 'res.partner'

    allowed_pos = fields.Many2many('pos.config', string='Allowed Pos',
                                   help='Allowed Pos for this user')


class PosConfig(models.Model):
    _inherit = 'pos.config'

    restrict_customer_only = fields.Boolean(default=False)


class ResConfigSettingsPos(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_restrict_customer_only = fields.Boolean(string='Only Restricted Customer',
                                                related='pos_config_id.restrict_customer_only', readonly=False)


class PosSessionResInherit(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        if self.config_id.restrict_customer_only == True:
            result['search_params']['domain'].extend([('allowed_pos', 'in', [(self.config_id.id)])]), ['fields'].extend(
            ['allowed_pos'])
            result['search_params']['fields'].extend(['allowed_pos'])
        return result

    def get_pos_ui_res_partner_by_params(self, custom_search_params):
        if self.config_id.restrict_customer_only == True:
            custom_search_params['domain'] = [('allowed_pos', 'in', [(self.config_id.id)])]
        partners = super().get_pos_ui_res_partner_by_params(custom_search_params)
        return partners
