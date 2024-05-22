import json

import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import CreateUserForm, UserResponse, DoctorInfo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserResponseForm
from json import dumps
from django.http import JsonResponse
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from .process import *
import random


def home_page(request):
    return render(request, 'home.html')


@login_required(login_url="/login")
def test_page(request):
    if UserResponse.objects.filter(user=request.user).exists():
        latest_response = UserResponse.objects.filter(user=request.user).values().latest("date_time")

        vals = [latest_response[i] for i in latest_response]
        stage_num = vals[2]
        vals = vals[3:8]
        counts = dict(Counter(vals))
        num_yes_no = {key: value for key, value in counts.items() if value > 1}
        num_yes_no = vals.count("Yes")
        print(num_yes_no)
        if num_yes_no > 2:
            messages.success(request, 'You can give Second Test!')
        return render(request, 'test_page.html')
    else:
        return render(request, 'test_page.html')


def signup_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            form.save()
            messages.success(request, 'Account Created!!!')
            return redirect('/login')

    context = {'form': form}

    return render(request, 'Accounts/sign_up.html', context)


def login_page(response):
    if response.method == 'POST':
        username = response.POST.get('username')
        password = response.POST.get('password')
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            return redirect('initial_test')

        else:
            messages.error(response, 'Username/Password Incorrect')

    return render(response, 'Accounts/login.html')


@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def record_response(request):
    form = UserResponseForm()

    if request.method == 'POST':
        form = UserResponseForm(request.POST)
        first_ques = request.POST.get("first_ques")
        second_ques = request.POST.get("second_ques")
        third_ques = request.POST.get("third_ques")
        fourth_ques = request.POST.get("fourth_ques")
        fifth_ques = request.POST.get("fifth_ques")
        request.user.userresponse_set.create(stage_number=1, first_ques=first_ques, second_ques=second_ques,
                                             third_ques=third_ques, fourth_ques=fourth_ques, fifth_ques=fifth_ques)

        user_response = UserResponse.objects.filter(user=request.user).latest("date_time")

        return render(request, 'test_view.html', {'data': user_response, 'form': form})

    else:
        return render(request, 'test.html', {"form": form})


def analyze_user_response(response, id):
    global df
    test_data = UserResponse.objects.values().get(pk=id)
    test_data_json = dumps(test_data, default=str)
    vals = [test_data[i] for i in test_data]
    stage_num = vals[2]
    vals = vals[3:8]
    if stage_num == 1:
        print("Stage-1")
        df = pd.read_csv('Datasets/Stage-1.csv')
    elif stage_num == 2:
        print("Stage-2")
        df = pd.read_csv('Datasets/Stage-2.csv')
    elif stage_num == 3:
        print("Stage-3")
        df = pd.read_csv('Datasets/Stage-3.csv')

    proc_df = df.loc[:, df.columns != 'Answers']
    proc_df.loc[len(proc_df)] = vals
    dup_df = proc_df[proc_df.duplicated(keep=False)]
    result = df.iloc[dup_df.index[0]]['Answers']
    doctor = DoctorInfo.objects.all()
    total_doctors = doctor.count()
    if total_doctors > 0:
        # Get a random index within the range of total doctors
        random_index = random.randint(0, total_doctors - 1)
        
        # Get the random doctor using the random index
        random_doctor = doctor[random_index]
    return render(response, 'analyze_test.html', {'result': result, 'doctor_info' : random_doctor})


@login_required(login_url='/login')
def stage2_test_response(request):
    form = UserResponseForm()

    if request.method == 'POST':
        form = UserResponseForm(request.POST)
        first_ques = request.POST.get("first_ques")
        second_ques = request.POST.get("second_ques")
        third_ques = request.POST.get("third_ques")
        fourth_ques = request.POST.get("fourth_ques")
        fifth_ques = request.POST.get("fifth_ques")
        request.user.userresponse_set.create(stage_number=2, first_ques=first_ques, second_ques=second_ques,
                                             third_ques=third_ques, fourth_ques=fourth_ques, fifth_ques=fifth_ques)

        user_response = UserResponse.objects.filter(user=request.user).latest("date_time")

        return render(request, 'test_view.html', {'data': user_response, 'form': form})

    else:
        return render(request, 'Stage-2_test.html', {"form": form})


