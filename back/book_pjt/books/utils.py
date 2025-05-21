import requests

API_URL = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'
API_KEY = 'ttbtmddnjs36641349002'

def fetch_bestsellers_from_aladin(total_count=100):
    all_items = []
    per_page = 50
    pages = (total_count + per_page - 1) // per_page

    for page in range(pages):
        start = page * per_page + 1
        params = {
            'TTBKey': API_KEY,
            'QueryType': 'Bestseller',
            'MaxResults': per_page,
            'Start': start,
            'SearchTarget': 'Book',
            'Output': 'JS',
            'Version': 20131101,
        }

        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            items = response.json().get('item', [])
            all_items.extend(items)
        else:
            print(f"[ERROR] Page {page + 1} failed: {response.status_code}")

    return all_items
