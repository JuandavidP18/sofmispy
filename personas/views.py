from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuarios
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect

from .models import Producto
from django.contrib import messages
import os
from django.conf import settings


from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import date

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Venta, DetalleVenta
from datetime import datetime
import json

from django.core.mail import send_mail
from django.http import HttpResponse


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from django.shortcuts import render
from .models import Venta
from django.db.models import Sum
from django.db.models.functions import TruncDay

from .models import Proveedor
from django.db.models import Count

def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('lemail')
        contraseña = request.POST.get('lpassword')

        try:
            usuario = Usuarios.objects.get(email=email)
        except Usuarios.DoesNotExist:
            usuario = None

        if usuario and check_password(contraseña, usuario.contraseña):
            return redirect('dashboard')  # Cambiado a redireccionar al dashboard
        else:   
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')

    return render(request, 'persona/log-in.html')

def inicio(request):
    return render(request, 'persona/index.html')

def sign_up(request):
    return render(request, 'persona/sign-up.html')

def compras(request):
    # Obtener el total de proveedores activos
    total_proveedores_activos = Proveedor.objects.filter(estatus='activo').count()

    # Obtener la fecha de hoy
    fecha_hoy = datetime.now().date()

    # Calcular la fecha de hace un día (para obtener los proveedores creados hoy)
    fecha_hace_un_dia = fecha_hoy - timedelta(days=1)

    # Obtener el total de proveedores nuevos (creados hoy)
    total_proveedores_nuevos = Proveedor.objects.filter(fecha_registro__date=fecha_hoy).count()

    proveedores = Proveedor.objects.all()
    return render(request, 'persona/compras.html', {
        'proveedores': proveedores,
        'total_proveedores_activos': total_proveedores_activos,
        'total_proveedores_nuevos': total_proveedores_nuevos
    })

def agregar_proveedor(request):
    if request.method == 'POST':
        # Recibes los datos desde el formulario
        nombre = request.POST.get('product-name')
        estatus = request.POST.get('product-status')
        telefono = request.POST.get('product-telephone')
        correo = request.POST.get('product-email')

        # Creas un nuevo objeto Proveedor y lo guardas en la base de datos
        Proveedor.objects.create(nombre=nombre, estatus=estatus, telefono=telefono, correo=correo)

        # Rediriges a donde desees
        return redirect('compras')  # Reemplaza 'ruta_de_exito' con la URL adecuada

    # Si la solicitud no es POST, simplemente redirige a donde desees
    return redirect('compras')

def editar_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id')
        if proveedor_id is not None:
            try:
                proveedor = Proveedor.objects.get(id=proveedor_id)
                proveedor.nombre = request.POST.get('product-name')
                proveedor.telefono = request.POST.get('product-telephone')
                proveedor.correo = request.POST.get('product-email')
                proveedor.estatus = request.POST.get('product-status')
                proveedor.save()
                return redirect('compras')
            except Proveedor.DoesNotExist:
                pass
    return redirect('compras')


def obtener_detalles_proveedor(request):
    if request.method == 'GET':
        proveedor_id = request.GET.get('proveedor_id')
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        detalles_proveedor = {
            'nombre': proveedor.nombre,
            'estatus': proveedor.estatus,
            'telefono': proveedor.telefono,
            'correo': proveedor.correo,
            # Otros campos del proveedor que desees incluir
        }
        return JsonResponse(detalles_proveedor)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id')
        try:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            proveedor.delete()
            return redirect('compras')
        except Proveedor.DoesNotExist:
            pass
    return redirect('compras')

#----------------------Fin de proveedores-----------------------------------
def dashboard(request):
    if request.method == 'POST':
        # Obtener los datos del formulario y crear un nuevo producto
        nombre = request.POST.get('nombre')
        imagen = request.FILES.get('imagen')
        estatus = request.POST.get('estatus')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        
        Producto.objects.create(
            nombre=nombre,
            imagen=imagen,
            estatus=estatus,
            precio=precio,
            stock=stock
        )
    
    # Obtener todos los productos de la base de datos
    productos = Producto.objects.all()

    # Calcular el total de dinero de todos los productos
    total_dinero_productos = productos.aggregate(total_dinero=Sum('precio'))['total_dinero'] or 0

    # Obtener la cantidad de nuevos productos creados el mismo día
    hoy = date.today()
    nuevos_productos = Producto.objects.filter(fecha_creacion__date=hoy).count()

    # Obtener la cantidad de productos activos (excluyendo los agotados)
    cantidad_productos_activos = Producto.objects.exclude(estatus='agotado').count()

    # Obtener la cantidad de productos agotados
    cantidad_productos_agotados = Producto.objects.filter(estatus='agotado').count()

    # Obtener todas las ventas de la base de datos
    ventas = Venta.objects.all()

    return render(request, 'persona/dashboard.html', {
        'productos': productos,
        'total_dinero_productos': total_dinero_productos,
        'nuevos_productos': nuevos_productos,
        'cantidad_productos_activos': cantidad_productos_activos,
        'cantidad_productos_agotados': cantidad_productos_agotados,
        'ventas': ventas,
    })
