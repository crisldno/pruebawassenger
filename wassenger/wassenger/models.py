from django.db import models

class Mensaje(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.phone}: {self.message}'

class USUARIO(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    tipo_doc = models.CharField(max_length=45)
    numero_doc = models.CharField(max_length=45)
    correo= models.EmailField()
    verificacion_correo = models.BooleanField(default=False)
    terminos = models.BooleanField(default=False)
    politicas = models.BooleanField(default=False)
    fecha_exp = models.DateField()
    estado = models.BooleanField(max_length=50)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class USUARIO_MOVIL(models.Model):
    id_usuario_movil = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE)
    celular = models.CharField(max_length=20)
    estado = models.BooleanField(default=False)
    id_device = models.CharField(default=100)
    estado_solicitud=models.IntegerField(default=100)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class USUARIO_SOLICITUD(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario_movil = models.ForeignKey(USUARIO_MOVIL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class STATUS(models.Model):
    id_status = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    estado = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class SOLICITUD(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE)
    id_tipo_producto = models.IntegerField()
    id_vigencia = models.IntegerField()
    id_formato_entrega = models.IntegerField()
    id_radicado_panel = models.IntegerField()
    cupon = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    pago = models.BooleanField(default=False)
    valida_identidad = models.BooleanField(default=False)
    terminos_pc = models.BooleanField(default=False)
    municipio_token = models.CharField(max_length=255)
    ciudad_token = models.CharField(max_length=255)
    direccion_token = models.CharField(max_length=255)
    estado = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class PREGUNTAS_TIPO_CERT(models.Model):
    id_preguntas = models.AutoField(primary_key=True)
    id_tipo_cert = models.IntegerField()
    tipo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)
    enunciado = models.TextField()
    estado = models.BooleanField(default=False)
    pregunta_guardado = models.CharField(max_length=150)
    nombre_api_radica = models.CharField(max_length=255)
    validaciones = models.TextField()
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class RESPUESTAS_TIPO_CERT(models.Model):
    id = models.AutoField(primary_key=True)
    id_pregunta_tipo_cert = models.ForeignKey(PREGUNTAS_TIPO_CERT, on_delete=models.CASCADE)
    resp_enunciado = models.TextField()
    estado = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class RESPUESTAS_USUARIO(models.Model):
    id_respuestas = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    id_pregunta = models.ForeignKey(PREGUNTAS_TIPO_CERT, on_delete=models.CASCADE)
    respuesta_user = models.TextField()
    estado = models.CharField(max_length=50)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class SOLICITUD_DOCUMENTOS(models.Model):
    id = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    id_docu = models.IntegerField()
    nombre_archivo = models.CharField(max_length=255)
    estado = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class SOLICITUD_PAGOS(models.Model):
    id = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(SOLICITUD, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    refpago = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)

class SOLICITUD_VALIDACION_IDE(models.Model):
    id_solicitud = models.OneToOneField(SOLICITUD, on_delete=models.CASCADE, primary_key=True)
    link = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    estado = models.BooleanField(default=False)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actualiza = models.DateTimeField(auto_now=True)