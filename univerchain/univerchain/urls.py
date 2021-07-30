import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("univerchain.apps.pages.urls", namespace="pages")),
    path("univercoin/", include("univerchain.apps.univercoin.urls", namespace="univercoin")),
    path("accounts/", include("univerchain.apps.accounts.urls", namespace="accounts")),
    path("store/", include("univerchain.apps.store.urls", namespace="store")),
    path("cart/", include("univerchain.apps.cart.urls", namespace="cart")),
    path("orders/", include("univerchain.apps.orders.urls", namespace="orders")),
    path("attendance/", include("univerchain.apps.attendance.urls", namespace="attendance")),
    # path("__debug__/", include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)