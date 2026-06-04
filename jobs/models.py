from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name   
    
class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, default='Unknown Company')
    location = models.CharField(max_length=200)

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField()

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    is_remote = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email    
class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job') 

# ===================== CV =====================
class CV(models.Model):

    TEMPLATE_CHOICES = [
        ("modern", "Modern"),
        ("classic", "Classic"),
        ("dark", "Dark"),
        ("europass", "Europass"),
    ]

    FONT_SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cv")

    # ---------- Personal Info ----------
    full_name       = models.CharField(max_length=100, blank=True)
    email           = models.EmailField(blank=True)
    phone           = models.CharField(max_length=20, blank=True)
    address         = models.CharField(max_length=255, blank=True)
    website         = models.URLField(blank=True, null=True)
    linkedin        = models.URLField(blank=True, null=True)
    github          = models.URLField(blank=True, null=True)
    profile_image   = models.ImageField(upload_to="cv_profiles/", blank=True, null=True)
    nationality     = models.CharField(max_length=100, blank=True)
    date_of_birth   = models.DateField(blank=True, null=True)

    # ---------- Summary ----------
    summary         = models.TextField(blank=True)

    # ---------- Template & Style ----------
    template        = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default="modern")
    font_size       = models.CharField(max_length=10, choices=FONT_SIZE_CHOICES, default="medium")
    color           = models.CharField(max_length=20, default="#4ca1af")  # hex color

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CV of {self.user.username}"


# ===================== SKILL =====================
class Skill(models.Model):
    cv      = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="skills_list")
    name    = models.CharField(max_length=100)
    level   = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("expert", "Expert"),
        ],
        blank=True
    )

    def __str__(self):
        return self.name


# ===================== EDUCATION =====================
class Education(models.Model):
    cv          = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="educations")
    school      = models.CharField(max_length=200)
    degree      = models.CharField(max_length=200, blank=True)
    field       = models.CharField(max_length=200, blank=True)
    start_year  = models.CharField(max_length=20, blank=True)
    end_year    = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} - {self.school}"


# ===================== EXPERIENCE =====================
class Experience(models.Model):
    cv          = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="experiences")
    title       = models.CharField(max_length=100)
    company     = models.CharField(max_length=100, blank=True)
    location    = models.CharField(max_length=100, blank=True)
    start_date  = models.CharField(max_length=50, blank=True)
    end_date    = models.CharField(max_length=50, blank=True)
    current     = models.BooleanField(default=False)   # "I currently work here"
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


# ===================== LANGUAGE =====================
class Language(models.Model):
    LEVEL_CHOICES = [
        ("A1", "A1 - Beginner"),
        ("A2", "A2 - Elementary"),
        ("B1", "B1 - Intermediate"),
        ("B2", "B2 - Upper Intermediate"),
        ("C1", "C1 - Advanced"),
        ("C2", "C2 - Proficient"),
        ("native", "Native"),
    ]

    cv          = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="languages")
    name        = models.CharField(max_length=100)
    listening   = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)
    reading     = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)
    writing     = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)
    speaking    = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)

    def __str__(self):
        return self.name


# ===================== PROJECT =====================
class Project(models.Model):
    cv          = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="projects")
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link        = models.URLField(blank=True, null=True)
    start_date  = models.CharField(max_length=50, blank=True)
    end_date    = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


# ===================== CERTIFICATION =====================
class Certification(models.Model):
    cv           = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="certifications")
    name         = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    year         = models.CharField(max_length=20, blank=True)
    link         = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# ===================== REFERENCE =====================
class Reference(models.Model):
    cv          = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="references")
    name        = models.CharField(max_length=200)
    company     = models.CharField(max_length=200, blank=True)
    position    = models.CharField(max_length=200, blank=True)
    email       = models.EmailField(blank=True)
    phone       = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


# ===================== CV SECTION ORDER =====================
class CVSection(models.Model):
    SECTION_TYPES = [
        ("personal",        "Personal Info"),
        ("summary",         "Summary"),
        ("skills",          "Skills"),
        ("education",       "Education"),
        ("experience",      "Experience"),
        ("languages",       "Languages"),
        ("projects",        "Projects"),
        ("certifications",  "Certifications"),
        ("references",      "References"),
    ]

    cv          = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="sections")
    type        = models.CharField(max_length=30, choices=SECTION_TYPES)
    order       = models.IntegerField(default=0)
    is_visible  = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.cv.user.username} - {self.type}"
# ===================== APPLICATION =====================
class Application(models.Model):

    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('reviewed',   'Reviewed'),
        ('shortlisted','Shortlisted'),
        ('rejected',   'Rejected'),
    ]

    job          = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name    = models.CharField(max_length=200)
    email        = models.EmailField()
    cv_file      = models.FileField(upload_to='applications/')
    cover_letter = models.TextField(blank=True)

    # AI screening fields
    match_score  = models.IntegerField(null=True, blank=True)       # 0–100
    matched_skills   = models.TextField(blank=True)                 # stored as comma-separated
    missing_skills   = models.TextField(blank=True)
    experience_fit   = models.CharField(max_length=20, blank=True)  # Poor/Fair/Good/Excellent
    verdict          = models.CharField(max_length=30, blank=True)  # Strong match etc.
    ai_summary       = models.TextField(blank=True)
    interview_questions = models.TextField(blank=True)

    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-match_score', '-applied_at']  # best matches first automatically

    def __str__(self):
        return f"{self.full_name} → {self.job.title}"    