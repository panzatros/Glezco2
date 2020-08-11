from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View, DetailView, FormView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.core.files.storage import FileSystemStorage



from .models import productos, DireccionEntrega, OrderItem, Order
from .forms import addToCart, CheckoutForm, ProductEditForm

class home(ListView):
    model = productos
    paginate_by = 9
    template_name='core/index.html'

class products(View):
    template_name='core/productos.html'
    def get(self, request):
        return render(request, self.template_name)

class detalles(DetailView):
    model = productos
    template_name = "core/product.html"

    def get_context_data(self, **kwargs):
        context = super(detalles, self).get_context_data(**kwargs)
        context['form'] = addToCart
        return context

def addToCartForm(request,slug):
    hola = get_object_or_404(productos,slug=slug)
    try:
        item = OrderItem.objects.get(user=request.user, ordered=False, item=hola)
        #item.quantity += int(request.POST['Cantidad'])
        #item.save()
    except:
        item = OrderItem.objects.create(user=request.user,ordered=False,item=hola,quantity=request.POST['Cantidad'])
        item.save()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=hola.slug).exists():
            item.quantity += int(request.POST['Cantidad'])
            item.save()
            #messages.info(request, "This item quantity was updated.")
            return redirect("/")
        else:
            order.items.add(item)
            #messages.info(request, "This item was added to your cart.")
            return redirect("/")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(item)
        #messages.info(request, "This item was added to your cart.")
        return redirect("/")
    #return redirect("/")

