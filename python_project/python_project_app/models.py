from django.db import models
from uuid import uuid4
from datetime import datetime, date, timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


TITLE_MAX_LENGTH = 250
DESCRIPTION_MAX_LEN = 1000

def get_datetime():
    return datetime.now(timezone.utc)

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

def check_created(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt},
        )

def check_modified(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt},
        )

class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_created],
    )

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_modified],
    )
    
    class Meta:
        abstract = True

class Marketplace(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=TITLE_MAX_LENGTH)
    url_address = models.URLField(_('url address'), null=False, blank=False)

    shops = models.ManyToManyField('Shop', through='ShopToMarketplace')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = '"online"."marketplace"'
        ordering = ['title']
        verbose_name = _('marketplace')
        verbose_name_plural = _('marketplaces')


class Shop(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), null=False, blank=False, max_length=DESCRIPTION_MAX_LEN)
    rating = models.FloatField(_('rating'), null=False, blank=False)

    marketplaces = models.ManyToManyField(Marketplace, verbose_name=_('Marketplace'), through='ShopToMarketplace')

    def __str__(self):
        return f'{self.title}, {self.description}, {self.rating}'

    class Meta:
        db_table = '"online"."shop"'
        ordering = ['title', 'rating']
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

class Discount(UUIDMixin, CreatedMixin, ModifiedMixin):
    shop_id = models.ForeignKey(Shop, verbose_name=_('shop'), on_delete=models.CASCADE)
    title = models.TextField(_('title'), null=True, blank=True, max_length=TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LEN)
    start_date = models.DateField(_('start date'), null=True, blank=True, default=datetime.now)
    end_date = models.DateField(_('end date'), null=True, blank=True, default=datetime.now)

    def __str__(self):
        return f'{self.title}, {self.description}, {self.start_date}, {self.end_date}'

    class Meta:
        db_table = '"online"."discount"'
        ordering = ['title', 'start_date', 'end_date']
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')


class ShopToMarketplace(models.Model):
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), on_delete=models.CASCADE)
    marketplace = models.ForeignKey(Marketplace, verbose_name=_('marketplace'), on_delete=models.CASCADE)
    
    class Meta:
        db_table = '"online"."shop_to_marketplace"'
        unique_together = (
            ('shop', 'marketplace'),
        )
        verbose_name = _('relationship shop marketplace')
        verbose_name_plural = _('relationships shop marketplace')
