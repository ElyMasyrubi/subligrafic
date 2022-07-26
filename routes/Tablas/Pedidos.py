class Pedidos():
    
    def __init__(self, id, id_usuario=None, fecha=None, productos=None, precioTotal=None, detallesdepago=None, estado=None):
        self.id = id
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.productos = productos
        self.precioTotal = precioTotal
        self.detallesDePago = detallesdepago
        self.estado = estado

    def to_JSON(self):
            return {
                'id': self.id,
                'id_usuario': self.id_usuario,
                'fecha': self.fecha,
                'productos': self.productos,
                'precioTotal': self.precioTotal,
                'detallesDePago': self.detallesDePago,
                'estado': self.estado,
                
            }