@login_required(login_url='/login')
def stage3_test_response(request):
    form = UserResponseForm()

    if request.method == 'POST':
        form = UserResponseForm(request.POST)
        first_ques = request.POST.get("first_ques")
        second_ques = request.POST.get("second_ques")
        third_ques = request.POST.get("third_ques")
        fourth_ques = request.POST.get("fourth_ques")
        fifth_ques = request.POST.get("fifth_ques")
        request.user.userresponse_set.create(stage_number=3, first_ques=first_ques, second_ques=second_ques,
                                             third_ques=third_ques, fourth_ques=fourth_ques, fifth_ques=fifth_ques)

        user_response = UserResponse.objects.filter(user=request.user).latest("date_time")
        return render(request, 'test_view.html', {'data': user_response, 'form': form})
    else:
        return render(request, 'Stage-3_test.html', {"form": form})


@login_required(login_url="/login")
def analyze_user_report(request):
    user_data = UserResponse.objects.filter(user=request.user).values("date_time", "first_ques",
                                                                      "third_ques", 'second_ques', 'fourth_ques',
                                                                      'fifth_ques').order_by("-id")[:10][::1]

    return render(request, 'Analyze/analyze_user.html', {'user_data': user_data})


def get_user_json(request):
    user_data = UserResponse.objects.filter(user=request.user).values("date_time", "first_ques",
                                                                      "third_ques", 'second_ques', 'fourth_ques',
                                                                      'fifth_ques').order_by("-id")[:10][::1]

    user_data = list(user_data)
    user_data_json = json.dumps(user_data, default=str)

    return JsonResponse(user_data_json, safe=False)

@login_required(login_url="/login")
def initial_test(request):
    context = {
        'username' : request.user.username
    }
    if request.method == "POST":
        label_Age =  int(request.POST["label_Age"])
        label_Gender =  int(request.POST["label_Gender"])
        label_self_employed =  int(request.POST["label_self_employed"])
        label_family_history =  int(request.POST["label_family_history"])
        label_treatment =  int(request.POST["label_treatment"])
        label_work_interfere =  int(request.POST["label_work_interfere"])
        label_no_employees =  int(request.POST["label_no_employees"])
        label_remote_work =  int(request.POST["label_remote_work"])
        label_tech_company =  int(request.POST["label_tech_company"])
        label_benefits =  int(request.POST["label_benefits"])
        label_care_options =  int(request.POST["label_care_options"])
        label_wellness_program =  int(request.POST["label_wellness_program"])
        label_seek_help =  int(request.POST["label_seek_help"])
        label_anonymity =  int(request.POST["label_anonymity"])
        label_leave =  int(request.POST["label_leave"])
        label_mental_health_consequence =  int(request.POST["label_mental_health_consequence"])
        label_phys_health_consequence =  int(request.POST["label_phys_health_consequence"])
        label_coworkers =  int(request.POST["label_coworkers"])
        label_supervisor =  int(request.POST["label_supervisor"])
        label_mental_health_interview =  int(request.POST["label_mental_health_interview"])
        label_phys_health_interview =  int(request.POST["label_phys_health_interview"])
        label_mental_vs_physical =  int(request.POST["label_mental_vs_physical"])
        label_obs_consequence =  int(request.POST["label_obs_consequence"])
        label_comments =  request.POST["label_comments"]

        scaler = MinMaxScaler()
        age = [[label_Age]]
        scaled_age = scaler.fit_transform(age)
        scaled_age = float(scaled_age[0][0])
        predict_health = health_Prediction(scaled_age, label_Gender, label_family_history, label_benefits, label_care_options, label_anonymity, label_leave, label_work_interfere)
        if predict_health == 0:
            messages.success(request, "You are Completely Stable!!!")
            return redirect("initial_test")
        elif predict_health == 1:
            level = random.randint(1,3)
            if level == 1:
                messages.info(request, "You are at First Level!!")
                return redirect("test_page")
            elif level == 2:
                messages.info(request, "You are at Second Level!!")
                return redirect("stage2Test")
            else:
                messages.info(request, "You are at Third Level!!")
                return redirect("stage3Test")

    return render(request, "initial_test.html", context)