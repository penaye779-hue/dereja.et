from django.shortcuts import render
from jobs.models import Job, Category
from django.core.paginator import Paginator

def home(request):
    jobs = Job.objects.all().order_by('-created_at')  # ✅ IMPORTANT LINE
    categories = Category.objects.all()

    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    category = request.GET.get('category')
    remote = request.GET.get('remote')

    if query:
        jobs = jobs.filter(title__icontains=query)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if remote:
        jobs = jobs.filter(is_remote=True)

    if category:
        jobs = jobs.filter(category_id=category)

    # Pagination
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'jobs': jobs,
        'categories': categories
    })