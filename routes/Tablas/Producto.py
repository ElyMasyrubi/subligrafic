class Producto():
    
    def __init__(self, id, code=None, tile=None, description=None, price=None, porcentajedeoferta=None, mainimage=None,tipodeproducto=None,tematica=None,esdestacado=None,tipodetrabajo=None,campopersonalizado=None):
        self.id = id
        self.code = code
        self.tile = tile
        self.description = description
        self.price = price
        self.porcentajedeoferta = porcentajedeoferta
        self.mainimage = mainimage
        self.tipodeproducto = tipodeproducto
        self.tematica = tematica
        self.esdestacado = esdestacado
        self.tipodetrabajo = tipodetrabajo
        self.campopersonalizado = campopersonalizado

    def to_JSON(self):
            return {
                'id': self.id,
                'code': self.code,
                'tile': self.tile,
                'description': self.description,
                'price': self.price,
                'porcentajedeoferta': self.porcentajedeoferta,
                'mainimage': self.mainimage,
                'tipodeproducto': self.tipodeproducto,
                'tematica': self.tematica,
                'esdestacado': self.esdestacado,
                'tipodetrabajo': self.tipodetrabajo,
                'campopersonalizado': self.campopersonalizado
                
            }

