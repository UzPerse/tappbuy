from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from . import settings
from store.views import *

# Admin panel title of header
admin.site.site_header = "TAPP-BUY"

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/store-list/', StoreDetailView.as_view()),
    path('api/v1/category-list/', CategoryListView.as_view()),
    path('api/v1/product-list/', ProductListView.as_view()),
    path('api/v1/product-detail/<int:pk>/', ProductDetailView.as_view()),
    path('api/v1/variant-list/', ProductVariantListView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