def pagina_inicio(request):
    return render(request, 'persona/log-in.html')

def ventas(request):
    productos = Producto.objects.all()
    return render(request, 'persona/ventas.html', {'productos': productos})

def reportes(request):
    return render(request, 'persona/reportes.html')

def generar_reporte_pdf(request):
    productos = Producto.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    data = []
    data.append(['Nombre', 'Estatus', 'Precio', 'Stock', 'Fecha de Creación'])
    for producto in productos:
        data.append([producto.nombre, producto.estatus, producto.precio, producto.stock, producto.fecha_creacion])

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                       ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    tabla = Table(data)
    tabla.setStyle(style)

    elementos = []
    elementos.append(tabla)
    doc.build(elementos)

    return response

def generar_reporte_usuarios_pdf(request):
    usuarios = Usuarios.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    data = []
    data.append(['Nombre', 'Correo'])
    for usuario in usuarios:
        data.append([usuario.nombres, usuario.email])

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                       ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    tabla = Table(data)
    tabla.setStyle(style)

    elementos = []
    elementos.append(tabla)
    doc.build(elementos)

    return response
def generar_reporte_ventas_pdf(request):
    ventas = Venta.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    data = []
    data.append(['Cliente', 'Fecha', 'Total', 'Producto', 'Cantidad'])

    for venta in ventas:
        detalles_venta = DetalleVenta.objects.filter(venta=venta)
        productos_venta = []
        cantidades_venta = []

        for detalle in detalles_venta:
            productos_venta.append(detalle.producto.nombre)
            cantidades_venta.append(detalle.cantidad)

        # Concatenar todos los productos comprados en una sola cadena
        productos_str = ", ".join(productos_venta)

        # Concatenar todas las cantidades correspondientes a los productos comprados
        cantidades_str = ", ".join(map(str, cantidades_venta))

        data.append([
            venta.cliente_nombre,
            venta.fecha.strftime("%d/%m/%Y %H:%M"),  # Formato de fecha personalizado
            venta.total,
            productos_str,
            cantidades_str
        ])

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                       ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    tabla = Table(data)
    tabla.setStyle(style)

    elementos = []
    elementos.append(tabla)
    doc.build(elementos)

    return response
# generar una venta 
def ventas(request):
    # Obtener todas las ventas
    ventas = Venta.objects.all()
    
    # Obtener todos los detalles de venta
    detalles_ventas = DetalleVenta.objects.all()
    
    # Obtener todos los productos
    productos = Producto.objects.all()
    
    # Obtener la cantidad total de ventas
    cantidad_ventas = ventas.count()
    
    # Obtener las ganancias de las ventas realizadas hoy
    hoy = date.today()
    ganancias_hoy = Venta.objects.filter(fecha__date=hoy).aggregate(total_ganancias=Sum('total'))
    ganancias_hoy = ganancias_hoy['total_ganancias'] if ganancias_hoy['total_ganancias'] else 0
    
    context = {
        'ventas': ventas,
        'detalles_ventas': detalles_ventas,
        'productos': productos,
        'cantidad_ventas': cantidad_ventas,
        'ganancias_hoy': ganancias_hoy
    }
    return render(request, 'persona/ventas.html', context)
# views.py
def crear_venta(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        cliente_nombre = request.POST.get('customer_name')
        total = request.POST.get('total')
        
        # Obtener los productos seleccionados y sus cantidades
        productos_seleccionados_json = request.POST.get('productos_seleccionados')
        cantidades_json = request.POST.get('cantidades')
        
        # Convertir los datos de JSON a listas
        productos_seleccionados = json.loads(productos_seleccionados_json)
        cantidades = json.loads(cantidades_json)

        # Guardar la fecha y hora actual
        fecha_venta = datetime.now()

        # Crear una instancia de Venta y guardarla en la base de datos
        venta = Venta.objects.create(cliente_nombre=cliente_nombre, total=total, fecha=fecha_venta)

        # Guardar los detalles de la venta (productos seleccionados) en la base de datos
        for producto_id, cantidad in zip(productos_seleccionados, cantidades):
            producto = Producto.objects.get(pk=producto_id)
            DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=int(cantidad))

        return render(request, 'persona/ventas.html')
    else:
        return render(request, 'persona/index.html')
