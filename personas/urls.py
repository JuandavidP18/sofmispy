from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro_usuario'),  # Nueva URL para el registro de usuarios
    path('sign_up/', views.sign_up, name='sign_up'),
    path('pagina_inicio/', views.pagina_inicio, name='pagina_inicio'),
    path('log_in/', views.log_in, name='log_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ventas/', views.ventas, name='ventas'),
    path('inventario/', views.inventario, name='inventario'),
    path('compras/', views.compras, name='compras'),
    path('registrar-producto/', views.registrar_producto, name='registrar_producto'),
    path('mostrar_productos/', views.mostrar_productos, name='mostrar_productos'),
    path('obtener_detalles_producto/', views.obtener_detalles_producto, name='obtener_detalles_producto'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),
    path('enviar_correo/', views.enviar_correo, name='enviar_correo'),
    path('crear_venta/', views.crear_venta, name='crear_venta'),
    path('reportes/', views.reportes, name='reportes'),
    path('generar_reporte_pdf/',  views.generar_reporte_pdf, name='generar_reporte_pdf'),
    path('generar_reporte_usuarios_pdf/', views.generar_reporte_usuarios_pdf, name='generar_reporte_usuarios_pdf'),
    path('generar_reporte_ventas_pdf/', views.generar_reporte_ventas_pdf, name='generar_reporte_ventas_pdf'),
    path('agregar_proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('editar_proveedor/', views.editar_proveedor, name='editar_proveedor'),
    path('obtener_detalles_proveedor/', views.obtener_detalles_proveedor, name='obtener_detalles_proveedor'),
    path('eliminar_proveedor/', views.eliminar_proveedor, name='eliminar_proveedor'),

]   
# Configuración para servir archivos estáticos en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)