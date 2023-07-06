from rest_framework import routers
from django.urls import path, include

from borrowings.views import BorrowingViewSet, CreateBorrowingViewSet

router = routers.DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = [
    path("create/", CreateBorrowingViewSet.as_view()),
    path("", include(router.urls)),
]

app_name = "borrowings"
