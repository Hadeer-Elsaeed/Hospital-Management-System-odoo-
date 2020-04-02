from odoo import models,fields,api
from odoo.exceptions import ValidationError

class My_custome(models.Model):
    _inherit =  'res.partner'
    related_patient_id = fields.Many2many('hms.patient')

    @api.constrains("email")
    def check_email(self):
        email=self.env['hms.patient'].search([('email','=',self.email)])
        if email:
            raise ValidationError("this email is already exist")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You can't delete a customer related to patient")
        super().unlink()

