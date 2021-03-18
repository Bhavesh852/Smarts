from django.contrib import admin

# Register your models here.
from .models import Vote_Groups, Startvote, Vote_Result, Maintenance, Payment_detail, Recent_Maintenance

admin.site.register(Vote_Groups)
admin.site.register(Startvote)
admin.site.register(Vote_Result)
admin.site.register(Maintenance)
admin.site.register(Payment_detail)
admin.site.register(Recent_Maintenance)