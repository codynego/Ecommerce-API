from django.urls import path
from .views import CategoryList, ProductView


urlpatterns = [
	path('category/', CategoryList.as_view(), name="category"),
	path('product/', ProductView.as_view(), name="product"),
]
