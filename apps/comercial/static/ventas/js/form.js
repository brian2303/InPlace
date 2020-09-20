let tablaProductos
//objeto literal que se envia a la vista de django para guardar registro de compra con su detalle
let ventas = {
    items : {
        estado :'',
        cliente:'',
        fecha: '',
        subtotal:0.00,
        iva:0.0,
        total:0.00,
        productos : []
    },
    calcularTotalFactura : function () {
        let subtotal = 0
        $.each(this.items.productos,function (pos,dict) {
            subtotal += dict.subtotal
        })
        this.items.subtotal = subtotal
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2))
        this.items.iva = this.items.subtotal * 0.19
        $('input[name="iva"]').val(this.items.iva.toFixed(2))
        this.items.total = this.items.subtotal + this.items.iva
        $('input[name="total"]').val(this.items.total.toFixed(2))
    },
    add :function (item) {
        this.items.productos.push(item)
        this.list()
    },
    list: function () {
        this.calcularTotalFactura()
        tablaProductos = $('#table-productos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy : true,
            //lista con los productos
            data: this.items.productos,
            columns: [
                {'data':'id'},
                {'data':'nombre'},
                {'data':'categoria.nombre_categoria'},
                {'data':'precioventa'},
                {'data':'cantidad'},
                {'data':'subtotal'},
            ],
            columnDefs:[
                {
                    targets:[0],
                    class:'text-center',
                    orderable:'false',
                    render: function (data,type,row) {
                        return `<a rel="remove" class="btn btn-danger btn-xs" style="color:white"> 
                                    <i class="fas fa-trash-alt"></i>
                                </a>`
                    }
                },
                {
                    targets:[3],
                    orderable:'false',
                    render: function (data,type,row) {
                        return `<input type="text" name="precio-venta"
                                        class="form-control form-control-sm input-sm" autocomplete="off" 
                                        value="${row.precioventa}"/>`
                    }
                },
                {
                    targets:[-2],
                    orderable:'false',
                    render: function (data,type,row) {
                        return `<input type="text" name="unidades"
                                        class="form-control form-control-sm input-sm" autocomplete="off"
                                        value="${row.cantidad}"/>`
                    }
                },
                {
                    targets:[-1],
                    orderable:'false',
                    render: function (data,type,row) {
                        return `
                        <span>${row.subtotal}<span/>
                        `
                    }
                },               
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                $(row).find('input[name="unidades"]').TouchSpin({
                    initval:1,
                    min: 1,
                    max: 100,
                    step: 1,
                })
                $(row).find('input[name="precio-venta"]').TouchSpin({
                    initval:100,
                    max: 1000000,
                    stepinterval: 50,
                    prefix: '$'
                })
                
            }
        })
    } 
}
$(function () {
    ventas.list()
    // aplicandole la libreria select2 al campo de cliente
    $('.select2').select2({
        theme :'bootstrap4',
        language : 'es',
    })
    //configuracion para que salga calendario.
    $('#fecha').datetimepicker({
        format:'YYYY-MM-DD',
        date : $('#fecha').val(),
        locale : 'es',
        //minDate : moment().format("YYYY-MM-DD"), 
        maxDate : moment().format("YYYY-MM-DD"),
    });
    //Buscador de productos
    $('input[name="search"]').autocomplete({
        source : function (request,response) {
            //peticion ajax para buscar insumos
            $.ajax({
                url : window.location.pathname,
                type: 'POST',
                data : {
                    'action':'buscar_productos',
                    // en este parametro va lo que el usuario ingresa para buscar
                    'term': request.term
                },
                dataType : 'JSON'
            }).done(function (data) {
                //muestra los insumos con los que encontro concidencia
                response(data)
            })
        },
        delay:500,
        minLength:1,
        //logica que se aplica cuando se selecciona uno de los insumos encontrados
        select: function (event,ui) {
            event.preventDefault()
            /*en ui.item se guarda el elemento que se acabo de seleccionar
                le agregamos las propiedades que no trae.
            */
            ui.item.precioventa = 0.00
            ui.item.cantidad = 1
            ui.item.subtotal = 0.00
            /* el metodo add de mi objeto ventas configurado al inicio
                agrega el producto a el array productos de mi objeto items */
            ventas.add(ui.item)
            //limpia el campo de busqueda
            $(this).val('')
            
        }
    })

    //guardando el estado cada vez que se cambien las unidades de un producto
    $("#table-productos tbody")
        .on('click','a[rel="remove"]',function () {
            let tr = tablaProductos.cell($(this).closest('td, li')).index()
            ventas.items.productos.splice(tr.row,1)
            ventas.list()
        })
        .on('change keyup','input[name="unidades"]',function () {
            let unidades =  parseInt($(this).val())
            let tr = tablaProductos.cell($(this).closest('td, li')).index()
            //cada vez que se van cambiando las unidades se va recalculando todos los valores
            ventas.items.productos[tr.row].cantidad = unidades
            ventas.items.productos[tr.row].subtotal = ventas.items.productos[tr.row].cantidad * ventas.items.productos[tr.row].precioventa
            $('td:eq(5)',tablaProductos.row(tr.row).node()).html(`$ ${ventas.items.productos[tr.row].subtotal}`)
            ventas.calcularTotalFactura()
        })
    //guardando el estado cada vez que se cambie el precio de venta
    $("#table-productos tbody").on('change keyup','input[name="precio-venta"]',function () {
            let precioVenta = parseFloat($(this).val())
            let tr = tablaProductos.cell($(this).closest('td, li')).index()
            ventas.items.productos[tr.row].precioventa = precioVenta
            ventas.items.productos[tr.row].subtotal = ventas.items.productos[tr.row].cantidad * ventas.items.productos[tr.row].precioventa
            $('td:eq(5)',tablaProductos.row(tr.row).node()).html(`$ ${ventas.items.productos[tr.row].subtotal}`)
            ventas.calcularTotalFactura()
    })
    //borrando la lista de insumos completa.
    $('#btnBorrarDetalle').on('click',function () {
            if(ventas.items.productos.length === 0)return false
            Swal.fire({
                title: 'Estas seguro de eliminar el detalle?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Si!',
                cancelButtonText: 'No!'
            }).then((result) => {
                if (result.value) {
                    ventas.items.productos = []
                    ventas.list()
                }
            })
    })

    //boton de limpiar busqueda de detalle de productos
    $('#limpiarBusqueda').on('click',function () {
        $('input[name="search"]').val('').focus()
    })
    // enviar los datos a la vista django (/comercial/ventas/crear)
    const URL = window.location.pathname
    $('#form-guardar-venta').on('submit',function (e) {
        e.preventDefault()
        if(ventas.items.productos.length === 0){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Debes agregar almenos un producto al detalle!',
            })
            return false
        }
        ventas.items.cliente = $('select[name="cliente"]').val()
        ventas.items.fecha = $('input[name="fecha"]').val()
        ventas.items.estado = $('select[name="estado"]').val()
        let redireccion = ''
        if (ventas.items.estado == 'cotizacion'){
            redireccion = '/comercial/cotizaciones/lista'
        }else{
            redireccion = '/comercial/ventas/lista'
        }
        $.ajax({
            url : URL,
            type: 'POST',
            data : {
                'action': $('input[name="action"]').val(),
                'ventas': JSON.stringify(ventas.items),
            },
            dataType : 'JSON'
        }).done(function (data) {
            Swal.fire({
                title: 'Registro Guardado exitosamente',
                text: "Listo !!",
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'OK!'
            }).then(result =>{
                if(result.value){
                    window.location.href = redireccion
                }
            })
        })
    })
})