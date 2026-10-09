from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from hr.models import Leave, Attendance, Holiday

User = get_user_model()


def set_password(request, uidb64, token):


    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is None or not default_token_generator.check_token(user, token):
        return render(request, "invalid_link.html")


    if request.method == "POST":


        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(
                "set_password",
                uidb64=uidb64,
                token=token
            )


        user.set_password(password)
        user.save()


        messages.success(
            request,
            "Password created successfully. You can now login."
        )


        return redirect("login")


    return render(request, "set_password.html")


@login_required
def employee_dashboard(request):


   employee = request.user.employee


   return render(request,"employee_dashboard.html",{
           "employee": employee,"is_employee": True,})


@login_required
def employee_profile(request):


   employee = request.user.employee


   return render(request,"profile.html",{
           "employee": employee,"is_employee": True,})

@login_required
def apply_leave(request):

    employee = request.user.employee

    if request.method == "POST":

        leave_type = request.POST.get("leave_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        Leave.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )

        messages.success(
            request,
            "Leave application submitted successfully."
        )

        return redirect("my_leaves")

    return render(
        request,
        "apply_leave.html",
        {
            "leave_types": Leave.LEAVE_TYPES,
            "is_employee": True,
        }
    )

@login_required
def my_leaves(request):
    employee = request.user.employee

    leaves = Leave.objects.filter(
        employee=employee
    ).order_by("-applied_date")

    return render(
        request,
        "my_leaves.html",
        {
            "leaves": leaves,
            "is_employee": True,
        }
    )


@login_required
def employee_leave_calendar(request):

    employee = request.user.employee

    leaves = Leave.objects.filter(
        employee=employee,
        status="Approved"
    )

    attendance = Attendance.objects.filter(
        employee=employee
    )

    holidays = Holiday.objects.all()

    events = []

    # Leaves
    for leave in leaves:

        events.append({
            "title": f"{leave.get_leave_type_display()} - Leave",
            "start": leave.start_date.isoformat(),
            "end": leave.end_date.isoformat(),
            "color": "#0d6efd",
        })

    # Attendance
    for record in attendance:

        if record.status == "Present":

            events.append({
                "title": "Present",
                "start": record.date.isoformat(),
                "color": "#198754",
            })

        elif record.status == "Absent":

            events.append({
                "title": "Absent",
                "start": record.date.isoformat(),
                "color": "#dc3545",
            })

    # Holidays
    for holiday in holidays:

        events.append({
            "title": holiday.name,
            "start": holiday.date.isoformat(),
            "color": "#ffc107",
        })

    context = {
        "events": events,
        "is_employee": True,
    }

    return render(
        request,
        "employee_leave_calendar.html",
        context
    )