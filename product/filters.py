from .models import *
import django_filters


class ProductFilter(django_filters.FilterSet):
	class Meta:
		model = Product
		fields = {
		'title': ['icontains'],
        }



class PriceFilter(django_filters.FilterSet):
	CHOICES=(
		('ascending','Lower to Higher'),
		('descending','Higher to Lower'))

	ordering=django_filters.ChoiceFilter(label='Price Ordering', choices=CHOICES, method='filter_by_ordering')

	def filter_by_ordering(self, queryset, name, value):
		expression='price' if value =='ascending' else '-price'
		return queryset.order_by(expression)