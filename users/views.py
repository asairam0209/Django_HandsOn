from django.shortcuts import render, redirect
from .forms import CustomRedgForm
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomRedgForm(request.POST)
        if form.is_valid(): 
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, Your Accoount is created.')
            return redirect('login')
    else:
    
        form = CustomRedgForm()
    return render(request, 'users/register.html', {'form': form})
