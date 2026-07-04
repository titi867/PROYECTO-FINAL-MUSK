import json
import pandas as pd
from client import Client
from sale import Sale
from client_collection import ClientCollection
from sales_collection import SalesCollection
from functional_utils import filter_sales_by_category

def load_clients(path):
    with open(path, 'r') as f:
        clients_data = json.load(f)
    return [Client(**c) for c in data]

def load_sales(path):
    df = pd.read_csv(path)
    return [Sale(
        sale_id=row['sale_id'],
        client_id=row['client_id'],
        product=row['product'],
        category=row['category'],
        amount=row['amount'],
        date=row['date']
    ) for index, row in df.iterrows()]

def main():
    clients = load_clients('data/clients.json')
    sales = load_sales('data/sales.csv')

    client_col = ClientCollection(clients)
    sales_col = SalesCollection(sales)

    df = pd.readcsv('data/sales.csv')

    total_clients = len(clients)
    total_sales = len(sales)

    clients_info = []
    for c in clients:
        total_spent = sales_col.total_amount_by_client(c.client_id)
        sale_count = len(sales_col.sales_by_client(c.client_id))
        average_sale = sales_col.average_sale_by_client(c.client_id)

        clients_info.append({
            "client_id": c.client_id,
            "name": c.name,
            "country": c.country,
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale
        })

        top_by_country = {}
        countries = set(c.country for c in clients)

        for country in countries:
            country_clients = client_col.client_by_country(country)
            if not country_clients:
                continue
           
            best = max(
               country_clients,
               key=lambda c: sales_col.total_amount_by_client(c.client_id)
           )
        
        top_by_country[country] = best.name

    sales_by_category = (
        df.groupby('category')['amount'].sum().to_dict()
    )

    top_client_category = {}
    for category in df['category'].unique():
        filtered = filter_sales_by_category(sales, category)
        counts = {}

        for s in filtered:
            counts[s.client_id] = counts.get(s.client_id, 0) + 1

        top_client = max(counts, key=counts.get)
        top_client_category[category] = client_col.get_client_by_id(top_client).name

        high_spending_clients = [
            c.client_id for c in clients 
            if sales_col.total_amount_by_client(c.client_id) > 500
        ]

        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)

        monthly_sales = df.groupby('month')['amount'].sum().to_dict()

        report = {
            'summary': {
                'total_clients': total_clients,
                'total_sales': total_sales,
                'total_revenue': df['amount'].sum(),
            },
            'clients': clients_info,
            'top_client_by_country': top_by_country,
            'sales_by_category': sales_by_category,
            'top_client_by_category': top_client_category,
            'high_spending_clients': high_spending_clients,
            'monthly_sales': monthly_sales
        }

    with open('report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    return report

if __name__ == "__main__":
    main()
            

