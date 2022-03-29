from marshmallow import Schema,fields
from marshmallow import validate,ValidationError


class CreateRegisterSchema(Schema):

    nombres = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    apellidos = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    correo = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=8, max=12))


class CreateLoginSchema(Schema):

    correo = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=8, max=12))

class CreateCompraSchema(Schema):

    idproducto = fields.Int(required=True, validate=validate.Range(min=1, max=100))