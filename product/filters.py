import django_filters
from .models import Artwork, Product
from main.custom_widgets import ProductWidget, ArtworkWidget


class ArtworkFilter(django_filters.FilterSet):

    class Meta:
        model = Artwork
        fields = (
            "code",
            "product",
            "approved",
        )

    code = django_filters.CharFilter(
        field_name="code",
        lookup_expr="icontains",
        label="Artwork Code",
        widget=ArtworkWidget(),
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
