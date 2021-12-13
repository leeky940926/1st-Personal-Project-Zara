from django.urls    import path

from products.views import (
    ProductView,
    DetailProductView
)

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', DetailProductView.as_view())
    

]
