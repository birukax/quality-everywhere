from django.shortcuts import render, get_object_or_404, redirect
from first_off.models import FirstOff
from .models import FirstOffApproval


# def approvals(request):
#     return render(request, 'approval/list.html', context)

def create_first_off_approval(request,id):
    first_off = get_object_or_404(FirstOff, id=id)
    if not first_off.status == 'PENDING':
        approvers = ['OPERATOR', 'SUPERVISOR']
        for a in approvers:
            app = FirstOffApproval(first_off=first_off, approver=a)
            app.save()
        first_off.status = 'PENDING'
        first_off.inspected_by = request.user
        first_off.save()
    return redirect('first_off:detail', id=id)

def first_offs(request):
    
    first_offs = FirstOffApproval.objects.filter(approved=False)
    context = {'first_offs': first_offs}
    return render(request, 'approval/first_off/list.html', context)