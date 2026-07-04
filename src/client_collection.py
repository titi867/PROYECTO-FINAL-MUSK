class ClientCollection:
    def __init__(self, clients):
        self.clients = clients
    
    def get_client_by_id(self, client_id):
        for c in self.clients:
            if c.client_id == client_id:
                return c
        return None
    
    def client_by_country(self, country):
        return [c for c in self.clients if c.country == country]
    