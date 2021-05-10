from odoo import _, api, fields, models, exceptions


class res_partner(models.Model):
_name = "res.partner"
_inherit = "res.partner"
company_type = fields.Selection(selection_add=[('is_school', 'Escuela'),('student', 'Estudiante')])
student = fields.Many2one('academia.student', 'Estudiante')
	
		

class academy_student(models.Model):
	_inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']
	_name = "academy.student"
	_description = "Modelo para formulario de estudiantes"
	name = fields.Char('Nombre', size = 128, track_visibility="onchange")
	last_name = fields.Char('Apellido', size = 128, track_visibility="onchange")
	photo = fields.Binary('Fotografía')
	create_date = fields.Datetime('Fecha de creacion', readonly=True)
	note = fields.Html('Comentarios')
	state = fields.Selection([('draf', 'Documento borrador'), 
							  ('progress', 'Proceso'),
							  ('done', 'Egresado')], 'Estado')
	active = fields.Boolean('Inactivo')
	age = fields.Integer('Edad', track_visibility="onchange")
	curp = fields.Char('Curp', size=18)
	#Relaciones
	partner_id = fields.Many2one('res.partner', 'Escuela')
	country = fields.Many2one('res.country', 'Pais' related='partner_id.country_id')

	invoice_ids = fields.Many2many('account.invoice',
									'student_invoice_rel',
									'student_id', 'invoice_id',
									'Facturas')


	@api.one
	@api.constrains('curp')
	def _check_lines(self):
		if len(self.curp)<18:
			raise.exceptions.ValidationError("Curp debe tener 18 caracteres")

	calificaciones_id = fields.One2many('academy.calificacion',
										'student_id',
										'Calificaciones')

	#Crear usuario en dos modulos

	@api.model
	def create(self,values):
	if values['name']:
	   nombre = values['name']
	   exist_ids = self.env['academy.student'].search([('name','=',self.name)])
	   if exist_ids:
	   	values.update({
	   		'name': values['name']+"(copia)",
	   		})
	   	res=super(academy_student, self).create(values)
	   	partner_obj = self.env['res.partner']
	   	vals_to_partner = {
	   	'name': res['name']+" "+res['last_name'],
	   	'company_type': 'student',
	   	'student_id': res['id'],
	}

	print(vals_to_partner)
	partner_id = partner_obj.create(vals_to_partner)
	print("===>partner_id", 'partner_id')
	return res

	#Eliminar usuario en dos modulos

	@api.multi
	def unlink(self):
		partner_obj = self.env['res.partner']
		partner_ids = partner_obj.search([('student','in',self.ids)])
		print("Partner ##### >>>>>", partner_ids)
		if partner_ids:
			for partner in partner_ids:
				partner.unlink()
			res = super(academy_student, self).unlink()
			return res

	_orden = 'name'
	_defaults = {
				 'state' = 'draf',
				 'active' = True, }






