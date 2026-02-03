from django.contrib import admin
from django.urls import path
from academic.views import admin_dashboard,home,semester_list,subject_list,subject_detail,download_material
from academic.views import search,about # Import add karna

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-dashboard/', admin_dashboard, name='dashboard'),    
    
    path('',home,name='home'),

 # Naye Raaste
    path('course/<int:course_id>/', semester_list, name='semesters'),
    path('semester/<int:semester_id>/', subject_list, name='subjects'),
    
# Naye Raaste (Subject Detail & Download)
    path('subject/<int:subject_id>/', subject_detail, name='subject_detail'),
    path('download/<int:material_id>/', download_material, name='download_material'),

    path('search/', search, name='search'),
    path('about/', about, name='about'), #about me


]
