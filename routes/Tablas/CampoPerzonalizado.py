class CampoPerzonalizado():
    
    def __init__(self, id, nombre=None, bolean=None):
        self.id = id
        self.nombre = nombre
        self.boleab = bolean

   
    def to_JSON(self):
            return {
                'id': self.id,
                'nombre': self.nombre,
                'bolean' : self.boleab
            }
