from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import json
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle
)

from .models import (
    Job, Subscriber, ContactMessage, SavedJob,
    CV, Skill, Education, Experience,
    Language, Project, Certification, Reference, CVSection
)
from applications.models import Application


# =========================
# JOB DETAIL
# =========================
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Login required to apply.")
            return redirect('job_detail', job_id=job.id)
        if getattr(user, "role", None) != "job_seeker":
            messages.error(request, "Only job seekers can apply.")
            return redirect('job_detail', job_id=job.id)
        if Application.objects.filter(user=user, job=job).exists():
            messages.warning(request, "You already applied.")
            return redirect('job_detail', job_id=job.id)
        Application.objects.create(user=user, job=job)
        messages.success(request, "Application submitted successfully!")
        return redirect('job_detail', job_id=job.id)

    return render(request, "job_detail.html", {"job": job})


# =========================
# JOB LIST
# =========================
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)
    saved_jobs = []
    if request.user.is_authenticated:
        saved_jobs = SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True)
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'saved_jobs': saved_jobs})


# =========================
# CONTACT
# =========================
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not all([name, email, subject, message_text]):
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": "All fields are required"})
            return render(request, "contact.html", {"success": False, "error": "All fields are required."})

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message_text)

        send_mail(
            subject=f"New Contact: {subject}",
            message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        try:
            html_content = render_to_string("emails/contact_auto_reply.html",
                {"name": name, "subject": subject, "message": message_text})
            email_msg = EmailMultiAlternatives(
                subject="We received your message - DEREJA.et",
                body="Thank you for contacting us.",
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()
        except Exception as e:
            print("Auto-reply error:", e)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        return render(request, "contact.html", {"success": True})

    return render(request, "contact.html")


# =========================
# SUBSCRIBE
# =========================
def subscribe(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    email = request.POST.get("email", "").strip()
    if not email:
        return JsonResponse({"error": "Email required"}, status=400)
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Invalid email"}, status=400)
    subscriber, created = Subscriber.objects.get_or_create(email=email)
    if not created:
        return JsonResponse({"message": "Already subscribed"})
    try:
        send_mail(
            subject="Welcome to DEREJA.et 🎉",
            message="You are now subscribed to job alerts.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
    except Exception as e:
        print("Subscribe email error:", e)
    return JsonResponse({"message": "Subscribed successfully!"})


# =========================
# NEWSLETTER
# =========================
def send_newsletter(request):
    subscribers = Subscriber.objects.all()
    for sub in subscribers:
        try:
            html_content = render_to_string("emails/newsletter.html", {"email": sub.email})
            email = EmailMultiAlternatives(
                subject="New Jobs Available - DEREJA.et",
                body="Check new jobs on DEREJA.et",
                from_email=settings.EMAIL_HOST_USER,
                to=[sub.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            print(f"Newsletter error ({sub.email}):", e)
    return JsonResponse({"message": "Newsletter sent successfully!"})


def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')


@login_required
def toggle_save_job(request, job_id):
    job = Job.objects.get(id=job_id)
    saved = SavedJob.objects.filter(user=request.user, job=job)
    if saved.exists():
        saved.delete()
        status = "removed"
        saved_state = False
    else:
        SavedJob.objects.create(user=request.user, job=job)
        status = "saved"
        saved_state = True
    count = SavedJob.objects.filter(user=request.user).count()
    return JsonResponse({"status": status, "saved": saved_state, "count": count})


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, "jobs/saved_jobs.html", {"saved_jobs": saved})


# ================================================================
#  CV BUILDER HELPERS
# ================================================================

def get_or_create_cv(user):
    cv, created = CV.objects.get_or_create(user=user)
    if created:
        _create_default_sections(cv)
    return cv


def _create_default_sections(cv):
    sections = [
        "personal", "summary", "skills", "education",
        "experience", "languages", "projects", "certifications", "references"
    ]
    for i, section_type in enumerate(sections):
        CVSection.objects.create(cv=cv, type=section_type, order=i)


def _base_context(cv, step):
    return {
        "cv": cv,
        "step": step,
        "steps": [
            ("1", "Import"),
            ("2", "Edit"),
            ("3", "Template"),
            ("4", "Download"),
        ],
        "templates": [
            ("modern",   "Modern"),
            ("classic",  "Classic"),
            ("dark",     "Dark"),
            ("europass", "Europass"),
        ],
        "font_sizes": [
            ("small",  "Small"),
            ("medium", "Medium"),
            ("large",  "Large"),
        ],
        "color_palettes": [
            "#4ca1af", "#2c3e50", "#e74c3c", "#27ae60",
            "#8e44ad", "#e67e22", "#2980b9", "#1abc9c",
            "#c0392b", "#16a085", "#d35400", "#2ecc71",
        ],
        "lang_levels": [
            ("A1", "A1"), ("A2", "A2"), ("B1", "B1"),
            ("B2", "B2"), ("C1", "C1"), ("C2", "C2"),
            ("native", "Native"),
        ],
        "lang_level_fields": [
            ("listening", "Listening"),
            ("reading",   "Reading"),
            ("writing",   "Writing"),
            ("speaking",  "Speaking"),
        ],
    }


# ================================================================
#  CV BUILDER VIEW
# ================================================================

@login_required
def cv_builder(request):
    step = request.GET.get("step", "1")
    cv   = get_or_create_cv(request.user)

    if step == "1":
        if request.method == "POST":
            action = request.POST.get("action")
            if action == "scratch":
                return redirect("/jobs/cv-builder/?step=2")
            if action == "upload" and request.FILES.get("cv_pdf"):
                extracted = _parse_pdf(request.FILES["cv_pdf"])
                ctx = _base_context(cv, "1_confirm")
                ctx["extracted"] = extracted
                return render(request, "jobs/cv_builder.html", ctx)
        return render(request, "jobs/cv_builder.html", _base_context(cv, "1"))

    if step == "1_confirm":
        if request.method == "POST":
            _fill_cv_from_post(cv, request.POST)
            return redirect("/jobs/cv-builder/?step=2")
        return redirect("/jobs/cv-builder/?step=1")

    if step == "2":
        if request.method == "POST":
            _save_step2(cv, request)
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"status": "ok"})
            return redirect("/jobs/cv-builder/?step=3")
        return render(request, "jobs/cv_builder.html", _base_context(cv, "2"))

    if step == "3":
        if request.method == "POST":
            cv.template  = request.POST.get("template", "modern")
            cv.font_size = request.POST.get("font_size", "medium")
            cv.color     = request.POST.get("color", "#4ca1af")
            cv.save()
            return redirect("/jobs/cv-builder/?step=4")
        return render(request, "jobs/cv_builder.html", _base_context(cv, "3"))

    if step == "4":
        return render(request, "jobs/cv_builder.html", _base_context(cv, "4"))

    return redirect("/jobs/cv-builder/?step=1")


# ================================================================
#  PDF PARSER
# ================================================================

def _parse_pdf(file):
    extracted = {
        "full_name": "", "email": "", "phone": "",
        "address": "", "website": "", "linkedin": "",
        "summary": "", "skills": [], "raw_text": "",
    }
    try:
        from pdfminer.high_level import extract_text
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name
        text = extract_text(tmp_path)
        os.unlink(tmp_path)
        extracted["raw_text"] = text
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        email_match = re.search(r"[\w.\-+]+@[\w.\-]+\.\w+", text)
        if email_match: extracted["email"] = email_match.group()
        phone_match = re.search(r"(\+?\d[\d\s\-().]{7,}\d)", text)
        if phone_match: extracted["phone"] = phone_match.group().strip()
        linkedin_match = re.search(r"linkedin\.com/in/[\w\-]+", text, re.IGNORECASE)
        if linkedin_match: extracted["linkedin"] = "https://" + linkedin_match.group()
        web_match = re.search(r"https?://(?!linkedin)[^\s]+", text)
        if web_match: extracted["website"] = web_match.group()
        if lines: extracted["full_name"] = lines[0]
        skills_section = re.search(r"skills[:\s]+([\s\S]{0,400}?)(?:\n[A-Z][a-z]+[\s:]+|\Z)", text, re.IGNORECASE)
        if skills_section:
            raw_skills = skills_section.group(1)
            extracted["skills"] = [s.strip() for s in re.split(r"[,\n•\-|]", raw_skills) if s.strip()]
        summary_match = re.search(r"(?:summary|profile|about me|objective)[:\s]+([\s\S]{0,600}?)(?:\n[A-Z]|\Z)", text, re.IGNORECASE)
        if summary_match: extracted["summary"] = summary_match.group(1).strip()
    except Exception as e:
        extracted["parse_error"] = str(e)
    return extracted


# ================================================================
#  FILL CV FROM CONFIRMATION
# ================================================================

def _fill_cv_from_post(cv, post):
    cv.full_name = post.get("full_name", "")
    cv.email     = post.get("email", "")
    cv.phone     = post.get("phone", "")
    cv.address   = post.get("address", "")
    cv.website   = post.get("website", "")
    cv.linkedin  = post.get("linkedin", "")
    cv.summary   = post.get("summary", "")
    cv.save()
    cv.skills_list.all().delete()
    for skill in post.getlist("skills[]"):
        if skill.strip():
            Skill.objects.create(cv=cv, name=skill.strip())


# ================================================================
#  SAVE STEP 2
# ================================================================

def _save_step2(cv, request):
    post = request.POST
    cv.full_name     = post.get("full_name", "")
    cv.email         = post.get("email", "")
    cv.phone         = post.get("phone", "")
    cv.address       = post.get("address", "")
    cv.website       = post.get("website", "")
    cv.linkedin      = post.get("linkedin", "")
    cv.github        = post.get("github", "")
    cv.nationality   = post.get("nationality", "")
    cv.date_of_birth = post.get("date_of_birth") or None
    cv.summary       = post.get("summary", "")
    if request.FILES.get("profile_image"):
        cv.profile_image = request.FILES["profile_image"]
    cv.save()

    cv.skills_list.all().delete()
    for skill, level in zip(post.getlist("skills[]"), post.getlist("skill_level[]")):
        if skill.strip():
            Skill.objects.create(cv=cv, name=skill.strip(), level=level)

    cv.educations.all().delete()
    schools = post.getlist("edu_school[]")
    degrees = post.getlist("edu_degree[]")
    fields  = post.getlist("edu_field[]")
    starts  = post.getlist("edu_start[]")
    ends    = post.getlist("edu_end[]")
    descs   = post.getlist("edu_desc[]")
    for i in range(len(schools)):
        if schools[i].strip():
            Education.objects.create(
                cv=cv, school=schools[i],
                degree=degrees[i] if i < len(degrees) else "",
                field=fields[i] if i < len(fields) else "",
                start_year=starts[i] if i < len(starts) else "",
                end_year=ends[i] if i < len(ends) else "",
                description=descs[i] if i < len(descs) else "",
            )

    cv.experiences.all().delete()
    titles    = post.getlist("exp_title[]")
    companies = post.getlist("exp_company[]")
    locations = post.getlist("exp_location[]")
    starts    = post.getlist("exp_start[]")
    ends      = post.getlist("exp_end[]")
    currents  = post.getlist("exp_current[]")
    descs     = post.getlist("exp_desc[]")
    for i in range(len(titles)):
        if titles[i].strip():
            Experience.objects.create(
                cv=cv, title=titles[i],
                company=companies[i] if i < len(companies) else "",
                location=locations[i] if i < len(locations) else "",
                start_date=starts[i] if i < len(starts) else "",
                end_date=ends[i] if i < len(ends) else "",
                current=str(i) in currents,
                description=descs[i] if i < len(descs) else "",
            )

    cv.languages.all().delete()
    lang_names = post.getlist("lang_name[]")
    listening  = post.getlist("lang_listening[]")
    reading    = post.getlist("lang_reading[]")
    writing    = post.getlist("lang_writing[]")
    speaking   = post.getlist("lang_speaking[]")
    for i in range(len(lang_names)):
        if lang_names[i].strip():
            Language.objects.create(
                cv=cv, name=lang_names[i],
                listening=listening[i] if i < len(listening) else "",
                reading=reading[i] if i < len(reading) else "",
                writing=writing[i] if i < len(writing) else "",
                speaking=speaking[i] if i < len(speaking) else "",
            )

    cv.projects.all().delete()
    proj_titles = post.getlist("proj_title[]")
    proj_descs  = post.getlist("proj_desc[]")
    proj_links  = post.getlist("proj_link[]")
    proj_starts = post.getlist("proj_start[]")
    proj_ends   = post.getlist("proj_end[]")
    for i in range(len(proj_titles)):
        if proj_titles[i].strip():
            Project.objects.create(
                cv=cv, title=proj_titles[i],
                description=proj_descs[i] if i < len(proj_descs) else "",
                link=proj_links[i] if i < len(proj_links) else "",
                start_date=proj_starts[i] if i < len(proj_starts) else "",
                end_date=proj_ends[i] if i < len(proj_ends) else "",
            )

    cv.certifications.all().delete()
    cert_names = post.getlist("cert_name[]")
    cert_orgs  = post.getlist("cert_org[]")
    cert_years = post.getlist("cert_year[]")
    cert_links = post.getlist("cert_link[]")
    for i in range(len(cert_names)):
        if cert_names[i].strip():
            Certification.objects.create(
                cv=cv, name=cert_names[i],
                organization=cert_orgs[i] if i < len(cert_orgs) else "",
                year=cert_years[i] if i < len(cert_years) else "",
                link=cert_links[i] if i < len(cert_links) else "",
            )

    cv.references.all().delete()
    ref_names     = post.getlist("ref_name[]")
    ref_companies = post.getlist("ref_company[]")
    ref_positions = post.getlist("ref_position[]")
    ref_emails    = post.getlist("ref_email[]")
    ref_phones    = post.getlist("ref_phone[]")
    for i in range(len(ref_names)):
        if ref_names[i].strip():
            Reference.objects.create(
                cv=cv, name=ref_names[i],
                company=ref_companies[i] if i < len(ref_companies) else "",
                position=ref_positions[i] if i < len(ref_positions) else "",
                email=ref_emails[i] if i < len(ref_emails) else "",
                phone=ref_phones[i] if i < len(ref_phones) else "",
            )


# ================================================================
#  PDF DOWNLOAD
# ================================================================

@login_required
def download_cv(request):
    cv = CV.objects.filter(user=request.user).last()
    if not cv:
        return HttpResponse("No CV found.", status=404)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="cv.pdf"'

    doc = SimpleDocTemplate(
        response, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
    )

    try:
        accent = colors.HexColor(cv.color or "#4ca1af")
    except Exception:
        accent = colors.HexColor("#4ca1af")

    dark   = colors.HexColor("#2c3e50")
    muted  = colors.HexColor("#6b7280")
    light  = colors.HexColor("#e5e7eb")
    styles = getSampleStyleSheet()

    logo_style = ParagraphStyle("Logo", parent=styles["Normal"],
        fontSize=8, textColor=colors.HexColor("#4ca1af"),
        alignment=2, fontName="Helvetica-Bold", spaceAfter=2)
    name_style = ParagraphStyle("CVName", parent=styles["Normal"],
        fontSize=20, textColor=dark, spaceAfter=4, fontName="Helvetica-Bold")
    contact_style = ParagraphStyle("CVContact", parent=styles["Normal"],
        fontSize=9, textColor=muted, spaceAfter=2)
    section_style = ParagraphStyle("CVSection", parent=styles["Normal"],
        fontSize=10, textColor=accent, spaceBefore=14, spaceAfter=4,
        fontName="Helvetica-Bold")
    entry_title_style = ParagraphStyle("EntryTitle", parent=styles["Normal"],
        fontSize=10, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1f2937"), spaceAfter=1)
    entry_sub_style = ParagraphStyle("EntrySub", parent=styles["Normal"],
        fontSize=9, textColor=muted, spaceAfter=2, fontName="Helvetica-Oblique")
    body_style = ParagraphStyle("Body", parent=styles["Normal"],
        fontSize=9, textColor=colors.HexColor("#374151"), spaceAfter=4, leading=13)
    tag_style = ParagraphStyle("Tag", parent=styles["Normal"],
        fontSize=9, textColor=accent, spaceAfter=6)
    date_style = ParagraphStyle("Date", parent=styles["Normal"],
        fontSize=9, textColor=muted, alignment=2)

    content = []

    # ── DEREJA.et logo (top right) ──
    content.append(Paragraph("DEREJA.et", logo_style))
    content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))

    # ── 1. PERSONAL INFO + SUMMARY ──
    content.append(Paragraph(cv.full_name or "Your Name", name_style))
    contact_parts = [p for p in [
        f"Email: {cv.email}" if cv.email else "",
        f"Phone: {cv.phone}" if cv.phone else "",
        f"Address: {cv.address}" if cv.address else "",
    ] if p]
    if contact_parts:
        content.append(Paragraph("   |   ".join(contact_parts), contact_style))
    link_parts = [p for p in [
        cv.website if cv.website and cv.website != "None" else "",
        cv.linkedin if cv.linkedin and cv.linkedin != "None" else "",
        cv.github if cv.github and cv.github != "None" else "",
    ] if p]
    if link_parts:
        content.append(Paragraph("   |   ".join(link_parts), contact_style))
    content.append(Spacer(1, 6))
    content.append(HRFlowable(width="100%", thickness=2, color=accent, spaceAfter=10))

    # ── 2. SUMMARY ──
    if cv.summary:
        content.append(Paragraph("SUMMARY", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        content.append(Paragraph(cv.summary, body_style))

    # ── 3. EDUCATION ──
    educations = list(cv.educations.all())
    if educations:
        content.append(Paragraph("EDUCATION", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        for edu in educations:
            degree = edu.degree + (f" in {edu.field}" if edu.field else "")
            dates = f"{edu.start_year} - {edu.end_year}"
            t = Table([[
                Paragraph(f"<b>{degree}</b>", entry_title_style),
                Paragraph(dates, date_style)
            ]], colWidths=["70%", "30%"])
            t.setStyle(TableStyle([
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 0),
                ("RIGHTPADDING", (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ]))
            content.append(t)
            content.append(Paragraph(edu.school, entry_sub_style))
            if edu.description:
                content.append(Paragraph(edu.description, body_style))
            content.append(Spacer(1, 6))

    # ── 4. LANGUAGES ──
    languages = list(cv.languages.all())
    if languages:
        content.append(Paragraph("LANGUAGES", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        for lang in languages:
            parts = []
            if lang.listening: parts.append(f"Listening: {lang.listening}")
            if lang.reading:   parts.append(f"Reading: {lang.reading}")
            if lang.writing:   parts.append(f"Writing: {lang.writing}")
            if lang.speaking:  parts.append(f"Speaking: {lang.speaking}")
            level_str = "   |   ".join(parts)
            content.append(Paragraph(
                f"<b>{lang.name}</b>" + (f"   —   {level_str}" if level_str else ""),
                body_style))
        content.append(Spacer(1, 4))

    # ── 5. WORK EXPERIENCE ──
    experiences = list(cv.experiences.all())
    if experiences:
        content.append(Paragraph("WORK EXPERIENCE", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        for exp in experiences:
            end = "Present" if exp.current else (exp.end_date or "")
            dates = f"{exp.start_date} - {end}" if exp.start_date else end
            loc = f", {exp.location}" if exp.location else ""
            t = Table([[
                Paragraph(f"<b>{exp.title}</b>", entry_title_style),
                Paragraph(dates, date_style)
            ]], colWidths=["70%", "30%"])
            t.setStyle(TableStyle([
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 0),
                ("RIGHTPADDING", (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ]))
            content.append(t)
            if exp.company:
                content.append(Paragraph(f"{exp.company}{loc}", entry_sub_style))
            if exp.description:
                content.append(Paragraph(exp.description, body_style))
            content.append(Spacer(1, 6))

    # ── 6. SKILLS ──
    skills = list(cv.skills_list.all())
    if skills:
        content.append(Paragraph("SKILLS", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        skill_text = "   •   ".join(
            f"{s.name} ({s.level.capitalize()})" if s.level else s.name for s in skills)
        content.append(Paragraph(skill_text, tag_style))
        content.append(Spacer(1, 4))

    # ── 7. CERTIFICATIONS ──
    certifications = list(cv.certifications.all())
    if certifications:
        content.append(Paragraph("CERTIFICATIONS", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        for cert in certifications:
            line = f"<b>{cert.name}</b>"
            if cert.organization: line += f"   —   {cert.organization}"
            if cert.year: line += f"   ({cert.year})"
            content.append(Paragraph(line, body_style))
        content.append(Spacer(1, 4))

    # ── 8. PROJECTS ──
    projects = list(cv.projects.all())
    if projects:
        content.append(Paragraph("PROJECTS", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        for proj in projects:
            content.append(Paragraph(f"<b>{proj.title}</b>", entry_title_style))
            if proj.start_date:
                content.append(Paragraph(f"{proj.start_date} - {proj.end_date}", entry_sub_style))
            if proj.description:
                content.append(Paragraph(proj.description, body_style))
            if proj.link:
                content.append(Paragraph(proj.link, entry_sub_style))
            content.append(Spacer(1, 6))

    # References
    references = list(cv.references.all())
    if references:
        content.append(Paragraph("REFERENCES", section_style))
        content.append(HRFlowable(width="100%", thickness=0.5, color=light, spaceAfter=6))
        for ref in references:
            line = f"<b>{ref.name}</b>"
            if ref.position: line += f", {ref.position}"
            if ref.company:  line += f" — {ref.company}"
            content.append(Paragraph(line, body_style))
            contact = "   |   ".join(p for p in [ref.email, ref.phone] if p)
            if contact:
                content.append(Paragraph(contact, entry_sub_style))
        content.append(Spacer(1, 4))

    doc.build(content)
    return response


# ================================================================
#  REORDER SECTIONS
# ================================================================

@login_required
def reorder_sections(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        for item in data:
            CVSection.objects.filter(
                id=item["id"], cv__user=request.user
            ).update(order=item["order"])
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ================================================================
#  AJAX SAVE
# ================================================================

@login_required
def save_cv_ajax(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    cv = get_or_create_cv(request.user)
    _save_step2(cv, request)
    return JsonResponse({"status": "ok"})