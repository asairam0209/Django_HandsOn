from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm
# Create your views here.
def index(request):
    items = Item.objects.all()
    return render(request, 'FoodApp/index.html',{'items' : items})

def details(request, pk):
    item = Item.objects.get(pk = pk)
    return render(request, 'FoodApp/details.html',{'item' : item})

def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Foodapp:index')  # Redirect to index page after saving
        else:
            print("Form errors:", form.errors)  # Debugging

    else:
        form = ItemForm()

    return render(request, 'FoodApp/item-form.html', {'form': form})

def update_item(request,pk):
    item = Item.objects.get(pk = pk)
    form = ItemForm(request.POST or None, instance=item)
    
    if form.is_valid():
        form.save()
        return redirect('Foodapp:index')
    
    return render(request, 'FoodApp/item-form.html', {'form': form, 'item': item})

def delete_item(request,pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('Foodapp:index')
    
    return render(request, 'FoodApp/confirm.html', {'item': item})


