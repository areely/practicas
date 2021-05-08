from odoo import _, api, fields, models

class academy_student(models.Model):
	_name = "academy.student"
	_description = "Modelo para formulario de estudiantes"
	name = fields.Char('Nombre', size = 128)
	last_name = fields.Char('Apellido', size = 128)
	photo = fields.Binary('Fotografía')
	create_date = fields.Datetime('Fecha de creacion', readonly=True)

