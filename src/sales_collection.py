class SalesCollection:
    def __init__(self, sales):
        self.sales = sales
    
    def sales_by_client(self, client_id):
        return [s for s in self.sales if s.client_id == client_id]  
    
    def total_amount_by_client(self, client_id):
        return sum(s.amount for s in self.sales if s.client_id == client_id)
    
    def total_amount_by_category(self, category):
        return sum(s.amount for s in self.sales if s.category == category)
    
    def average_sale_by_client(self, client_id):
        client_sales = self.sales_by_client(client_id)
        if not client_sales:
            return 0
        return sum(s.amount for s in client_sales) / len(client_sales)
    