from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, DeleteView
from usermanagement.models import Consultation, Examen, Medicament, Patient
from .formulaire import  MedicineForm, PatientForm, ConsultationForm, ExamForm
from django.urls import reverse_lazy

# Create your views here.


#---------------------------------------------DESCRIPTION-----------------------------------------#
#---------------------------------------------DESCRIPTION-----------------------------------------#
#---------------------------------------------DESCRIPTION-----------------------------------------#
def index(request):
    return render(request, 'usermanagement/description/index.html')    

def home(request):
    if request.user.role == "Receptionist":
        return viewpatientlist(request)
    elif request.user.role == "Doctor":
        return doctorviewpl(request)
    elif request.user.role == "Pharmacist":
        return pharmacistviewpl(request)  
    elif request.user.role == "Labtech":
        return labtechviewpl(request)  
    elif request.user.role == "Accountant":
        return cahierviewpl(request)  
    else:
        return render(request, 'usermanagement/home.html')


def reception(request):
     return render(request, 'usermanagement/description/reception.html')


def about(request):
    return render(request, 'usermanagement/description/about.html')


def pharmacy(request):
    return render(request, 'usermanagement/description/pharmacy.html')

def cashdesk(request):
    return render(request, 'usermanagement/description/cashdesk.html' )

def laboratory(request):
    return render(request, 'usermanagement/description/laboratory.html' )

def dentalunit(request):
    return render(request, 'usermanagement/description/dentalunit.html' )

def genMedicine(request):
    return render(request, 'usermanagement/description/genMedicine.html' )

def ophtalmoservice(request):
    return render(request, 'usermanagement/description/ophtalmoservice.html' )


#-------------------------------------RECEPTIONIST-----------------------------------------#
#-------------------------------------RECEPTIONIST-----------------------------------------#
#-------------------------------------RECEPTIONIST-----------------------------------------#

def addPatient(request):
    #traitement de la requete post
    if request.method == "POST":
        form = PatientForm(request.POST).save()
        return viewpatientlist(request) #redirect('/addPatient')
    else:   
        form = PatientForm()    
    return render(request, 'usermanagement/receptionist/addPatient.html', {'form':form})
    #objet formulaire sous forme d'un dictionnaire:{'form':form}


def receptionist(request):
    return render(request, 'usermanagement/receptionist/receptionist.html')


def viewpatientlist(request):
    if request.method == 'POST':
        name = ''
        if 'name' in request.POST:
            name = request.POST['name']
        patients = Patient.objects.filter(FirstName__contains=name)
        patientList = []
        for p in patients:
            if not [p.FirstName,p.LastName,p.CNI_number] in patientList:
                patientList.append([p.FirstName,p.LastName,p.CNI_number])
        context = {
            'patientList':patientList,
            'patients': patients,
            'selectName':name,
        }
        return render(request, 'usermanagement/receptionist/viewpatientlist.html', context)
    patients = Patient.objects.all()
    patientList = []
    for p in patients:
        if not [p.FirstName,p.LastName,p.CNI_number] in patientList:
            patientList.append([p.FirstName,p.LastName,p.CNI_number])
    context = {
        'patientList':patientList,
        'patients': patients,
    }
    return render(request, 'usermanagement/receptionist/viewpatientlist.html', context)

class PatientUpdateView(UpdateView):
    model = Patient
    context = {
        'patients': Patient.objects.all()
    }
    fields = '__all__'
    template_name = 'usermanagement/receptionist/patient_update_form.html'


class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy('usermanagement:viewpatientlist')

def NewRegistration(request,nom,prenom,cni):
    if request.method == 'POST':
        PatientForm(request.POST).save()
        return viewpatientlist(request)
    p = Patient.objects.filter(FirstName=nom,LastName=prenom,CNI_number=cni)
    if not p is None:
        p = p[0]
        form = PatientForm(initial={
            'FirstName': p.FirstName.__str__(),
            'LastName': p.LastName.__str__(),
            'sexe': p.sexe.__str__(),
            'BirthDate': p.BirthDate.__str__(),
            'CNI_number': p.CNI_number.__str__(),
            'Address': p.Address.__str__(),
            'Phone_number': p.Phone_number.__str__(),
            'Email_address': p.Email_address.__str__(),
            })
        context = {'form':form,'patient':p}
        return render(request=request,template_name='usermanagement/receptionist/NewRegistration.html',context=context)
    return render(request=request,template_name='usermanagement/receptionist/NewRegistration.html')

