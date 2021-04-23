from django.shortcuts import render, redirect
from .models import User, Job
import bcrypt
from django.contrib import messages

def index(request):

    return render(request, "belt/index.html")

def create(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    
    else:
        first = request.POST['fname']
        last = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pcode']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash) 

        newuser = User.objects.create(first_name = first, last_name = last, email = email, password = pw_hash)
        request.session['key'] = newuser.email        
        email = User.objects.get(email = request.POST['email'])
        request.session['fname'] = newuser.first_name
        request.session['id'] = newuser.id
        request.session['lname'] = newuser.last_name

        return redirect('/success')

def login(request):

    if request.method == "GET":
        return redirect('/')
    else:

            
        errors = User.objects.login_validator(request.POST)


        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            return redirect('/')

        else:
            email = User.objects.get(email = request.POST['email'])
            request.session['key'] = email.email
            request.session['fname'] = email.first_name
            request.session['id'] = email.id
            request.session['lname'] = email.last_name 
            return redirect("/success")


def success(request):

    context ={
        'oneuser' : request.session['key'],
        'firstname': request.session['fname'],
        'lastname': request.session['lname'],
        'id': request.session['id'],
        'all_jobs': Job.objects.all()
    }

    return render(request, "belt/list.html", context)

def newjob(request):

    return render(request, "belt/new.html")

def createprocess(request):

    errors = Job.objects.job_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors

        return redirect ('/jobs/new')
    else:
        jobtitle = request.POST['title']
        desc = request.POST['description']
        loc = request.POST['location']
        user_id = request.session['id']

        get_user = User.objects.get(id = user_id)
        
        newjob = Job.objects.create(job = jobtitle, description = desc, location = loc, user = get_user)

        return redirect('/success')

def editjob(request, my_id):

    context = {
        'one_job' : Job.objects.get(id = int(my_id)) 
    }
    print('editprocess')

    return render(request ,'belt/edit.html', context)

def editprocess(request, my_id):

    errors = Job.objects.job_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors

        return redirect ('/jobs/edit/' + str(my_id))
    else:    

        editJob = Job.objects.get(id = int(my_id))
        editJob.job = request.POST['title']
        editJob.description = request.POST['description']
        editJob.location = request.POST['location']
        editJob.save()

        return redirect('/success')

def viewprocess(request, my_id):
    userID = request.POST['userId']
    print(userID)
    context ={
        'one_job' : Job.objects.get(id = int(my_id)),
        'one_person': User.objects.get(id = int(userID))
    }

    return render (request, 'belt/view.html', context)

def back(request):

    return redirect('/success')

def remove(request, my_id):

    deletejob = Job.objects.get(id = int(my_id))
    deletejob.delete()

    return redirect('/success')



def logout(request):
    if 'key' in request.session:

        del request.session['key'] 

    return redirect('/')