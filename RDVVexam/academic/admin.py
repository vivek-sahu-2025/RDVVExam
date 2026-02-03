from django.contrib import admin
from .models import Course,Semester,Subject,Material

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'material_type', 'views_count', 'downloads_count')
    list_filter = ('material_type','subject')
    search_fields = ('title','subject__name')

admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Material, MaterialAdmin)    