from django.urls import path
from .views import (
    SignInView,
    SignOutView,
    SignUpView,
    CategoriesView,
    CatalogView,
    TagsView,
    LimitedEditionProductsView,
    ProductDetailsView,
    AddReviewView,
    BasketView,
    PopularProductsView,
    BannerView,
    OrderView,
    PaymentView,
    ProfileView,
    ProfilePasswordView,
    ProfileAvatarView,
)

urlpatterns = [
    path('sign-in', SignInView.as_view()),
    path('sign-out', SignOutView.as_view()),
    path('sign-up', SignUpView.as_view()),
    path('categories', CategoriesView.as_view()),
    path('tags', TagsView.as_view()),
    path('catalog', CatalogView.as_view()),
    path('products/popular', PopularProductsView.as_view()),
    path('products/limited', LimitedEditionProductsView.as_view()),
    path('product/<int:pk>', ProductDetailsView.as_view()),
    path('product/<int:pk>/reviews', AddReviewView.as_view()),
    path('basket', BasketView.as_view()),
    path('banners', BannerView.as_view()),
    path('orders', OrderView.as_view()),
    path('order/<int:pk>', OrderView.as_view()),
    path('payment/<int:pk>', PaymentView.as_view()),
    path('profile', ProfileView.as_view()),
    path('profile/password', ProfilePasswordView.as_view()),
    path('profile/avatar', ProfileAvatarView.as_view()),

]