def patientDetails(request,nom,prenom,cni):
    p = Patient.objects.filter(FirstName=nom,LastName=prenom,CNI_number=cni)
    context = {'p':p[0],'patients':p}
    if request.user.role == "Receptionist":
        return render(request, 'usermanagement/receptionist/patientDetails.html',context)
    if request.user.role == "Doctor":
        return render(request, 'usermanagement/doctor/patientDetails.html',context)
    return home(request)
    

#'''---------------------------------------------------------------------------------------DOCTOR--------------------------------------'''
#'''---------------------------------------------------------------------------------------DOCTOR--------------------------------------'''
#'''---------------------------------------------------------------------------------------DOCTOR--------------------------------------'''

def doctor(request):        
    return render(request, 'usermanagement/doctor/doctor.html')

def doctorviewpl(request):
    if request.method == 'POST':
        name = ''
        if 'name' in request.POST:
            name = request.POST['name']
        patients = Patient.objects.filter(FirstName__contains=name,Service__iexact="General Medicine")
        patientList = []
        for p in patients:
            if not [p.FirstName,p.LastName,p.CNI_number] in patientList:
                patientList.append([p.FirstName,p.LastName,p.CNI_number])
        context = {
            'patientList':patientList,
            'patients': patients,
            'selectName':name,
        }
        return render(request, 'usermanagement/doctor/doctorviewpl.html', context)
    patients = Patient.objects.filter(Service__iexact="General Medicine")
    patientList = []
    for p in patients:
        if not [p.FirstName,p.LastName,p.CNI_number] in patientList:
            patientList.append([p.FirstName,p.LastName,p.CNI_number])
    context = {
        'patientList':patientList,
        'patients': patients,
    }
    return render(request, 'usermanagement/doctor/doctorviewpl.html', context)


class DoctorPatientUpdateView(UpdateView):
    model = Patient
    fields = '__all__'
    template_name = 'usermanagement/doctor/patient_doctor_update_form.html'
    success_url = reverse_lazy('usermanagement:doctorviewpl')


class DoctorPatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy('usermanagement:doctorviewpl')


def consultationlist(request):
    def contain(patientList,nom,prenom,cni):
        for n,p,c,l in patientList:
            if n==nom and p == prenom and c == cni:
                return False
        return True
    name = ''
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST['name']
    patientList = []
    patients = Patient.objects.filter(FirstName__contains = name)
    listId = []
    for p in patients:
        listId.append(p.id) 

    consultations = Consultation.objects.filter(idPatient__in=listId)
    listId = []
    for c in consultations:
        if not c.idPatient.id in listId:
            listId.append(c.idPatient.id)
    
    for p in patients:
        if contain(patientList,p.FirstName,p.LastName,p.CNI_number) and p.id in listId:
            tmpList = []
            for a in patients:
                if a.FirstName == p.FirstName and a.LastName ==  p.LastName and a.CNI_number ==  p.CNI_number:
                    tmpList.append(a.id)
            patientList.append([p.FirstName,p.LastName,p.CNI_number,tmpList])
    context = {
        'consultationlist': consultations,
        'patientList': patientList,
        'selectName':name,
    }
    return render(request, 'usermanagement/doctor/consultationlist.html',context=context)


def newconsultation(request):
    #traitement de la requete post
    if request.method == "POST":
        form1 =  ConsultationForm(request.POST).save()
        return consultationlist(request)
    else:   
        form1 = ConsultationForm()
    return render(request, 'usermanagement/doctor/newconsultation.html', {'form':form1})
    #objet formulaire sous forme d'un dictionnaire:{'form':form}

def newexamprescription(request):
    if request.method == "POST":
        form =  ExamForm(request.POST).save()
        form = ExamForm()    

        return render(request, 'usermanagement/doctor/newexamprescription.html', {'form':form})
    else:   
        form = ExamForm()    
    return render(request, 'usermanagement/doctor/newexamprescription.html', {'form':form})


def examlist(request):    
    def ndExam(idPatient):
        m = Examen.objects.filter(idPatient__exact=idPatient,status__exact='invalid')
        print(idPatient)
        return len(m)
    examens = Examen.objects.all()
    listePatient = []
    for m in examens:
        if not m.idPatient in listePatient:
            if ndExam(m.idPatient.id)>0:
                listePatient.append(m.idPatient)
    context = {
        'listePatient':listePatient,
        'examens':examens,
    }
    return render(request=request,template_name='usermanagement/doctor/examlist.html',context=context)

def medecinelist(request):
    def ndMed(idPatient):
        m = Medicament.objects.filter(idPatient__exact=idPatient,status__exact='invalid')
        print(idPatient)
        return len(m)
    medicaments = Medicament.objects.all()
    listePatient = []
    for m in medicaments:
        if not m.idPatient in listePatient:
            if ndMed(m.idPatient.id)>0:
                listePatient.append(m.idPatient)
    context = {
        'listePatient':listePatient,
        'medicaments':medicaments,
    }
    return render(request=request,template_name='usermanagement/doctor/medecinelist.html',context=context)




