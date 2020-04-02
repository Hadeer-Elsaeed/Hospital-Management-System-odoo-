import re
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError


class Patient(models.Model):
    _name = "hms.patient"
    _rec_name = "first_name"

    first_name = fields.Char(required="true")
    last_name = fields.Char(required="true")
    birth_date = fields.Date()
    age = fields.Integer()
    image = fields.Binary()
    address = fields.Text()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([("A","A"),("B","B"),("O","O"),("AB","AB")],default = "A")
    pcr = fields.Boolean()
    department_id = fields.Many2one(comodel_name="hms.department")
    department_capacity=fields.Integer(related='department_id.capacity')
    states = fields.Selection([("Undetermined","Undetermined"),("Good","Good"),("Fair","Fair"),("Serious","Serious")],default="Undetermined")
    logs_ids = fields.One2many(comodel_name="hms.log",inverse_name="patient_id")
    doctors_ids = fields.Many2many(comodel_name="hms.doctor")
    email = fields.Char()
    crm = fields.Many2many('res.partner')

    def change_states(self):
        if self.states=="undetermined":
            self.states="good"
        elif self.states=="good":
            self.states="fair"
        elif self.states=="fair":
            self.states="serious"
        elif self.states=="serious":
            self.states="undetermined"
        self.logs_ids.create({
           "patient_id": self.id,
           "description": self.first_name + "'s states has changed to " + self.states,
        })

    @api.onchange('Age')
    def onchange_age(self):
        if self.Age<30:
            prc_domain=[('checked','=',True)]
        else:
            prc_domain=[]
        return {
                'domain':{'history':prc_domain},
                'warning':{
                    'title':'age change',
                    'message':'PCR has been checked!'
                }
            }

    def compute_age(self):
        today = date.today()
        for record in self:
            print(record.birth_date.year)
            record.Age=today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))

    @api.constrains("email")
    def check_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        for record in self:
            if not re.search(regex, record.email):
                raise ValidationError("Opps not atrue email pleaze enter some thing like this = ahmed_hazem@yahoo.com")


class Log(models.Model):
    _name = "hms.log"

    description = fields.Text()
    patient_id = fields.Many2one(comodel_name="hms.patient")

