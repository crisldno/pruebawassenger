from django.db import models


class USUARIOS(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    id_rol = models.BigIntegerField()
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    id_tipo_documento = models.BigIntegerField()
    documento = models.CharField(max_length=255)
    fecha_expide_doc = models.DateTimeField(default='2000-12-28 00:00:00')
    celular = models.CharField()
    email = models.CharField(max_length=255)
    email_confirmed = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True)
    email_confirmation_code = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255)
    pic = models.CharField(max_length=255, null=True)
    remember_token = models.CharField(max_length=100, null=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'USUARIOS'

class USUARIOS_MOVIL(models.Model):
    id_usuario_movil = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(USUARIOS, on_delete=models.CASCADE)
    celular = models.CharField(max_length=20)
    estado = models.BooleanField(default=False)
    id_device = models.TextField()
    estado_solicitud = models.IntegerField()
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'USUARIOS_MOVIL'

class BANCO_PREGUNTAS(models.Model):
    id = models.BigAutoField(primary_key=True)
    pregunta_nombre = models.CharField(max_length=255)
    pregunta_enunciado = models.CharField(max_length=255)
    pregunta_tipo = models.CharField(max_length=255)
    pregunta_guardado = models.CharField(max_length=255, default='2')
    pregunta_api = models.CharField(max_length=255, blank=True, null=True)
    pregunta_html = models.CharField(max_length=255)
    pregunta_estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BANCO_PREGUNTAS'

class BANCO_RESPUESTAS(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_pregunta = models.ForeignKey(BANCO_PREGUNTAS, on_delete=models.CASCADE)
    id_respuesta_panel = models.BigIntegerField()
    respuesta_enunciado = models.TextField()
    respuesta_estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BANCO_RESPUESTAS'

class CONSULTA_USER(models.Model):
    id = models.BigAutoField(primary_key=True)
    documento = models.BigIntegerField()
    id_tipo_documento = models.ForeignKey('TIPO_DOCUMENTO', on_delete=models.CASCADE)
    plataforma = models.CharField(max_length=255)
    request = models.TextField()
    response = models.TextField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'CONSULTA_USER'


class FORMULARIO_CATEGORIA(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_tipo_producto = models.BigIntegerField()
    categoria_nombre = models.CharField(max_length=255)
    categoria_descripcion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'FORMULARIO_CATEGORIA'

class FORMULARIO_INTENTO(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_solicitud = models.BigIntegerField()
    status = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    navegador = models.CharField(max_length=255)
    adicional = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'FORMULARIO_INTENTO'

class FORMULARIO_INTENTO_RESPONDE(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_intento = models.BigIntegerField()
    id_formulario_local = models.BigIntegerField()
    id_respuesta = models.BigIntegerField(null=True)
    respuesta_text = models.TextField(null=True)
    respuesta_api = models.TextField(null=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'FORMULARIO_INTENTO_RESPONDE'


class FORMULARIO_LOCAL(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_categoria = models.BigIntegerField()
    id_pregunta = models.BigIntegerField()
    orden = models.BigIntegerField()
    col_md = models.CharField(max_length=255)
    class_add = models.CharField(max_length=255)
    note_add = models.CharField(max_length=255)
    note_type = models.CharField(max_length=255)
    obligatorio = models.BooleanField(default=False)
    validaciones = models.CharField(max_length=255, default='ninguno')
    value_default = models.CharField(max_length=255, default='ninguno')
    no_editable = models.BooleanField(default=False)
    nombre_api_radica = models.CharField(max_length=255, default='NO_APLICA_API')
    api_valor_id_pregunta = models.BigIntegerField(null=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'FORMULARIO_LOCAL'

class PRODUCTO_CATEGORIA(models.Model):
    id = models.BigAutoField(primary_key=True)
    categoria_nombre = models.TextField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PRODUCTO_CATEGORIA'

class PRODUCTO_POLITICAS(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_producto = models.BigIntegerField()
    politica_titulo = models.TextField()
    politica_especifica = models.TextField()
    politica_pdf = models.TextField()
    politica_recomendacion = models.TextField()
    politica_requiere = models.TextField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PRODUCTO_POLITICAS'

class PRODUCTOS(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto_nombre = models.CharField(max_length=255)
    producto_descripcion = models.TextField()
    producto_imagen = models.CharField(max_length=255)
    id_categoria = models.BigIntegerField(default=1)
    orden_web = models.BigIntegerField(default=1)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    webservice_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'PRODUCTOS'

class ROLES(models.Model):
    id = models.BigAutoField(primary_key=True)
    rol_nombre = models.CharField(max_length=255)
    rol_sigla = models.CharField(max_length=255)
    rol_descripcion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ROLES'

class SOLICITUD(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey(USUARIOS, on_delete=models.CASCADE)
    id_tipo_producto_panel = models.BigIntegerField()
    id_formato_cert = models.BigIntegerField()
    id_vigencia_cert = models.BigIntegerField()
    id_radicado_panel = models.BigIntegerField(null=True)
    cantidad = models.IntegerField()
    id_estado_tramite = models.ForeignKey('TIPO_ESTADO_TRAMITE', on_delete=models.CASCADE)    
    pago = models.BooleanField()
    bolsa = models.BooleanField()
    confirma_identidad = models.BooleanField()
    cupon = models.CharField(max_length=255)
    direccion_token = models.CharField(max_length=255, null=True)
    departamento_token = models.CharField(max_length=255, null=True)
    municipio_token = models.CharField(max_length=255, null=True)
    fecha_inicio_vigencia = models.DateTimeField(null=True)
    estado = models.BooleanField(default=True)
    politica_terminos = models.BooleanField(default=False)
    politica_tratamientos = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_radica = models.TextField(null=True)
    renovacion = models.BooleanField(default=False)
    id_old_panel_solicitud = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'SOLICITUD'

class SOLICITUD_ADJUNTOS(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    id_documento = models.IntegerField()
    Adjunto = models.TextField()
    detalles = models.TextField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'SOLICITUD_ADJUNTOS'

class SOLICITUD_BOLSA(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_solicitud_compra = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE, related_name='solicitud_compra')
    correo_colaborador = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    mensaje_colaborador = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    id_solicitud_uso = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE, related_name='solicitud_uso')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'SOLICITUD_BOLSA'
    
class SOLICITUD_FORMULARIO(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    id_pregunta = models.BigIntegerField()
    id_respuesta = models.BigIntegerField()
    texto_respuesta = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'SOLICITUD_FORMULARIO'

class SOLICITUD_LOG(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey(USUARIOS, on_delete=models.CASCADE)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    metodo = models.TextField()
    request = models.TextField()
    old_values = models.TextField()
    new_values = models.TextField()
    ip_client = models.TextField()
    navegador = models.TextField()
    session = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id_rol = models.IntegerField(null=True)
    nombres = models.CharField(max_length=50, null=True)
    apellidos = models.CharField(max_length=50, null=True)
    id_tipo_documento = models.ForeignKey('TIPO_DOCUMENTO', on_delete=models.CASCADE)
    documento = models.IntegerField(null=True)
    fecha_expide_doc = models.CharField(max_length=50, null=True)
    celular = models.IntegerField(null=True)
    email = models.CharField(max_length=50, null=True)
    email_confirmed = models.BooleanField(default=False)
    email_verified_at = models.CharField(max_length=50, null=True)
    email_confirmation_code = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=64, null=True)
    pic = models.CharField(max_length=50, null=True)
    remember_token = models.CharField(max_length=64, null=True)
    estado = models.BooleanField(null=True)

    class Meta:
        db_table = 'SOLICITUD_LOG'

class SOLICITUD_PAGO(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    ref_pago_epayco = models.CharField(max_length=255)
    id_pago = models.CharField(max_length=255)
    n_pago = models.CharField(max_length=255)
    estado_pago = models.CharField(max_length=255)
    valor_pagado = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    respuesta = models.TextField()
    intentos = models.IntegerField()
    estado = models.BooleanField(default=True)
    fecha_proxima_validacion = models.DateTimeField(default='2023-07-21 11:05:15')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    INSERT_INTO_public_solicitud_pago_id_solicitud = models.CharField(max_length=50)
    updated_at_VALUES = models.CharField(max_length=50)

    class Meta:
        db_table = 'SOLICITUD_PAGO'

class SOLICITUD_VALIDACION(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    tipo_validacion = models.TextField()
    token_validacion = models.TextField()
    intento = models.BigIntegerField()
    status = models.TextField()
    message = models.TextField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'SOLICITUD_VALIDACION'

class TIPO_DOCUMENTO(models.Model):
    id = models.BigAutoField(primary_key=True)
    abreviatura_tipo = models.CharField(max_length=255)
    nombre_tipo = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TIPO_DOCUMENTO'

class TIPO_ESTADO_TRAMITE(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado_nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TIPO_ESTADO_TRAMITE'

