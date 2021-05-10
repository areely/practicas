
from odoo import _, api, fields, models, exceptions

class academy_calificacion(models.Model):
	_name = "academy.calificacion"
	_description = "Calificacion"
	name = fields.Many2one('academy.materia', 'Materia')
	calificacion = fields.Float('Calificacion', digits=(3,2))
	student_id = fields.Many2one('academia.student', 'ID Ref')

	@api.one
	@api.constrains('calificacion')
	def _check_calificacion(self):
		if self.calificacion < 5 or self.calificacion > 10:
			raise.exceptions.ValidationError('La calificacion debe ser mayor a 5 o menor igual a 10')

	class academy_materia(models.Model):
	_name = "academy.materia"
	_description = "Materias"
	name = fields.Char('Nombre')
	_sql_constraints = [('name_uniq', 'unique(name)', 'El nombre de la materia debe ser unico')]


