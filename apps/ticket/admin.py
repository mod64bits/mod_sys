from django.contrib import admin

from .models import Ticket, Atendimento, IamagemAtendimento, MensagemAtendimento, UploadImagensAtendimento


admin.site.register(Ticket)
admin.site.register(Atendimento)
admin.site.register(IamagemAtendimento)
admin.site.register(MensagemAtendimento)
admin.site.register(UploadImagensAtendimento)
