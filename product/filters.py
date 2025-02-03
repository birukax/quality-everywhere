import django_filters
from .models import Artwork, Product
from main.custom_widgets import ProductWidget


class ArtworkFilter(django_filters.FilterSet):
    class Meta:
        model = Artwork
        fields = (
            "code",
            "product",
            "approved",
        )

    product = django_filters.CharFilter(
        field_name="product",
        lookup_expr="exact",
        label="Product",
        widget=ProductWidget(),
    )


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = (
            "no",
            "name",
        )

    product = django_filters.CharFilter(
        field_name="product",
        lookup_expr="exact",
        label="Product",
        widget=ProductWidget(),
    )
