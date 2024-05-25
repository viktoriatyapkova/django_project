from django.db import models
from uuid import uuid4
from datetime import datetime, date, timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf.global_settings import AUTH_USER_MODEL


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
    title = models.TextField(_('title'), null=True, blank=False, max_length=TITLE_MAX_LENGTH)
    url_address = models.URLField(_('url address'), null=True, blank=True)

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
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LEN)
    rating = models.FloatField(_('rating'), null=True, blank=True,  validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]) # добавить атрибут-выборку, чтобы там был выбор только он 0 до 5

    marketplaces = models.ManyToManyField(Marketplace, verbose_name=_('Marketplace'), through='ShopToMarketplace')

    def __str__(self):
        return f'{self.title}, {self.description}, {self.rating}'

    class Meta:
        db_table = '"online"."shop"'
        ordering = ['title', 'rating']
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    
class Discount(UUIDMixin, CreatedMixin, ModifiedMixin):
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), on_delete=models.SET_NULL, null=True, blank=True)
    title = models.TextField(_('title'), null=False, blank=False, max_length=TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), null=True, blank=True, max_length=DESCRIPTION_MAX_LEN)
    start_date = models.DateField(_('start date'), null=True, blank=True, default=date.today) 
    end_date = models.DateField(_('end date'), null=True, blank=True, default=date.today)

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError({'start_date': "Дата начала не может быть позже даты окончания."})
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': "Дата окончания не может быть раньше даты начала."})
        super().clean()
    
    def __str__(self):
        return f'{self.title}, {self.description}, {self.start_date}, {self.end_date}'

    class Meta:
        db_table = '"online"."discount"'
        ordering = ['title', 'start_date', 'end_date']
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')



def check_positive(number) -> None:
    if number < 0:
        raise ValidationError('value should be equal or greater than zero')

class ShopToMarketplace(models.Model):
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), on_delete=models.SET_NULL, null=True, blank=True)
    marketplace = models.ForeignKey(Marketplace, verbose_name=_('marketplace'), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = '"online"."shop_to_marketplace"'
        unique_together = (
            ('shop', 'marketplace'),
        )
        verbose_name = _('relationship shop marketplace')
        verbose_name_plural = _('relationships shop marketplace')


class Client(UUIDMixin, CreatedMixin, ModifiedMixin):
    money = models.DecimalField(
        verbose_name=_('money'),
        decimal_places=2,
        max_digits=11,
        default=0,
        validators=[check_positive],
    )
    user = models.OneToOneField(AUTH_USER_MODEL, unique=True, verbose_name=_('user'), on_delete=models.CASCADE)
    shops = models.ManyToManyField(Shop, through='ShopToClient', verbose_name=_('shops'))

    class Meta:
        db_table = '"online"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def first_name(self) -> str:
        return self.user.first_name

    @property
    def last_name(self) -> str:
        return self.user.last_name

    def __str__(self) -> str:
        return f'{self.username} ({self.first_name} {self.last_name})'
    
class ShopToClient(UUIDMixin, CreatedMixin):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name=_('shop'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('client'))

    class Meta:
        db_table = '"online"."shop_to_client"'
        verbose_name = _('relationship shop client')
        verbose_name_plural = _('relationships shop client')
