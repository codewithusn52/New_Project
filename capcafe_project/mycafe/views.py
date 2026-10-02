from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import DetailView
from .models import MenuItem, Category,Order, OrderItem
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
        return redirect('mycafe:menu_list')
    return render(request, 'cafe/menuitem_form.html', {'form': form, 'title': 'Add New Item'})

# 5. UPDATE View (FBV)
def item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('mycafe:menu_list')
    return render(request, 'cafe/menuitem_form.html', {'form': form, 'title': 'Edit Item'})

# 6. DELETE View (FBV)
def item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('mycafe:menu_list')
    return render(request, 'cafe/menuitem_confirm_delete.html', {'item': item})

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    
    # Cart quantity update
    cart[item_id_str] = cart.get(item_id_str, 0) + 1
    request.session['cart'] = cart
    return redirect('mycafe:menu_list')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        subtotal = item.price * quantity
        total_price += subtotal
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def place_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        table_number = request.POST.get('table_number')
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('mycafe:menu_list')

        # Create Order Record
        order = Order.objects.create(
            customer_name=customer_name,
            table_number=table_number if table_number else None
        )

        # Create Order Items
        for item_id, quantity in cart.items():
            menu_item = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )

        # Clear session cart after placing order
        request.session['cart'] = {}
        return redirect('mycafe:order_success')

    return redirect('mycafe:view_cart')

def order_success(request):
    return render(request, 'order_success.html')

