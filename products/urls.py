from django.urls    import path

from products.views import MenuView

urlpatterns = [
    path('/menus', MenuView.as_view())
]
