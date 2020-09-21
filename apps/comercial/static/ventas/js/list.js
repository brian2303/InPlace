let tablaVentas
$(function () {
    tablaVentas = $('#table-ventas').DataTable({
        //responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdatasale',
            },
            dataSrc: ""
        },
        columns: [
            {"data": "cliente.numero_identificacion"},
            {"data": "cliente.nombres"},
            {"data": "fecha"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let conversion = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(data)
                    return `${conversion}`;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = `
                        <a style="color:white" id="detalleVenta" data-toggle="modal" data-target="#modalDetalle" class="btn btn-info btn-xs">
                            <i class="fas fa-search"></i>
                        </a>`
                        buttons += `
                        <a href="/comercial/ventas/eliminar/${row.id}" class="btn btn-danger btn-xs">
                            <i class="fas fa-trash"></i>
                        </a>`
                        buttons += `
                        <a style="color:white" href="/comercial/ventas/editar/${row.id}" class="btn btn-warning btn-xs">
                            <i class="fas fa-edit"></i>
                        </a>
                        `
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    //modal para mostrar el detalle
    function modalDetalle(detalle) {
        return(`
                <tr>
                    <td>${detalle.producto.nombre}</td>
                    <td>${detalle.precio_venta}</td>
                    <td>${detalle.cantidad}</td>
                    <td>${detalle.subtotal}</td>
                </tr>
            `
        )
    }

    $('#table-ventas tbody')
        .on('click','#detalleVenta',function () {
            let tr = tablaVentas.cell($(this).closest('td,li')).index()
            let venta = tablaVentas.row(tr.row).data()
            let detalleProductos = venta.detalle
            let bodyDetalle = document.getElementById('filas-detalle-venta')
            if (bodyDetalle.hasChildNodes()){
                bodyDetalle.innerHTML = ''
            } 
            detalleProductos.forEach(detalle => {
                bodyDetalle.innerHTML += modalDetalle(detalle) 
            });
        })
})