"""def prescriptionlist(request):  
    if request.method == 'POST':
        name = request.POST['name']
        examens = Examen.objects.filter(consultation_idPatient_FirstName__contains=name)
        medicaments = Medicament.objects.filter(consultation_idPatient_FirstName__contains=name)
        context = {
            'examens': examens,
            'medicaments': medicaments,
            'selectName':name,
        }
        return render(request, 'usermanagement/doctor/doctor.html',context=context)
    examens = Examen.objects.all()
    medicaments = Medicament.objects.all()
    context = {
            'examens': examens,
            'medicaments': medicaments,
    }
    return render(request, 'usermanagement/doctor/prescriptionlist.html', context)

    def prescriptionlist(request):
    def ndMed(idPatient):
        m = Medicament.objects.filter(idPatient__exact=idPatient,status__exact='invalid')
        print(idPatient)
        return len(m)
    medicaments = Medicament.objects.all()
    listePatient = []
    for m in medicaments:
        if not m.idPatient in listePatient:
            if ndMed(m.idPatient.id)>0:
                listePatient.append(m.idPatient)
    context = {
        'listePatient':listePatient,
        'medicaments':medicaments,
    }
    return render(request=request,template_name='usermanagement/doctor/consultationlist.html',context=context)

"""
def newmedicineprescription(request):
    if request.method == "POST":
        form =  MedicineForm(request.POST).save()
        form = MedicineForm()    
        return render(request, 'usermanagement/doctor/newmedicineprescription.html', {'form':form})
        
    else:   
        form = MedicineForm()    
    return render(request, 'usermanagement/doctor/newmedicineprescription.html', {'form':form})


#---------------------------------------PHARMACIST---------------------------------------------#
#---------------------------------------PHARMACIST---------------------------------------------#
#---------------------------------------PHARMACIST---------------------------------------------#


def pharmacist(request):        
    return render(request, 'usermanagement/pharmacist/pharmacist.html')

def facturemedicament(request,id):
    if request.method== 'POST':
        listeMed = Medicament.objects.filter(idPatient__exact=id)
        validMed = []
        for m in listeMed:
            if str(m.id) in request.POST:
                if request.POST[str(m.id)] == 'valid':
                    validMed.append(m)
                    m.status = 'valid'
                    m.save()
        nom = Patient.objects.filter(id__exact=id)[0]
        context = {'validMed':validMed,'nom':nom}
        return render(request, 'usermanagement/pharmacist/facturemedicament.html',context)
    return pharmacistviewpl(request)

def pharmacistviewpl(request):
    def ndMed(idPatient):
        m = Medicament.objects.filter(idPatient__exact=idPatient,status__exact='invalid')
        print(idPatient)
        return len(m)
    medicaments = Medicament.objects.all()
    listePatient = []
    for m in medicaments:
        if not m.idPatient in listePatient:
            if ndMed(m.idPatient.id)>0:
                listePatient.append(m.idPatient)
    context = {
        'listePatient':listePatient,
        'medicaments':medicaments,
    }
    return render(request=request,template_name='usermanagement/pharmacist/pharmacistviewpl.html',context=context)


    
#---------------------------------------LAB_TECHNICIAN---------------------------------------------#
#---------------------------------------LAB_TECHNICIAN---------------------------------------------#
#---------------------------------------LAB_TECHNICIAN---------------------------------------------#


def labtechviewpl(request):
    def ndExam(idPatient):
        m = Examen.objects.filter(idPatient__exact=idPatient,status__exact='invalid')
        print(idPatient)
        return len(m)
    examens = Examen.objects.all()
    listePatient = []
    for m in examens:
        if not m.idPatient in listePatient:
            if ndExam(m.idPatient.id)>0:
                listePatient.append(m.idPatient)
    context = {
        'listePatient':listePatient,
        'examens':examens,
    }
    return render(request=request,template_name='usermanagement/labTechnician/labtechviewpl.html',context=context)


def factureexamen(request,id):
    if request.method== 'POST':
        listeExamen = Examen.objects.filter(idPatient__exact=id)
        validExam = []
        for m in listeExamen:
            if str(m.id) in request.POST:
                if request.POST[str(m.id)] == 'valid':
                    validExam.append(m)
                    m.status = 'valid'
                    m.save()
        nom = Patient.objects.filter(id__exact=id)[0]
        context = {'validExam':validExam,'nom':nom}
        return render(request, 'usermanagement/labTechnician/factureexamen.html',context)
    return labtechviewpl(request)




