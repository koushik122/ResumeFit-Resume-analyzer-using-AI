from django.shortcuts import render, redirect
from .forms import DataForm

# Create your views here.
def index(request):
    form = None
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result')
        else:
            form=DataForm()
            return render(request, 'index.html', {'form':form})
    
    form=DataForm()
    return render(request, 'index.html', {'form':form})


def result(request):
    return render(request, 'result.html')