from rest_framework import routers
from django.urls import path,include

from .views import (UserProfileViewSet,CategoryListAPIView, CategoryDetailAPIView,SubCategoryListAPIView,SubCategoryDetailAPIView,
                    ProductListAPIView,ProductDetailAPIView,ReviewViewSet,CartViewSet,CartItemViewSet,RegisterView,LogoutView,LoginView)


router = routers.SimpleRouter()

router.register(r'user', UserProfileViewSet)
router.register(r'review', ReviewViewSet)
#router.register(r'cart', CartViewSet)
#router.register(r'cartitem', CartItemViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),


    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('cart/',CartViewSet.as_view(), name= 'cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post' : 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put':'update', 'delete' : 'destroy'}), ),


]