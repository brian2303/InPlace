function generarReporte(fecha_ini,fecha_fin,accion,cliente){
    let parametros;
    debugger
    if (accion==="buscar_reporte_fecha"){
        parametros = {
            'action':accion,
            'fecha_inicial':`${fecha_ini}`,
            'fecha_final':`${fecha_fin}`,
        }
    }else{
        parametros = {
            'action':accion,
            'cliente':cliente
        }
    }
    $('#table-list').DataTable({
        responsive: true,
        autoWidth: false,
        destroy : true,
        deferRender:true,
        paging :false,
        info:false,
        ordering:false,
        order:false,
        searching:false,
        dom:'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="ml-1 fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="ml-1 fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                
            }
        ],
        ajax :{
            url: window.location.pathname,
            type:'POST',
            data: parametros,
            dataSrc : '',
        },
        columns :[
            {'data':'cliente.numero_identificacion'},
            {'data':'cliente.nombres'},
            {'data':'fecha'},
            {'data':'subtotal'},
            {'data':'iva'},
            {'data':'total'},
        ],
        columnDefs:[
            {
                targets : [-1,-2,-3],
                class : 'text-center',
                orderable :false,
                render: function (data,type,row) {
                    let conversion = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(data)
                    return `${conversion}`
                }
            }
        ]
    })
}


$(function () {
    $('input[name="rango_fecha"]').daterangepicker({
        locale:{
            format : 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-check"></i> Seleccionar',
            cancelLabel: '<i class="fas fa-window-close"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function(ev, picker) {
        fecha_incial = picker.startDate.format('YYYY-MM-DD')
        fecha_final = picker.endDate.format('YYYY-MM-DD')
        generarReporte(fecha_incial,fecha_final,'buscar_reporte_fecha','')
    }).on('cancel.daterangepicker', function(ev, picker) {
        let fechaActual = new moment().format('YYYY-MM-DD')
        $(this).data('daterangepicker').setStartDate(fechaActual);
        $(this).data('daterangepicker').setEndDate(fechaActual);
        generarReporte(fechaActual,fechaActual,'buscar_reporte_fecha','')
    });
    $('#id_cliente').on('change',function () {
        let cliente = $(this).val()
        generarReporte('','','buscar_reporte_cliente',cliente)
    })
})
