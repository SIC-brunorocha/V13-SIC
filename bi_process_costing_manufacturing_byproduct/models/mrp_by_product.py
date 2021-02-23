# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
import math

class MrpBom(models.Model):
    _inherit = "mrp.bom"
    
    

    def _compute_total_cost_by(self):
        total_material = 0.0
        total_labour = 0.0
        total_overhead = 0.0
        
        for material_line in self.bom_by_material_cost_ids:
            total_material += material_line.by_total_cost
        self.by_bom_total_material_cost = total_material
        
        for labour_line in self.bom_by_labour_cost_ids:
            total_labour += labour_line.by_total_cost
        self.by_bom_total_labour_cost = total_labour
        
        for overhead_line in self.bom_by_overhead_cost_ids:
            total_overhead += overhead_line.by_total_cost
        self.by_bom_total_overhead_cost = total_overhead
                
    bom_by_material_cost_ids = fields.One2many("material.cost.byproduct","by_bom_material_id","Material Cost")
    bom_by_labour_cost_ids = fields.One2many("labour.cost.byproduct","by_mrp_bom_labour_id","Labour Cost")
    bom_by_overhead_cost_ids = fields.One2many("overhead.cost.byproduct","by_mrp_bom_overhead_id","Overhead Cost")
    # single page total cost
    by_bom_total_material_cost = fields.Float(compute='_compute_total_cost_by',string="Total Material Cost")
    by_bom_total_labour_cost = fields.Float(compute='_compute_total_cost_by',string="Total Labour Cost")
    by_bom_total_overhead_cost = fields.Float(compute='_compute_total_cost_by',string="Total Overhead Cost")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def onchange_product_id(self):
        list_of_by_material = []
        list_of_by_labour = []
        list_of_by_overhead = []
        
        list_of_material = []
        list_of_labour = []
        list_of_overhead = []
        
        if not self.product_id:
            self.bom_id = False
        else:
            bom = self.env['mrp.bom']._bom_find(product=self.product_id, picking_type=self.picking_type_id, company_id=self.company_id.id)
            if bom.type == 'normal':
                self.bom_id = bom.id
                
                for by_material in bom.bom_by_material_cost_ids:
                    list_of_by_material.append(by_material.id)
                self.pro_by_material_cost_ids = [(6,0,list_of_by_material)]
                
                for by_labour in bom.bom_by_labour_cost_ids:
                    list_of_by_labour.append(by_labour.id)
                self.pro_by_labour_cost_ids = [(6,0,list_of_by_labour)]
                
                for by_overhead in bom.bom_by_overhead_cost_ids:
                    list_of_by_overhead.append(by_overhead.id)
                self.pro_by_overhead_cost_ids = [(6,0,list_of_by_overhead)]
                #
                for material in bom.bom_material_cost_ids:
                    list_of_material.append(material.id)
                self.pro_material_cost_ids = [(6,0,list_of_material)]
                
                for labour in bom.bom_labour_cost_ids:
                    list_of_labour.append(labour.id)
                self.pro_labour_cost_ids = [(6,0,list_of_labour)]
                
                for overhead in bom.bom_overhead_cost_ids:
                    list_of_overhead.append(overhead.id)
                self.pro_overhead_cost_ids = [(6,0,list_of_overhead)]
                                
                
            else:
                self.bom_id = False
                
                for by_material in bom.bom_by_material_cost_ids:
                    list_of_by_material.append(by_material.id)
                self.pro_by_material_cost_ids = [(6,0,list_of_by_material)]
                
                for by_labour in bom.bom_by_labour_cost_ids:
                    list_of_by_labour.append(by_labour.id)
                self.pro_by_labour_cost_ids = [(6,0,list_of_by_labour)]
                
                for by_overhead in bom.bom_by_overhead_cost_ids:
                    list_of_by_overhead.append(by_overhead.id)
                self.pro_by_overhead_cost_ids = [(6,0,list_of_by_overhead)]

                #
                for material in bom.bom_material_cost_ids:
                    list_of_material.append(material.id)
                self.pro_material_cost_ids = [(6,0,list_of_material)]
                
                for labour in bom.bom_labour_cost_ids:
                    list_of_labour.append(labour.id)
                self.pro_labour_cost_ids = [(6,0,list_of_labour)]
                
                for overhead in bom.bom_overhead_cost_ids:
                    list_of_overhead.append(overhead.id)
                self.pro_overhead_cost_ids = [(6,0,list_of_overhead)]                
                
            self.product_uom_id = self.product_id.uom_id.id
            return {'domain': {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}}
            
    def _compute_total_cost_by(self):
        total_material = 0.0
        total_labour = 0.0
        total_overhead = 0.0
        
        actual_total_material = 0.0
        actual_total_labour = 0.0
        actual_total_overhead = 0.0
        
        for material_line in self.pro_by_material_cost_ids:
            total_material += material_line.by_total_cost
            actual_total_material += material_line.by_total_actual_cost
            
        self.by_total_material_cost = total_material 
        self.by_total_actual_material_cost = actual_total_material
        
        for labour_line in self.pro_by_labour_cost_ids:
            total_labour += labour_line.by_total_cost
            actual_total_labour += labour_line.by_total_actual_cost
            
        self.by_total_labour_cost = total_labour
        self.by_total_actual_labour_cost = actual_total_labour
        
        for overhead_line in self.pro_by_overhead_cost_ids:
            total_overhead += overhead_line.by_total_cost
            actual_total_overhead += overhead_line.by_total_actual_cost
            
        self.by_total_overhead_cost = total_overhead
        self.by_total_actual_overhead_cost = actual_total_overhead
        
        total_cost = 0.0
        actual_total_cost = 0.0
        
        total_cost = self.by_total_material_cost + self.by_total_labour_cost + self.by_total_overhead_cost
        actual_total_cost = self.by_total_actual_material_cost + self.by_total_actual_labour_cost + self.by_total_actual_overhead_cost
        
        self.by_total_all_cost = total_cost 
        self.by_total_actual_all_cost = actual_total_cost

    def _compute_total_by_product_cost(self):
        total = 0.0
        for line in self.finished_move_line_ids:
            if line.qty_done != 0.0:
                total =  self.by_total_actual_all_cost / line.qty_done
        self.by_product_unit_cost = total       

    
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id         
        
    pro_by_material_cost_ids = fields.One2many("material.cost.byproduct","by_pro_material_id","Material Cost")
    pro_by_labour_cost_ids = fields.One2many("labour.cost.byproduct","by_pro_labour_id","Labour Cost")
    pro_by_overhead_cost_ids = fields.One2many("overhead.cost.byproduct","by_pro_overhead_id","Overhead Cost")

    # Costing By Product Tab    
    by_total_material_cost = fields.Float(compute='_compute_total_cost_by',string="Total Material Cost By Product",default=0.0)
    by_total_labour_cost = fields.Float(compute='_compute_total_cost_by',string="Total Labour Cost By Product",default=0.0)
    by_total_overhead_cost = fields.Float(compute='_compute_total_cost_by',string="Total Overhead Cost By Product",default=0.0)
    by_total_all_cost = fields.Float(compute='_compute_total_cost_by',string="Total Cost By Product",default=0.0)
    
    by_total_actual_material_cost = fields.Float(compute='_compute_total_cost_by',string="Total Actual Material Cost By Product",default=0.0)
    by_total_actual_labour_cost = fields.Float(compute='_compute_total_cost_by',string="Total Actual Labour Cost By Product",default=0.0)
    by_total_actual_overhead_cost = fields.Float(compute='_compute_total_cost_by',string="Total Actual Overhead Cost By Product",default=0.0)
    by_total_actual_all_cost = fields.Float(compute='_compute_total_cost_by',string="Total Actual Cost",default=0.0)
    
    by_product_unit_cost = fields.Float(compute='_compute_total_by_product_cost',string="Product Unit Cost",default=0.0)
        
