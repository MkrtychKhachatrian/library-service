from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user__id = self.request.query_params.get("user_id")

        queryset = self.queryset

        if is_active:
            queryset = queryset.filter(actual_return_date=None)

        if self.request.user.is_staff and user__id:
            queryset = queryset.filter(user_id=user__id)

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class CreateBorrowingViewSet(APIView):
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        expected_return_date = serializer.data["expected_return_date"]
        actual_return_date = serializer.data["actual_return_date"]
        book = get_object_or_404(Book, pk=serializer.data["book"])

        if book.inventory == 0:
            raise ValidationError({"The book inventory is 0!"})

        book.inventory = book.inventory - 1
        book.save()

        user = self.request.user

        Borrowing.objects.create(
            expected_return_date=expected_return_date,
            actual_return_date=actual_return_date,
            book=book,
            user=user,
        )

        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReturnBorrowingViewSet(APIView):
    serializer_class = BorrowingReturnSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, pk):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        borrowing = get_object_or_404(Borrowing, pk=pk)

        if borrowing.actual_return_date:
            raise ValidationError("The borrowing has already been returned")

        borrowing.actual_return_date = serializer.data.get("actual_return_date")
        borrowing.save()

        book = borrowing.book
        book.inventory = book.inventory + 1
        book.save()

        return Response(status=status.HTTP_200_OK)
