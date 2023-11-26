from django.contrib import admin

from .models import Ticket, Atendimento, IamagemAtendimento


admin.site.register(Ticket)
admin.site.register(Atendimento)
admin.site.register(IamagemAtendimento)
