from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from core import views
from django.views.decorators.http import require_http_methods
from django.conf.urls.static import static
from django.conf import settings


app_name = 'core'

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    #url(r'^accounts/', include('allauth.urls')),
    #administracion gnral
    path('admin/', admin.site.urls),
    #home
    path('', views.home.as_view(), name='home'),
    #log in
    #path('login/', views.loginuser.as_view(), name='login'),
    #signup
    #path('signup/', views.signupuser.as_view(), name='home'),
    #productos
    path('producto/', views.products.as_view(), name='products'),
    #detalle producto
    #path('producto/<slug>', views.details.as_view(), name='producto'),
    #detalle de producto version 2
    path('producto/<slug>', views.detalles.as_view(), name='producto'),
    #add to cart form
    path('myform/<slug>', views.addToCartForm, name='my_form_view_url'),
    #path('myform/', views.addToCartForm.as_view(), name='my_form_view_url')
    
    #path Carrito
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),

    #remove product
    path('myform2/<slug>', views.remove_from_cart, name='remove-from-cart'),

    #remover uno del carrito
    path('myform3/<slug>', views.remove_one_from_cart, name='remove-one-from-cart'),

    #agregar uno del carrito
    path('myform4/<slug>', views.add_one_from_cart, name='add-one-from-cart'),

    #checkout view
    path('checkout/', views.checkout.as_view(), name='checkout'),

    #select adress
    path('checkout/Domicilio',views.selectAddres.as_view(),name='slect-addres'),

    #add address
    path('checkout/Domicilio/agregar/', views.addAddres, name='add-addres'),

    #delete address
    path('checkout/Domicilio/detalle/<slug>', views.detalleAddres.as_view(), name='detalle-addres'),

    #delete address
    path('checkout/Domicilio/delete/<slug>', views.deleteAddres, name='delete-addres'),

    #seleccionar address
    path('checkout/Domicilio/selecionar/<slug>', views.selectDireccion, name='select-Direccion'),
    #confirmacion de pedido
    path('checkout/confirmar-pedido/', views.confirmar_Pedido, name='confirmacion-de-pedido'),
    #tu pedido ha sido realizado
    path('pedido-realizado', views.gracias_por_pedido, name='gracias-pedido'),
    #panel de control
    path('paneldecontrol', views.panel.as_view(), name='panel'),
    #agregar
    path('agregarProducto', views.addPrduct, name='agregar-producto'),
    #detalle de producto panel
    path('producto-Panel/<slug>', views.PanelDetalles.as_view(), name='producto_panel'),
    #detalle de producto panel edit
    path('producto-Panel/edit/<slug>', views.change_prodcuts, name='producto_panel_edit'),
    #detalle de orden pendioente
    path('Panel/ordenesAbiertas', views.ver_ordenes, name='OrdenesMasterAbiertas'),
    #detalle de orden cerrada 
    path('Panel/ordenesCerradas', views.ver_ordenes_Cerradas, name='OrdenesMasterCerradas'),
    #detalle de orden Enviada
    path('Panel/ordenesEnviadas', views.ver_ordenes_Enviadas, name='OrdenesMasterEnviadas'),
    #detalle orden cancelada
    path('Panel/ordenesCanceladas', views.ver_ordenes_canceladas, name='OrdenesMasterCanceladas'),
    #detalle orden
    path('Panel/ordenes/<int:la_pk>', views.observarla_orden, name='DetalleOrden'),
    #detalle orden button
    path('Panel/ordenes/can/<int:la_pk>', views.Cancelar_orden, name='DetalleOrdenCan'),
    #detalle orden button
    #path('Panel/ordenes/can/<int:la_pk>', views.Cancelar_orden, name='DetalleOrdenCan'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)