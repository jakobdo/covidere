from django.views.generic import DetailView, ListView

from shop.models import Shop


class ShopsListView(ListView):
    """
    Shop List View. Will list all active shops for enduser
    """
    model = Shop
    template_name = 'shop/list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(active=True)
        return queryset


class ShopsDetailView(DetailView):
    """
    Shop Detail View. Will show detail for an active shop
    """
    model = Shop
    template_name = 'shop/detail.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(active=True)
        return queryset
