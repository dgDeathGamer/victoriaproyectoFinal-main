# reportes/views.py
from django.shortcuts import render
from ventas.models import Venta  # Asegúrate de tener el modelo Venta en la app ventas
from inventario.models import Inventario  # Asegúrate de tener el modelo Inventario en la app inventario
from django.db.models import Q
from datetime import datetime

def reporte_view(request):
    # Renderiza la página principal del reporte con el formulario vacío
    return render(request, 'reportes/reporte.html')

def generar_reporte(request):
    reportes = []
    tipo_reporte = request.GET.get('tipo_reporte')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Validar que las fechas estén proporcionadas
    if fecha_inicio and fecha_fin:
        try:
            # Convertir las fechas de string a objetos datetime
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

            # Validar que fecha_inicio no sea posterior a fecha_fin
            if fecha_inicio > fecha_fin:
                return render(request, 'reportes/reporte.html', {
                    'error': 'La fecha de inicio no puede ser posterior a la fecha de fin.',
                    'tipo_reporte': tipo_reporte,
                    'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
                })

            # Generar reportes según el tipo seleccionado
            if tipo_reporte == 'ventas':
                reportes = Venta.objects.filter(
                    fecha__range=(fecha_inicio, fecha_fin)
                )
            elif tipo_reporte == 'inventario':
                reportes = Inventario.objects.filter(
                    fecha__range=(fecha_inicio, fecha_fin)
                )
            else:
                return render(request, 'reportes/reporte.html', {
                    'error': 'Por favor, seleccione un tipo de reporte válido.',
                    'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
                })

        except ValueError:
            # Manejar error de formato de fecha inválido
            return render(request, 'reportes/reporte.html', {
                'error': 'Formato de fecha inválido. Use el formato YYYY-MM-DD.',
                'tipo_reporte': tipo_reporte,
            })

    else:
        # Si las fechas no están completas
        return render(request, 'reportes/reporte.html', {
            'error': 'Por favor, proporcione tanto la fecha de inicio como la fecha de fin.',
            'tipo_reporte': tipo_reporte,
        })

    # Renderizar el reporte con los resultados obtenidos
    return render(request, 'reportes/reporte.html', {
        'reportes': reportes,
        'tipo_reporte': tipo_reporte,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d') if fecha_inicio else None,
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d') if fecha_fin else None,
    })
