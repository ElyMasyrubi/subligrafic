class TipoDeProducto():
    
    def __init__(self, id, nombre=None, tipos_del_producto=None):
        self.id = id
        self.nombre = nombre
        self.tipos_del_producto = tipos_del_producto
   
    def to_JSON(self):
            return {
                'id': self.id,
                'nombre': self.nombre,
                'tipos_del_producto': self.tipos_del_producto

            }
