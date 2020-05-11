from basket.utils import Basket


def basket_counter(request):
    basket = Basket(request.session)
    context = {
        'basket_counter': basket.count(),
    }
    return context
