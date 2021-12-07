from django.urls    import path

from products.views import (
    MenuView,
    ProductView
)

urlpatterns = [
    path('/menus', MenuView.as_view()),
    path('', ProductView.as_view())
]
