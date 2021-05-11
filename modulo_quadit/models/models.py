from odoo import _, api, fields, models, exceptions

class academy_materia_list(models.Model):
	_name = 'academy.materia.list'
	grado_id = fields.Many2one('academy.grado', 'ID Referencia')
	materia_id = fields.Many2one('academy.materia', 'Materia', required=True)

class academy_grado(models.Model):
	_name = 'academy.grado'
	_description = 'Modelo grados con un listado de materias'

	@api.depends('name', 'grupo')
		def calculate_name(self):
			complete_name = self.name + " / " + self.grupo
		self.complete_name = complete_name
	_rec_name  = complete_name

	name = fields.Selection([
		('1','Primero'),
		('2','Segundo'),
		('3','Tercero'),
		('4','Cuarto'),
		('5','Quinto'),
		('6','Sexto')],
		 'Grado', required=True)

	gupo = fields.Selection([
		('a','A'),
		('b','B'),
		('c','C')],'Grupo')

materia_ids = fields.One2many('academy.materia.list', 'grado_id', 'Materias')
complete_name = fields.Char('Nombre Completo', size=128, compute="calculate_name" ,store=True)



class res_partner(models.Model):
_name = "res.partner"
_inherit = "res.partner"
company_type = fields.Selection(selection_add=[('is_school', 'Escuela'),('student', 'Estudiante')])
student = fields.Many2one('academy.student', 'Estudiante')
	
class academy_student(models.Model):	
	_inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']

	@api.depends('calificaciones_id')
	def calcula_promedio(self):
		acum = 0.0
		for xcal in self.calificaciones_id:
			acum+=xcal.calificacion
			if acum:
				promedio = acum/len(self.calificaciones_id)
				self.promedio = promedio


	@api.model
	def _get_school_default(self):
	school_id = self.env['res.partner'].search([('name','=',"Escuela Comodin")])
	return school_id

	_name = "academy.student"
	_description = "Modelo para formulario de estudiantes"
	name = fields.Char('Nombre', size = 128, track_visibility="onchange")
	last_name = fields.Char('Apellido', size = 128, track_visibility="onchange")
	photo = fields.Binary('Fotografia')
	create_date = fields.Datetime('Fecha de creacion', readonly=True)
	note = fields.Html('Comentarios')
	state = fields.Selection([('draf', 'Documento borrador'), 
							  ('progress', 'Proceso'),
							  ('done', 'Egresado')
							  ('cancel', 'Expulsado')], 'Estado', default="draft")
	active = fields.Boolean('Inactivo')
	age = fields.Integer('Edad', track_visibility=True)
	curp = fields.Char('Curp', size=18, copy=False, track_visibility=True)
	#Relaciones
	partner_id = fields.Many2one('res.partner', 'Escuela', default=_get_school_default)
	country = fields.Many2one('res.country', 'Pais' related='partner_id.country_id')

	invoice_ids = fields.Many2many('account.invoice',
									'student_invoice_rel',
									'student_id', 'invoice_id',
									'Facturas')

	grado_id = fields.Many2one('academy.grado', 'Grado')
	promedio = fields.Float('Promedio', digits=(14,2),compute="calcula_promedio")

	@api.onchange('grado_id')
		def onchange_grado(self)
		calificaciones_list = []
			for materia in self.grado_id.materia_ids:
			 xval = (0,0, {
			 	'name': materia.materia_id.id,
			 	'calificacion': 5
			 	})
	calificaciones_list.append(xval)
	self.update({'calificaciones_id': calificaciones_list})




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

	@api.multi 
	def done(self):
		self.state = 'done'
		return True

	@api.multi 
	def confirm(self):
		self.state = 'process'
		return True

	@api.multi 
	def cancel(self):
		self.state = 'cancel'
		return True

	@api.multi 
	def draft(self):
		self.state = 'draft'
		return True






