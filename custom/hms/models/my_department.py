from odoo import models, fields


class Department(models.Model):
    _name = "hms.department"
    _rec_name = "dep_name"

    dep_name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients_ids = fields.One2many(comodel_name="hms.patient",inverse_name="department_id")


class Doctor(models.Model):
    _name = "hms.doctor"
    _rec_name = "first_name"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary("Image")