class MaterialCost(models.Model):
    _name = "material.cost.byproduct"
    
    by_operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
    by_product_id = fields.Many2one('product.template',string="Product")
    by_planned_qty = fields.Float(string="Planned Qty",default=0.0)
    by_uom_id = fields.Many2one('uom.uom',string="UOM")
    by_cost = fields.Float(string="Cost/Unit")
    by_actual_qty = fields.Float(string="Actual Qty",default=1.0)
    by_total_cost = fields.Float(compute='onchange_by_planned_qty',string="Total Cost")
    by_total_actual_cost = fields.Float(compute='onchange_by_planned_qty',string="Total Actual Cost")
    by_bom_material_id = fields.Many2one("mrp.bom","Mrp Bom Material")
    by_pro_material_id = fields.Many2one("mrp.production","Mrp Production Material")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    
    
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
                
    
    @api.onchange('by_product_id')
    def onchange_by_product_id(self):
        res = {}
        if not self.by_product_id:
            return res
        self.by_uom_id = self.by_product_id.uom_id.id
        
    #@api.multi
    @api.onchange('by_planned_qty', 'by_cost')
    def onchange_by_planned_qty(self):
        for line in self:
            price = line.by_planned_qty * line.by_cost
            actual_price = line.by_actual_qty * line.by_cost
            line.by_total_cost = price
            line.by_total_actual_cost = actual_price

