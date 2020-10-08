import csv
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import CsvRow, Build, Ride, Foil, Board, Motor, Controller, Propeller, Battery, Remote
from .forms import FoilForm, BoardForm, MotorForm, PropellerForm, ControllerForm, RideForm, BuildForm, BatteryForm, RemoteForm

ACCEPTED_DATA_SET = {
    "ms_today",
    "input_voltage",
    "temp_mos_max",
    "current_motor",
    "current_in",
    "erpm",
    "duty_cycle",
    "amp_hours_used",
    "watt_hours_used",
}

def index(request):
    if request.user.is_authenticated:
        return render(request, "plotter/authindex.html")
    return render(request, "plotter/index.html")

def handle_uploaded_file(f):
    with open("file.csv", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Not logged in
def parse_file(request, ride_id):
    template_data = {}
    with open("file.csv") as f:
        reader = csv.reader(f, delimiter=";")
        dataMap = {}
        rowMap = {}
        counter = 0
        header = []
        for index, head in enumerate(next(reader)):
            if head in ACCEPTED_DATA_SET:
                dataMap[index] = head
                header.append(head)
                rowMap[head] = counter
                counter += 1

        print(rowMap)

        # O(nRows*mdataMapkeys)
        data = []
        for row in reader:
            rowData = []
            for key in dataMap:
                if key == "temp_mos_max":
                    row[key] = row[key]*1.8 + 32
                rowData.append(row[key])
            newRow = CsvRow()
            for field in ACCEPTED_DATA_SET:
                if field in rowMap:
                    setattr(newRow, field, rowData[rowMap[field]])
                else:
                    setattr(newRow, field, None)
            ride = Ride.objects.filter(id=ride_id)
            newRow.ride = ride[0]
            newRow.save()
            data.append(rowData)

        template_data = {
            "header": header,
            "data": data
        }
        send_data = json.dumps(template_data)
        return send_data

@login_required(login_url='/login/')
def upload(request):
    rideForm = RideForm()
    if request.user.is_authenticated:
        user_id = request.user.id
        rideForm.fields["build"].queryset = Build.objects.filter(author=user_id)
        if request.method == 'POST':
            rideForm = RideForm(request.POST)
            if rideForm.is_valid():
                rideInfo = rideForm.save(commit=False)
                rideInfo.rider = request.user
                rideInfo.save()
                handle_uploaded_file(request.FILES["file"])
                parse_file(request, rideInfo.id)
                urlPath = "/graph/" + str(rideInfo.id) + "/"
                return redirect(urlPath)

    return render(request, "plotter/upload.html", context={'accepted_data_set':ACCEPTED_DATA_SET, 'rideForm': rideForm })

def graph(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    header_display = [
        "ms_today",
        "Voltage",
        "Temperature",
        "Motor Current",
        "Battery Current",
        "RPM",
        "Throttle",
        "AMP Hours",
        "Watt Hours",
    ]

    template_data = {}
    data = []
    csvData = CsvRow.objects.filter(ride=ride_id)

    for row in csvData:
        rowData = row.getAllFields()
        data.append(rowData)

    template_data = {
        "header": header_display,
        "data": data
    }

    send_data = json.dumps(template_data)

    return render(request, "plotter/graph2.html", context={"mydata": send_data, "ride":ride})

def profile(request, username):
    current_user = get_object_or_404(User, username=username)
    builds = Build.objects.filter(author=current_user)
    rides = Ride.objects.filter(rider=current_user)
    return render(request, "plotter/profile.html", context={"username": username, "builds":builds, "rides":rides})

@login_required(login_url='/login/')
def add_build(request):
    buildForm = BuildForm(prefix='build')
    boardForm = BoardForm(prefix='board')
    foilForm = FoilForm(prefix='foil')
    motorForm = MotorForm(prefix='motor')
    propellerForm = PropellerForm(prefix='propeller')
    controllerForm = ControllerForm(prefix='controller')
    batteryForm = BatteryForm(prefix='battery')
    remoteForm = RemoteForm(prefix='remote')

    if request.user.is_authenticated:
        if request.method == 'POST':
            buildForm = BuildForm(request.POST, prefix='build')
            boardForm = BoardForm(request.POST, prefix='board')
            foilForm = FoilForm(request.POST, prefix='foil')
            motorForm = MotorForm(request.POST, prefix='motor')
            propellerForm = PropellerForm(request.POST, prefix='propeller')
            controllerForm = ControllerForm(request.POST, prefix='controller')
            batteryForm = BatteryForm(request.POST, prefix='battery')
            remoteForm = RemoteForm(request.POST, prefix='remote')
            if buildForm.is_valid() and boardForm.is_valid() and foilForm.is_valid() and motorForm.is_valid() and propellerForm.is_valid() and controllerForm.is_valid() and batteryForm.is_valid() and remoteForm.is_valid():
                #get form object but dont save
                build = buildForm.save(commit=False)
                board = boardForm.save()
                foil = foilForm.save()
                motor = motorForm.save()
                prop = propellerForm.save()
                controller = controllerForm.save()
                battery = batteryForm.save()
                remote = remoteForm.save()
                # setting foreign keys
                build.author = request.user
                build.board = board
                build.foil = foil
                build.motor = motor
                build.propeller = prop
                build.controller = controller
                build.battery = battery
                build.remote = remote
                build.save()
                title = buildForm.cleaned_data.get('title')
                messages.success(request, 'Build "' + title + '" was created')
                return redirect('/build')
    context={'boardForm':boardForm, 'foilForm':foilForm, 'motorForm':motorForm, 'propellerForm':propellerForm, 'controllerForm':controllerForm, 'buildForm':buildForm, 'batteryForm':batteryForm, 'remoteForm':remoteForm}
    return render(request, "plotter/add_build.html", context)

@login_required(login_url='/login/')
def edit_build(request, build_id):

    build = get_object_or_404(Build, id=build_id)

    if build.author != request.user:
        redirect('/profile' + build.author.username/ + '/')

    buildForm = BuildForm(instance=build)
    boardForm = BoardForm(instance=build.board, prefix='board')
    foilForm = FoilForm(instance=build.foil, prefix='foil')
    motorForm = MotorForm(instance=build.motor, prefix='motor')
    propellerForm = PropellerForm(instance=build.propeller, prefix='propeller')
    controllerForm = ControllerForm(instance=build.controller, prefix='controller')
    batteryForm = BatteryForm(instance=build.battery, prefix='battery')
    remoteForm = RemoteForm(instance=build.remote, prefix='remote')


    if request.method == 'POST':
        buildForm = BuildForm(request.POST, instance=build)
        boardForm = BoardForm(request.POST,instance=build.board, prefix='board')
        foilForm = FoilForm(request.POST,instance=build.foil, prefix='foil')
        motorForm = MotorForm(request.POST,instance=build.motor, prefix='motor')
        propellerForm = PropellerForm(request.POST, instance=build.propeller, prefix='propeller')
        controllerForm = ControllerForm(request.POST,instance=build.controller, prefix='controller')
        batteryForm = BatteryForm(request.POST, instance=build.battery, prefix='battery')

        if buildForm.is_valid() and boardForm.is_valid() and foilForm.is_valid() and motorForm.is_valid() and propellerForm.is_valid() and controllerForm.is_valid() and batteryForm.is_valid() and remoteForm.is_valid():
            #get form object but dont save and remoteForm.is_valid()
            build = buildForm.save(commit=False)
            board = boardForm.save()
            foil = foilForm.save()
            motor = motorForm.save()
            prop = propellerForm.save()
            controller = controllerForm.save()
            battery = batteryForm.save()
            remote = remoteForm.save()
            # setting foreign keys
            build.author = request.user
            build.board = board
            build.foil = foil
            build.motor = motor
            build.propeller = prop
            build.controller = controller
            build.battery = battery
            build.remote = remote
            build.save()
            title = buildForm.cleaned_data.get('title')
            messages.success(request, 'Build "' + title + '" was updated')
            return redirect('/build')

    context={'boardForm':boardForm, 'foilForm':foilForm, 'motorForm':motorForm, 'propellerForm':propellerForm, 'controllerForm':controllerForm, 'buildForm':buildForm, 'batteryForm':batteryForm, 'remoteForm':remoteForm}
    return render(request, "plotter/add_build.html", context)

@login_required(login_url='/login/')
def delete_build(request, build_id):
    build = get_object_or_404(Build, id=build_id)

    if build.author != request.user:
        redirect('/profile' + build.author.username/ + '/')

    if request.method == 'POST':
        build.delete()
        redirect('/profile' + request.user.username/ + '/')

    context={"build":build}
    return render(request, "plotter/delete.html", context)

def users(request):
    users = User.objects.all()
    return render(request, "plotter/users.html", context={"users":users})
