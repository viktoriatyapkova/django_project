# Generated by Django 5.0.4 on 2024-05-22 13:45

import datetime
import django.core.validators
import django.db.models.deletion
import python_project_app.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Marketplace",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_created],
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_modified],
                        verbose_name="modified",
                    ),
                ),
                (
                    "title",
                    models.TextField(max_length=250, null=True, verbose_name="title"),
                ),
                (
                    "url_address",
                    models.URLField(blank=True, null=True, verbose_name="url address"),
                ),
            ],
            options={
                "verbose_name": "marketplace",
                "verbose_name_plural": "marketplaces",
                "db_table": '"online"."marketplace"',
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_created],
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_modified],
                        verbose_name="modified",
                    ),
                ),
                ("title", models.TextField(max_length=250, verbose_name="title")),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "rating",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(5.0),
                        ],
                        verbose_name="rating",
                    ),
                ),
            ],
            options={
                "verbose_name": "shop",
                "verbose_name_plural": "shops",
                "db_table": '"online"."shop"',
                "ordering": ["title", "rating"],
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_created],
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_modified],
                        verbose_name="modified",
                    ),
                ),
                (
                    "money",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=11,
                        validators=[python_project_app.models.check_positive],
                        verbose_name="money",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "client",
                "verbose_name_plural": "clients",
                "db_table": '"online"."client"',
            },
        ),
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_created],
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_modified],
                        verbose_name="modified",
                    ),
                ),
                ("title", models.TextField(max_length=250, verbose_name="title")),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        blank=True,
                        default=datetime.datetime.now,
                        null=True,
                        verbose_name="start date",
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        blank=True,
                        default=datetime.datetime.now,
                        null=True,
                        verbose_name="end date",
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="python_project_app.shop",
                        verbose_name="shop",
                    ),
                ),
            ],
            options={
                "verbose_name": "discount",
                "verbose_name_plural": "discounts",
                "db_table": '"online"."discount"',
                "ordering": ["title", "start_date", "end_date"],
            },
        ),
        migrations.CreateModel(
            name="ShopToClient",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        default=python_project_app.models.get_datetime,
                        null=True,
                        validators=[python_project_app.models.check_created],
                        verbose_name="created",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="python_project_app.client",
                        verbose_name="client",
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="python_project_app.shop",
                        verbose_name="shop",
                    ),
                ),
            ],
            options={
                "verbose_name": "relationship shop client",
                "verbose_name_plural": "relationships shop client",
                "db_table": '"online"."shop_to_client"',
            },
        ),
        migrations.AddField(
            model_name="client",
            name="shops",
            field=models.ManyToManyField(
                through="python_project_app.ShopToClient",
                to="python_project_app.shop",
                verbose_name="shops",
            ),
        ),
        migrations.CreateModel(
            name="ShopToMarketplace",
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
                    "marketplace",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="python_project_app.marketplace",
                        verbose_name="marketplace",
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="python_project_app.shop",
                        verbose_name="shop",
                    ),
                ),
            ],
            options={
                "verbose_name": "relationship shop marketplace",
                "verbose_name_plural": "relationships shop marketplace",
                "db_table": '"online"."shop_to_marketplace"',
                "unique_together": {("shop", "marketplace")},
            },
        ),
        migrations.AddField(
            model_name="shop",
            name="marketplaces",
            field=models.ManyToManyField(
                through="python_project_app.ShopToMarketplace",
                to="python_project_app.marketplace",
                verbose_name="Marketplace",
            ),
        ),
        migrations.AddField(
            model_name="marketplace",
            name="shops",
            field=models.ManyToManyField(
                through="python_project_app.ShopToMarketplace",
                to="python_project_app.shop",
            ),
        ),
    ]