#ventas 

def enviar_correo(request):
    if request.method == 'POST':
        correo_destinatario = request.POST.get('correo')
        id_venta = request.POST.get('id_venta')
        
        try:
            venta = Venta.objects.get(pk=id_venta)
            detalles_venta = DetalleVenta.objects.filter(venta=venta)
            
            # Construir el contenido del correo electrónico con los detalles de la venta
            asunto = 'Detalles de la venta'
            mensaje = f'Aquí están los detalles de la venta:\n\n' \
                      f'Nombre del Cliente: {venta.cliente_nombre}\n' \
                      f'Fecha de Venta: {venta.fecha}\n' \
                      f'Total de Venta: {venta.total}\n' \
                      'Detalles de la compra:\n'
            
            for detalle in detalles_venta:
                mensaje += f'- Producto: {detalle.producto.nombre}, Cantidad: {detalle.cantidad}\n'
            
            # Enviar el correo electrónico
            send_mail(
                asunto,
                mensaje,
                'juandavidsierrapinzon@gmail.com',  # Reemplaza esto con tu dirección de correo electrónico
                [correo_destinatario],
                fail_silently=False,
            )
            
            return redirect('ventas')
        
        except Venta.DoesNotExist:
            return HttpResponse('La venta no existe.')
        
        except Exception as e:
            return HttpResponse(f'Ocurrió un error al enviar el correo: {e}')
    
    else:
        return HttpResponse('Este endpoint solo acepta solicitudes POST.')



def inventario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario y crear un nuevo producto
        nombre = request.POST.get('nombre')
        imagen = request.FILES.get('imagen')
        estatus = request.POST.get('estatus')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        
        Producto.objects.create(
            nombre=nombre,
            imagen=imagen,
            estatus=estatus,
            precio=precio,
            stock=stock
        )
    
    # Obtener todos los productos de la base de datos
    productos = Producto.objects.all()

    # Calcular el total de dinero de todos los productos
    total_dinero_productos = productos.aggregate(total_dinero=Sum('precio'))['total_dinero'] or 0

    # Obtener la cantidad de nuevos productos creados el mismo día
    hoy = date.today()
    nuevos_productos = Producto.objects.filter(fecha_creacion__date=hoy).count()

    # Obtener la cantidad de productos activos (excluyendo los agotados)
    cantidad_productos_activos = Producto.objects.exclude(estatus='agotado').count()

    # Obtener la cantidad de productos agotados
    cantidad_productos_agotados = Producto.objects.filter(estatus='agotado').count()

    return render(request, 'persona/inventario.html', {
        'productos': productos,
        'total_dinero_productos': total_dinero_productos,
        'nuevos_productos': nuevos_productos,
        'cantidad_productos_activos': cantidad_productos_activos,
        'cantidad_productos_agotados': cantidad_productos_agotados,
    })




def registro_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('semail')
        nombres = request.POST.get('sname')
        contraseña = request.POST.get('spassword')
        
        # Encriptación de la contraseña
        contraseña_encriptada = make_password(contraseña)
        
        # Crear un nuevo objeto Usuarios con la contraseña encriptada
        nuevo_usuario = Usuarios(email=email, nombres=nombres, contraseña=contraseña_encriptada)
        nuevo_usuario.save()
        
        return redirect('inicio')

    return render(request, 'persona/index.html')



