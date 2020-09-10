let tablaCompras
$(function () {
    tablaCompras = $('#table-compras').DataTable({
        //responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "proveedor.nombre"},
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
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = `
                        <a style="color:white" id="detalleCompra" data-toggle="modal" data-target="#modalDetalle" class="btn btn-info btn-xs">
                            <i class="fas fa-search"></i>
                        </a>`
                        buttons += `
                        <a href="/inventario/compra/eliminar/${row.id}" class="btn btn-danger btn-xs">
                            <i class="fas fa-trash"></i>
                        </a>`
                        buttons += `
                        <a style="color:white" href="/inventario/compra/editar/${row.id}" class="btn btn-warning btn-xs">
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
                    <td>${detalle.insumo.nombre}</td>
                    <td>${detalle.precio_compra}</td>
                    <td>${detalle.cantidad}</td>
                    <td>${detalle.subtotal}</td>
                </tr>
            `
        )
    }

    $('#table-compras tbody')
        .on('click','#detalleCompra',function () {
            let tr = tablaCompras.cell($(this).closest('td,li')).index()
            let compra = tablaCompras.row(tr.row).data()
            let detalleInsumos = compra.detalle
            let bodyDetalle = document.getElementById('filas-detalle-compra')
            if (bodyDetalle.hasChildNodes()){
                bodyDetalle.innerHTML = ''
            }
            console.log(bodyDetalle) 
            detalleInsumos.forEach(detalle => {
                bodyDetalle.innerHTML += modalDetalle(detalle) 
            });
        })
})