def remove_from_cart(request, slug):
    item = get_object_or_404(productos, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            #messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            #messages.info(request, "This item was not in your cart")
            return redirect("producto", slug=slug)
    else:
        #messages.info(request, "You do not have an active order")
        return redirect("producto", slug=slug)

def remove_one_from_cart(request, slug):
    item = get_object_or_404(productos, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists:
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove()
                order_item.delete()
            return redirect("order-summary")
        else:
            return redirect("producto", slug=slug)
    else:
        return redirect("producto", slug=slug)

def add_one_from_cart(request, slug):
    item = get_object_or_404(productos, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists:
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity += 1
            order_item.save()
            return redirect("order-summary")
        else:
            return redirect("producto", slug=slug)
    else:
        return redirect("producto", slug=slug)

class checkout(View):
    template_name='core/checkout.html'
    def get(self, request):
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            cosa = ''
            if order.shipping_address.all():
                cosa = 'seleccionado'
            else:
                cosa = 'no seleccionado'
            context = {
                'cosa':cosa, 'object': order
            }
            return render(request, self.template_name, context)
        else:
            return redirect("/")
    def post(self, request):
        pass

class selectAddres(ListView):
    model = DireccionEntrega
    paginate_by = 10
    template_name='core/adress.html'
    def get_context_data(self, **kwargs):
        context = super(selectAddres, self).get_context_data(**kwargs)
        context['form'] = CheckoutForm
        return context

def addAddres(request):
    url = slugify(request.POST['calle'] + '-' + request.POST['colonia'] + '-' + str(request.POST['numeroExterior']))
    numero_interior = None
    if request.POST['numeroInterior'] is None:
        numero_interior = None
    else:
        numero_interior = int(request.POST['numeroInterior'])
    item = DireccionEntrega.objects.create(
        usuario=request.user,
        calle=request.POST['calle'],
        numeroExterior=int(request.POST['numeroExterior']),
        numeroInterior=numero_interior,
        colonia=request.POST['colonia'],
        codigoPostal=int(request.POST['numeroInterior']),
        slug = url
        )
    item.save()
    return redirect("slect-addres")

def deleteAddres(request,slug):
    item = get_object_or_404(DireccionEntrega, slug=slug)
    item.delete()
    return redirect("slect-addres")

def selectDireccion(request,slug):
    item = get_object_or_404(DireccionEntrega, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    domicilioPrevio = order.shipping_address.all()
    if order.shipping_address is None:
        order.shipping_address.add(item)
    else:
        try:
            order.shipping_address.remove(domicilioPrevio[0])
            order.shipping_address.add(item)
        except:
            order.shipping_address.add(item)
        #order.shipping_address.remove(domicilioPrevio[0])
    return redirect("checkout")


class detalleAddres(View):
    def get(self,request,slug):
        item = get_object_or_404(DireccionEntrega, slug=slug)
        context = {'object':item}
        return render(request, "core/detalleDireccion.html", context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'core/order_summary.html', context)
        except :
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


def confirmar_Pedido(request):
    order = Order.objects.get(user=request.user, ordered=False)
    try:
        if order.shipping_address.all():
            order.ordered = True
            order.ordered_date_pedido = timezone.now()
            order.save()
            return redirect ("gracias-pedido")
        else:
            return redirect("slect-addres")
    except:
        return redirect("slect-addres")

def gracias_por_pedido(request):
    return render(request, "core/Thanks.html")

#@login_required
class panel(ListView):
    model = productos
    paginate_by = 9
    template_name='core/panel.html'
    
    def get_context_data(self, **kwargs):
        context = super(panel, self).get_context_data(**kwargs)
        context['form'] = ProductEditForm
        return context

@login_required
def addPrduct(request):
    if request.method == 'POST':
        url23 = slugify(request.POST['titulo'])
        valor = False
        if request.POST['disponible'] == "on":
            valor = True
        form = ProductEditForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            instance = productos(titulo=request.POST['titulo'], descripcion=request.POST['descripcion'] ,image=request.FILES['image'],slug=url23,disponible=valor)
            instance.save()
            return redirect('panel')
    """
    if request.POST['disponible'] == "on":
        valor = True
    item = productos.objects.create(
        titulo=request.POST['titulo'],
        descripcion=request.POST['descripcion'],
        image="media/core/images/"+request.POST['image'],
        slug=url23,
        disponible=valor,
    )
    item.save()
    print(request.FILES.get("image"))              #<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    #print(request.FILES["file"])  
    #handle_uploaded_file(request.FILES['image'].read())
    return redirect('panel')
    """

#@login_required
class PanelDetalles(UpdateView):
    model = productos
    template_name = "core/panelProduct.html"
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        context = super(PanelDetalles, self).get_context_data(**kwargs)
        object = self.get_object()
        context['productos'] = context['object'] = object
        return context

@login_required
def change_prodcuts(request, slug):
    hola = get_object_or_404(productos,slug=slug)
    url23 = slugify(request.POST['titulo'])
    valor = False
    if request.POST['disponible'] == "on":
        valor = True
    form = ProductEditForm(instance=hola)
    if form.is_valid():
        # file is saved
        instance = productos(titulo=request.POST['titulo'], descripcion=request.POST['descripcion'] ,image=request.FILES['image'],slug=url23,disponible=valor)
        instance.save()
        return redirect('panel')

@login_required
def ver_ordenes(request):
    todos = Order.objects.filter(ordered=True, cancelled=False, being_delivered=False, received=False).order_by('-ordered_date_pedido')
    return render(request, 'core/OrdenAbierta.html', {'object_list':todos})

@login_required
def ver_ordenes_canceladas(request):
    todos = Order.objects.filter(cancelled=True).order_by('-ordered_date_pedido')
    return render(request, 'core/OrdenCancelada.html', {'object_list':todos})

@login_required
def ver_ordenes_Enviadas(request):
    todos = Order.objects.filter(being_delivered=True, received=False).order_by('-ordered_date_pedido')
    return render(request, 'core/OrdenEnviada.html', {'object_list':todos})

@login_required
def ver_ordenes_Cerradas(request):
    todos = Order.objects.filter(received=True).order_by('-ordered_date_pedido')
    return render(request, 'core/OrdenCerrada.html', {'object_list':todos})

@login_required
def observarla_orden(request, la_pk):
    todo = get_object_or_404(Order, pk=la_pk)
    if request.method == 'GET':
        return render(request, 'core/OrdenDetalle.html', {'detalle':todo})

def Cancelar_orden(request, la_pk):
    todo = get_object_or_404(Order, pk=la_pk)
    if request.method == 'POST':
        todo.cancelled = True
        todo.save()

def Enviada_orden(request, la_pk):
    todo = get_object_or_404(Order, pk=la_pk)
    if request.method == 'POST':
        todo.being_delivered = True
        todo.save()

def Recivida_orden(request, la_pk):
    todo = get_object_or_404(Order, pk=la_pk)
    if request.method == 'POST':
        todo.received = True
        todo.save()

def Cancelar_orden_cliente(request, la_pk):
    todo = get_object_or_404(Order, pk=la_pk, user=request.user)
    if request.method == 'POST':
        todo.cancelled = True
        todo.save()


@login_required
def ver_ordenes(request):
    todos = Order.objects.filter(ordered=True, cancelled=False, being_delivered=False, received=False).order_by('-ordered_date_pedido')
    return render(request, 'core/OrdenAbierta.html', {'object_list':todos})