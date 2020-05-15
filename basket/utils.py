class Basket:
    """
    Small basket helper to add item to basket
    """
    def __init__(self, session):
        self.session = session

    def add(self, product, count):
        # Add or update item
        basket = self.session.setdefault('basket', [])
        item = next((item for item in basket if (
            item['product'] == product
        )), None)
        if item:
            item['count'] += count
        else:
            basket.append(dict(
                product=product,
                count=count
            ))
        return basket

    def count(self):
        basket = self.session.setdefault('basket', [])
        count = 0
        for item in basket:
            count += item['count']
        return count
