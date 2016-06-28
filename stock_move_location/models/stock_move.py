# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'
    _order = 'product_location,product_code'

    product_location = fields.Char(
        compute="_get_product_info",
        string="Location",
        store=True
    )
    product_code = fields.Char(
        compute="_get_product_info",
        string="Code",
        store=True
    )

    @api.one
    @api.depends('product_id', 'picking_id')
    def _get_product_info(self):
        picking = self.picking_id
        if picking.picking_type_id.warehouse_id:
            self.product_location = self.product_id.with_context(warehouse=picking.picking_type_id.warehouse_id.id).product_location
        else:
            self.product_location = self.product_id.product_location
        self.product_code = self.product_id.default_code