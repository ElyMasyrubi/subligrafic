class Usuario():
    def __init__(self, id, name=None, lastname=None, email=None, password=None, phone=None, adress=None) -> None:
        self.id = id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone
        self.adress = adress
   

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'adress': self.adress
            
        }
