from django.contrib import admin

from postcode.models import Postcode

class PostcodeAdmin(admin.ModelAdmin):
    list_display = ('postcode', 'city', 'active')
    search_fields = ['postcode']
    list_filter = ('active', )

admin.site.register(Postcode, PostcodeAdmin)