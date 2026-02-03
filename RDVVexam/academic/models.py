from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course.name} - {self.semester_number}"
    
class Subject(models.Model):
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return f"{self.name}({self.semester})"  

class Material(models.Model):
    MATERIAL_TYPES = (
        ('notes', 'Notes'),
        ('pyq', 'Previous Year Question'),
        ('syllabus', 'Syllabus'),
    )
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    material_type = models.CharField(max_length=10,choices=MATERIAL_TYPES)
    unit_name = models.CharField(max_length=100,blank=True,help_text="unit 1, unit2") 

    # Drive Link Logic
    drive_link = models.URLField(help_text="Google drive sharable link ")   

    #tracking
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}-{self.subject.name}"   