class LabourCost(models.Model):
    _name = "labour.cost.byproduct"
    
    
    @api.onchange('by_product_id')
    def onchange_by_product_id(self):
        res = {}
        if not self.by_product_id:
            return res
        self.by_uom_id = self.by_product_id.uom_id.id
            
    @api.onchange('by_planned_qty', 'by_cost')
    def onchange_by_planned_qty(self):
        for line in self:
            price = line.by_planned_qty * line.by_cost
            actual_price = line.by_actual_qty * line.by_cost
            line.by_total_cost = price
            line.by_total_actual_cost = actual_price
            
    
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    by_operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
    by_product_id = fields.Many2one('product.template',string="Product")
    by_planned_qty = fields.Float(string="Planned Qty",default=0.0)
    by_uom_id = fields.Many2one('uom.uom',string="UOM")
    by_cost = fields.Float(string="Cost/Unit")
    by_actual_qty = fields.Float(string="Actual Qty",default=1.0)
    by_total_cost = fields.Float(compute='onchange_by_planned_qty',string="Total Cost")
    by_total_actual_cost = fields.Float(compute='onchange_by_planned_qty',string="Total Actual Cost")
    by_mrp_bom_labour_id = fields.Many2one("mrp.bom","Mrp Bom Labour")
    by_pro_labour_id = fields.Many2one("mrp.production","Mrp Production Labour")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")
    
class OverheadCost(models.Model):
    _name = "overhead.cost.byproduct"
    
    
    @api.onchange('by_product_id')
    def onchange_by_product_id(self):
        res = {}
        if not self.by_product_id:
            return res
        self.by_uom_id = self.by_product_id.uom_id.id
            
    @api.onchange('by_planned_qty', 'by_cost')
    def onchange_by_planned_qty(self):
        for line in self:
            price = line.by_planned_qty * line.by_cost
            actual_price = line.by_actual_qty * line.by_cost
            line.by_total_cost = price
            line.by_total_actual_cost = actual_price
            
    
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id
            
    by_operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
    by_product_id = fields.Many2one('product.template',string="Product")
    by_planned_qty = fields.Float(string="Planned Qty",default=0.0)
    by_uom_id = fields.Many2one('uom.uom',string="UOM")
    by_cost = fields.Float(string="Cost/Unit")
    by_actual_qty = fields.Float(string="Actual Qty",default=1.0)
    by_total_cost = fields.Float(compute='onchange_by_planned_qty',string="Total Cost")
    by_total_actual_cost = fields.Float(compute='onchange_by_planned_qty',string="Total Actual Cost")
    by_mrp_bom_overhead_id = fields.Many2one("mrp.bom","Mrp Bom Overhead")
    by_pro_overhead_id = fields.Many2one("mrp.production","Mrp Production Overhead")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