def registrar_producto(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('product-name')
        imagen = request.FILES.get('product-image')
        estatus = request.POST.get('product-status')
        precio = request.POST.get('product-price')
        stock = request.POST.get('product-stock')

        # Crear un nuevo objeto Producto con los datos del formulario
        nuevo_producto = Producto(nombre=nombre, estatus=estatus, precio=precio, stock=stock)
        nuevo_producto.save()

        # Guardar la imagen en la carpeta de static/productos
        ruta_carpeta_productos = os.path.join(settings.BASE_DIR, 'personas','static', 'productos')
        if not os.path.exists(ruta_carpeta_productos):
            os.makedirs(ruta_carpeta_productos)

        # Construir la ruta para guardar la imagen
        nombre_imagen = f'{nombre.replace(" ", "_")}{os.path.splitext(imagen.name)[1]}'
        ruta_imagen = os.path.join(ruta_carpeta_productos, nombre_imagen)

        # Guardar la imagen en la carpeta de static/productos
        with open(ruta_imagen, 'wb') as f:
            for chunk in imagen.chunks():
                f.write(chunk)

        # Asignar la ruta de la imagen al objeto Producto y guardarlo
        nuevo_producto.imagen = os.path.join('static','productos', nombre_imagen)
        nuevo_producto.save()

        # Redirigir a alguna página de éxito o a donde desees
        return redirect('inventario')

    return render(request, 'persona/inventario.html')

def mostrar_productos(request):
    productos = Producto.objects.all()
    print("Número de productos:", len(productos))  # Imprime el número de productos en la consola
    return render(request, 'persona/inventario.html', {'productos': productos})
from django.shortcuts import get_object_or_404

def editar_producto(request):
    if request.method == 'POST':
        # Obtener el ID del producto a editar del formulario
        producto_id = request.POST.get('producto_id')
        # Obtener el producto de la base de datos
        producto = get_object_or_404(Producto, pk=producto_id)

        # Actualizar los datos del producto con los datos del formulario
        producto.nombre = request.POST.get('nombre_producto')
        producto.estatus = request.POST.get('estatus')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')

        # Actualizar la imagen del producto si se proporciona una nueva
        imagen = request.FILES.get('imagen_producto')
        if imagen:
            # Guardar la imagen en la carpeta de static/productos
            ruta_carpeta_productos = os.path.join(settings.BASE_DIR, 'personas', 'static', 'productos')
            if not os.path.exists(ruta_carpeta_productos):
                os.makedirs(ruta_carpeta_productos)

            # Construir la ruta para guardar la imagen
            nombre_imagen = f'{producto.nombre.replace(" ", "_")}{os.path.splitext(imagen.name)[1]}'
            ruta_imagen = os.path.join(ruta_carpeta_productos, nombre_imagen)

            # Guardar la imagen en la carpeta de static/productos
            with open(ruta_imagen, 'wb') as f:
                for chunk in imagen.chunks():
                    f.write(chunk)

            # Asignar la ruta de la imagen al objeto Producto y guardar
            producto.imagen = os.path.join('static', 'productos', nombre_imagen)

        # Guardar los cambios en el producto
        producto.save()

        # Redirigir a alguna página de éxito o a donde desees
        return redirect('inventario')

    # Si la solicitud no es POST, redirigir a alguna página de error o a donde desees
    return redirect('index')


def obtener_detalles_producto(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        producto_id = request.GET.get('producto_id')
        producto = Producto.objects.filter(id=producto_id).values().first()
        if producto:
            return JsonResponse(producto, safe=False)
        else:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)
    
def eliminar_producto(request):
    if request.method == 'POST':
        # Obtener el ID del producto a eliminar
        producto_id = request.POST.get('product_id')
        # Obtener el producto de la base de datos
        producto = get_object_or_404(Producto, pk=producto_id)
        # Eliminar el producto
        producto.delete()
        # Redirigir a alguna página de éxito o a donde desees
        return redirect('inventario')
    # Si la solicitud no es POST, redirigir a alguna página de error o a donde desees
    return redirect('inventario')    

def tu_vista(request):
    # Total de todos los productos en dinero
    total_dinero_productos = Producto.objects.aggregate(total_dinero=Sum('precio'))['total_dinero']

    # Nuevos productos (creados el mismo día)
    hoy = datetime.now().date()
    nuevos_productos = Producto.objects.filter(fecha_creacion=hoy).count()

    # Productos activos y su cantidad
    productos_activos = Producto.objects.filter(estatus='activo')
    cantidad_productos_activos = productos_activos.count()

    # Productos agotados y su cantidad
    productos_agotados = Producto.objects.filter(estatus='agotado')
    cantidad_productos_agotados = productos_agotados.count()

    # Total de productos agotados
    total_productos_agotados = productos_agotados.aggregate(total_agotados=Sum('stock'))['total_agotados']

    return render(request, 'tu_template.html', {
        'total_dinero_productos': total_dinero_productos,
        'nuevos_productos': nuevos_productos,
        'cantidad_productos_activos': cantidad_productos_activos,
        'cantidad_productos_agotados': cantidad_productos_agotados,
        'total_productos_agotados': total_productos_agotados
    })