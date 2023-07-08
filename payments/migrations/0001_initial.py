# Generated by Django 4.2.2 on 2023-07-08 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "Pending"), ("PAID", "Paid")], max_length=7
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PAYMENT", "Payment"), ("FINE", "Fine")], max_length=7
                    ),
                ),
                ("session_url", models.CharField(max_length=255)),
                ("session_id", models.CharField(max_length=255)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="borrowings.borrowing",
                    ),
                ),
            ],
        ),
    ]