class ChangeProductionQty(models.TransientModel):
    _inherit = 'change.production.qty'
    
    
    def change_prod_qty(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for wizard in self:
            production = wizard.mo_id
            produced = sum(production.move_finished_ids.filtered(lambda m: m.product_id == production.product_id).mapped('quantity_done'))
            if wizard.product_qty < produced:
                format_qty = '%.{precision}f'.format(precision=precision)
                raise UserError(_("You have already processed %s. Please input a quantity higher than %s ") % (format_qty % produced, format_qty % produced))
            old_production_qty = production.product_qty
            production.write({'product_qty': wizard.product_qty})
            
            # Change Material,Labour and Overhead quantity
            for material in production.pro_material_cost_ids:
                    material.write({'planned_qty':wizard.product_qty,'actual_qty':wizard.product_qty})
        
            for labour in production.pro_labour_cost_ids:
                    labour.write({'planned_qty':wizard.product_qty,'actual_qty':wizard.product_qty}) 

            for overhead in production.pro_overhead_cost_ids:
                    overhead.write({'planned_qty':wizard.product_qty,'actual_qty':wizard.product_qty}) 
                    
			# Change Material,Labour and Overhead quantity By Product
            for material in production.pro_by_material_cost_ids:
                    material.write({'by_planned_qty':wizard.product_qty,'by_actual_qty':wizard.product_qty})
        
            for labour in production.pro_by_labour_cost_ids:
                    labour.write({'by_planned_qty':wizard.product_qty,'by_actual_qty':wizard.product_qty}) 

            for overhead in production.pro_by_overhead_cost_ids:
                    overhead.write({'by_planned_qty':wizard.product_qty,'by_actual_qty':wizard.product_qty})                     
                    
            done_moves = production.move_finished_ids.filtered(lambda x: x.state == 'done' and x.product_id == production.product_id)
            qty_produced = production.product_id.uom_id._compute_quantity(sum(done_moves.mapped('product_qty')), production.product_uom_id)
            factor = production.product_uom_id._compute_quantity(production.product_qty - qty_produced, production.bom_id.product_uom_id) / production.bom_id.product_qty
            boms, lines = production.bom_id.explode(production.product_id, factor, picking_type=production.bom_id.picking_type_id)
            documents = {}
            for line, line_data in lines:
                move, old_qty, new_qty = production._update_raw_move(line, line_data)
                iterate_key = production._get_document_iterate_key(move)
                if iterate_key:
                    document = self.env['stock.picking']._log_activity_get_documents({move: (new_qty, old_qty)}, iterate_key, 'UP')
                    for key, value in document.items():
                        if documents.get(key):
                            documents[key] += [value]
                        else:
                            documents[key] = [value]
            production._log_manufacture_exception(documents)
            operation_bom_qty = {}
            for bom, bom_data in boms:
                for operation in bom.routing_id.operation_ids:
                    operation_bom_qty[operation.id] = bom_data['qty']
            finished_moves_modification = self._update_product_to_produce(production, production.product_qty - qty_produced, old_production_qty)
            production._log_downside_manufactured_quantity(finished_moves_modification)
            moves = production.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            moves._action_assign()
            for wo in production.workorder_ids:
                operation = wo.operation_id
                if operation_bom_qty.get(operation.id):
                    cycle_number = float_round(operation_bom_qty[operation.id] / operation.workcenter_id.capacity, precision_digits=0, rounding_method='UP')
                    wo.duration_expected = (operation.workcenter_id.time_start +
                                 operation.workcenter_id.time_stop +
                                 cycle_number * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency)
                quantity = wo.qty_production - wo.qty_produced
                if production.product_id.tracking == 'serial':
                    quantity = 1.0 if not float_is_zero(quantity, precision_digits=precision) else 0.0
                else:
                    quantity = quantity if (quantity > 0) else 0
                if float_is_zero(quantity, precision_digits=precision):
                    wo.final_lot_id = False
                    wo.active_move_line_ids.unlink()
                wo.qty_producing = quantity
                if wo.qty_produced < wo.qty_production and wo.state == 'done':
                    wo.state = 'progress'
                if wo.qty_produced == wo.qty_production and wo.state == 'progress':
                    wo.state = 'done'
                # assign moves; last operation receive all unassigned moves
                # TODO: following could be put in a function as it is similar as code in _workorders_create
                # TODO: only needed when creating new moves
                moves_raw = production.move_raw_ids.filtered(lambda move: move.operation_id == operation and move.state not in ('done', 'cancel'))
                if wo == production.workorder_ids[-1]:
                    moves_raw |= production.move_raw_ids.filtered(lambda move: not move.operation_id)
                moves_finished = production.move_finished_ids.filtered(lambda move: move.operation_id == operation) #TODO: code does nothing, unless maybe by_products?
                moves_raw.mapped('move_line_ids').write({'workorder_id': wo.id})
                (moves_finished + moves_raw).write({'workorder_id': wo.id})
                if quantity > 0 and wo.move_raw_ids.filtered(lambda x: x.product_id.tracking != 'none') and not wo.active_move_line_ids:
                    wo._generate_lot_ids()
        return {}
        
            
