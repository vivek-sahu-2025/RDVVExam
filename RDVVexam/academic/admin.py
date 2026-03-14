from django.contrib import admin
from .models import Course,Semester,Subject,Material
from django.utils.html import format_html

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'material_type', 'views_count', 'downloads_count')
    list_filter = ('material_type','subject')
    search_fields = ('title','subject__name')

admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Material, MaterialAdmin)    
# Admin Panel ka Header aur Title customize karna
admin.site.site_header = "Mera Admin Portal"

# Yahan hum index_title mein HTML button ghusa rahe hain
admin.site.index_title = format_html(
    'Welcome to Administration | <a href="/my-dashboard/" style="background-color: #417690; color: white; padding: 5px 12px; border-radius: 4px; text-decoration: none; font-size: 14px; margin-left: 100px;">🚀 Go to My Dashboard</a>'
)