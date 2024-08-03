from django.contrib import admin
from .models import Avisorden
from .models import Flota
from .models import InventarioS4
from .models import Ordenreserva
from .models import PlanAvisorden
from .models import PlanOrdenreserva
from .models import PlanReservas
from .models import Reservas

# Register your models here.

admin.site.register(Flota)
admin.site.register(InventarioS4)

admin.site.register(Ordenreserva)
admin.site.register(Reservas)
admin.site.register(Avisorden)

admin.site.register(PlanAvisorden)
admin.site.register(PlanOrdenreserva)
admin.site.register(PlanReservas)

