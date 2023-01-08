from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from home.models import Poll
from django.template import loader
from datetime import datetime
from django.contrib import messages
# Create your views here.


def index(request):

    if  request.user.is_anonymous:
        return redirect("/login")
    else:
        
        polls=Poll.objects.all().exclude(created_by=request.user) #filtering polls not created by logged in user
        template = loader.get_template('index.html')
        context={
            'polls':polls
        }
        return HttpResponse(template.render(context, request))

def userPolls(request):

    polls=Poll.objects.all().filter(created_by=request.user)  #filtering polls created by logged in user
    template = loader.get_template('userPolls.html')
    context={
        'polls':polls
    }
    return HttpResponse(template.render(context, request))



def create(request):
    question=request.POST.get("question")
    option_one=request.POST.get("option_one")
    option_two=request.POST.get("option_two")
    option_three=request.POST.get("option_three")
    deadline=request.POST.get("deadline")

    if request.method=="POST":
        poll=Poll(question=question,option_one=option_one,option_two=option_two,option_three=option_three,deadline=deadline,created_by=request.user)
        poll.save()

        return redirect("/")

    return render(request,'create.html')

def vote(request,poll_id):

    poll=Poll.objects.get(id=poll_id)

    current_date = datetime.now().date()  
   

    
    if current_date>poll.deadline:
        messages.warning(request, 'This poll has already ended!')
        return redirect('/')

    if request.method=="POST":
        option_one_check=request.POST.get("option_one_check")
        option_two_check=request.POST.get("option_two_check")
        option_three_check=request.POST.get("option_three_check")

        

        if option_one_check=="on":
            poll.option_one_count+=1

        elif option_two_check=="on":
            poll.option_two_count+=1
        
        else:
            poll.option_three_count+=1
        
        poll.save()
        return redirect("/result/"+poll_id)


    template = loader.get_template('vote.html')
    context={
            'poll':poll
    }
    return HttpResponse(template.render(context, request))

def result(request,poll_id):
    poll=Poll.objects.get(id=poll_id)

    total_poll_count=poll.option_one_count+poll.option_two_count+poll.option_three_count
    if total_poll_count==0:
        option_one_percent=0
        option_two_percent=0
        option_three_percent=0

    else:
        option_one_percent=poll.option_one_count/total_poll_count*100
        option_two_percent=poll.option_two_count/total_poll_count*100
        option_three_percent=poll.option_three_count/total_poll_count*100

    template = loader.get_template('result.html')
    context={
            'poll':poll,
            'option_one_percent':option_one_percent,
            'option_two_percent':option_two_percent,
            'option_three_percent':option_three_percent,
            'total_poll_count':total_poll_count
    }
    return HttpResponse(template.render(context, request))

def createUser(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    if request.method=="POST":
        user = User.objects.create_user(username=username ,email=email,password=password)
        return redirect("/")

    return render(request,'register.html')
    

def loginUser(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    if request.method=="POST":
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # request.session["user"]=user  #making the logged in user available to all the functions in views.py
            return redirect("/")
        else:
            return render(request,'login.html')
    
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')


def deletePoll(request,poll_id):
    poll = Poll.objects.get(id=poll_id)
    poll.delete()
    return redirect("/user_polls")


   
    
