from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
import base64

ABSOLUT_PATH = r"C:/Users/k_mir/OneDrive/Desktop/Django/sis3/resume_project/cv"

def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")
        employed = request.POST.get("employed", "")
        picture = request.FILES.get("picture", "")

        if employed == 'on':
            employed = True
        else:
            employed = False
        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school,
                          university=university, previous_work=previous_work, skills=skills, employed=employed,
                          profile_picture=picture)
        profile.save()
    return render(request, 'pdf/accept.html')


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile,
                            'get_image_as_base64': get_image_as_base64(user_profile.profile_picture.path)})
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'enable-local-file-access': True,
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response


def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})


def get_image_as_base64(filepath):
    with open(filepath, 'rb') as image:
        return base64.b64encode(image.read()).decode('utf-8')
