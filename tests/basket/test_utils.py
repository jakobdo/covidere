from basket.utils import Basket


class TestBasket:
    class_name = Basket

    def test_basket_count(self):
        basket = self.class_name(session=dict())
        assert basket.count() == 0
    
    def test_basket_add(self):
        basket = self.class_name(session=dict())
        # Create empty basket
        assert basket.count() == 0
        # Add product=1, count=1
        basket.add(1, 1)
        assert basket.count() == 1
        # Add an extra product=1, count=1
        basket.add(1, 1)
        assert basket.count() == 2
        # Add 2 new products, product=2, count=2
        basket.add(2, 2)
        assert basket.count() == 4
