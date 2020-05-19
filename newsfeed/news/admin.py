from django.contrib import admin
from .models import currency
from .models import indexes
from .models import stocknews
from .models import equities
from .models import eqnews
from .models import fxnews



# Register your models here.
admin.site.register(currency)
admin.site.register(indexes)
admin.site.register(stocknews)
admin.site.register(equities)
admin.site.register(eqnews)
admin.site.register(fxnews)
