from django.shortcuts import render
from django.db.models import Sum
from .models import Material, Course, Semester, Subject
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404 # <-- Ye naya import zaroori h
from django.shortcuts import redirect # <-- Ye import zaroori hai upar
from django.db.models import Q # <-- Ye import zaroori hai (Search query ke liye)


# Ye check karega ki user Admin hai ya nahi. Agar nahi hai to login page par bhej dega.
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # 1. Total Counts nikalo
    total_materials = Material.objects.count()
    total_courses = Course.objects.count()
    
    # 2. Total Views aur Downloads ka sum (jod) nikalo
    # Agar data nahi h to 0 maano (fallback)
    total_views = Material.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
    total_downloads = Material.objects.aggregate(Sum('downloads_count'))['downloads_count__sum'] or 0
    
    # 3. Top 5 Popular Notes nikalo (Graph ke liye)
    popular_notes = Material.objects.order_by('-downloads_count')[:5]
    
    # Data ko graph ke format me ready karo
    note_titles = [note.title for note in popular_notes]
    note_downloads = [note.downloads_count for note in popular_notes]

    context = {
        'total_materials': total_materials,
        'total_courses': total_courses,
        'total_views': total_views,
        'total_downloads': total_downloads,
        'note_titles': note_titles,
        'note_downloads': note_downloads,
    }
    
    return render(request, 'dashboard.html', context)


def home(request):
    courses = Course.objects.all()
    return render(request,'index.html',{'courses': courses})

# 1. Semesters dikhane ke liye
def semester_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    semesters = Semester.objects.filter(course=course)
    return render(request, 'semester_list.html', {'course': course, 'semesters': semesters})


# 2. Subjects dikhane ke liye
def subject_list(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    return render(request, 'subject_list.html', {'semester': semester, 'subjects': subjects})


# 1. Main Subject Dashboard
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Alag-alag type ka maal nikalo
    notes = Material.objects.filter(subject=subject, material_type='notes').order_by('unit_name')
    pyqs = Material.objects.filter(subject=subject, material_type='pyq').order_by('-title') # Newest first
    syllabus = Material.objects.filter(subject=subject, material_type='syllabus').first()
    
    context = {
        'subject': subject,
        'notes': notes,
        'pyqs': pyqs,
        'syllabus': syllabus
    }
    return render(request, 'subject_detail.html', context)

# 2. Secret Download Counter (Jo dikhta nahi par kaam karta hai)
def download_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    
    # 1. Count badhao
    material.downloads_count += 1
    material.save()
    
    # 2. Asli Google Drive link par bhej do
    return redirect(material.drive_link)

def search(request):
    query = request.GET.get('q') # URL se 'q' uthayega
    results = []
    
    if query:
        # Subject ka naam ya Course ka naam dhundo (Case insensitive)
        results = Subject.objects.filter(
            Q(name__icontains=query) | 
            Q(semester__course__name__icontains=query)
        )
    
    return render(request, 'search_results.html', {'results': results, 'query': query})

def about(request):
    return render(request, 'about.html')

# views.py ke andar
def contribute(request):
    return render(request, 'contribute.html') # Yahan apne HTML file ka exact naam daalna