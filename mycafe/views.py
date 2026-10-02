from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import DetailView
from .models import MenuItem, Category
from .forms import MenuItemForm

# Create your views here.


# 1. Home Page View (FBV)
def home(request):
    total_items = MenuItem.objects.count()
    return render(request, 'cafe/home.html', {'total_items': total_items})

# 2. READ (List) View with Query Parameter Search (FBV)
def menu_list(request):
    query = request.GET.get('q', '') # Query parameter handling
    if query:
        items = MenuItem.objects.filter(name__icontains=query)
    else:
        items = MenuItem.objects.all()
    return render(request, 'cafe/menu.html', {'items': items, 'query': query})

# 3. READ (Detail) View (Class-Based View)
class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'cafe/menuitem_detail.html'
    context_object_name = 'item'

# 4. CREATE View (FBV)
def item_create(request):
    form = MenuItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('cafe:menu_list')
    return render(request, 'cafe/menuitem_form.html', {'form': form, 'title': 'Add New Item'})

# 5. UPDATE View (FBV)
def item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('cafe:menu_list')
    return render(request, 'cafe/menuitem_form.html', {'form': form, 'title': 'Edit Item'})

# 6. DELETE View (FBV)
def item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('cafe:menu_list')
    return render(request, 'cafe/menuitem_confirm_delete.html', {'item': item})

