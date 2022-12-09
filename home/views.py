from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from home.models import Poll
from django.template import loader
# Create your views here.
def index(request):

    if  request.user.is_anonymous:
        return redirect("/login")
    else:
        polls=Poll.objects.all().values()
        template = loader.get_template('index.html')
        context={
            'polls':polls
        }
        return HttpResponse(template.render(context, request))

def create(request):
    question=request.POST.get("question")
    option_one=request.POST.get("option_one")
    option_two=request.POST.get("option_two")
    option_three=request.POST.get("option_three")

    if request.method=="POST":
        poll=Poll(question=question,option_one=option_one,option_two=option_two,option_three=option_three)
        poll.save()

        return redirect("/")

    return render(request,'create.html')

def vote(request,poll_id):

    poll=Poll.objects.get(id=poll_id)

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
        return redirect("/")


    template = loader.get_template('vote.html')
    context={
            'poll':poll
    }
    return HttpResponse(template.render(context, request))

def result(request,poll_id):
    poll=Poll.objects.get(id=poll_id)

    total_poll_count=poll.option_one_count+poll.option_two_count+poll.option_three_count
    option_one_percent=poll.option_one_count/total_poll_count*100
    option_two_percent=poll.option_two_count/total_poll_count*100
    option_three_percent=poll.option_three_count/total_poll_count*100

    template = loader.get_template('result.html')
    context={
            'question':poll.question,
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
            return redirect("/")
        else:
            return render(request,'login.html')
    
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')

   
    
