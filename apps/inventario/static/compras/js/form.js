let tablaInsumos
let compras = {
    items : {
        proveedor:'',
        fecha: '',
        subtotal:0.00,
        iva:0.0,
        total:0.00,
        insumos : []
    },
    calcularTotalFactura : function () {
        let subtotal = 0
        $.each(this.items.insumos,function (pos,dict) {
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
        this.items.insumos.push(item)
        this.list()
    },
    list: function () {
        this.calcularTotalFactura()
        tablaInsumos = $('#table-insumos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy : true,
            //lista con los insumos
            data: this.items.insumos,
            columns: [
                {'data':'id'},
                {'data':'nombre'},
                {'data':'unidad_medida.nombre'},
                {'data':'preciocompra'},
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
                        return `<input type="text" name="precio-compra"
                                        class="form-control form-control-sm input-sm" autocomplete="off" 
                                        value="${row.preciocompra}"/>`
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
                $(row).find('input[name="precio-compra"]').TouchSpin({
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
    // aplicandole la libreria select2 al campo de proveedor
    $('.select2').select2({
        theme :'bootstrap4',
        language : 'es',
    })
    //configuracion para que salga calendario.
    $('#fecha').datetimepicker({
        format:'YYYY-MM-DD',
        date : moment().format("YYYY-MM-DD"),
        locale : 'es',
        //minDate : moment().format("YYYY-MM-DD"), 
        maxDate : moment().format("YYYY-MM-DD"),
    });
    //Buscador de insumos
    $('input[name="search"]').autocomplete({
        source : function (request,response) {
            //peticion ajax para buscar insumos
            $.ajax({
                url : window.location.pathname,
                type: 'POST',
                data : {
                    'action':'buscar_insumos',
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
            ui.item.preciocompra = 0.00
            ui.item.cantidad = 1
            ui.item.subtotal = 0.00
            /* el metodo add de mi objeto compras configurado al inicio
                agrega el insumo a el array insumos de mi objeto items */
            compras.add(ui.item)
            $(this).val('')
            
        }
    })

    //guardando el estado cada vez que se cambien las unidades de un insumo
    $("#table-insumos tbody")
        .on('click','a[rel="remove"]',function () {
            let tr = tablaInsumos.cell($(this).closest('td, li')).index()
            compras.items.insumos.splice(tr.row,1)
            compras.list()
        })
        .on('change keyup','input[name="unidades"]',function () {
            let unidades =  parseInt($(this).val())
            let tr = tablaInsumos.cell($(this).closest('td, li')).index()
            compras.items.insumos[tr.row].cantidad = unidades
            compras.items.insumos[tr.row].subtotal = compras.items.insumos[tr.row].cantidad * compras.items.insumos[tr.row].preciocompra
            $('td:eq(5)',tablaInsumos.row(tr.row).node()).html(`$ ${compras.items.insumos[tr.row].subtotal}`)
            compras.calcularTotalFactura()
        })
    //guardando el estado cada vez que se cambie el precio de compra
    $("#table-insumos tbody").on('change keyup','input[name="precio-compra"]',function () {
            let precioCompra = parseFloat($(this).val())
            let tr = tablaInsumos.cell($(this).closest('td, li')).index()
            compras.items.insumos[tr.row].preciocompra = precioCompra
            compras.items.insumos[tr.row].subtotal = compras.items.insumos[tr.row].cantidad * compras.items.insumos[tr.row].preciocompra
            $('td:eq(5)',tablaInsumos.row(tr.row).node()).html(`$ ${compras.items.insumos[tr.row].subtotal}`)
            compras.calcularTotalFactura()
    })
    //borrando el detalle de insumos de manera completa.
    $('#btnBorrarDetalle').on('click',function () {
            if(compras.items.insumos.length === 0)return false
            Swal.fire({
                title: 'Are you sure delete detail?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes!',
                cancelButtonText: 'No!'
            }).then((result) => {
                if (result.value) {
                    compras.items.insumos = []
                    compras.list()
                }
            })
    })

    // enviar los datos a la vista correspondiente
    const URL = window.location.pathname
    $('#form-guardar-compra').on('submit',function (e) {
        e.preventDefault()
        compras.items.proveedor = $('select[name="proveedor"]').val()
        compras.items.fecha = $('input[name="fecha"]').val()
        $.ajax({
            url : URL,
            type: 'POST',
            data : {
                'action': $('input[name="action"]').val(),
                'compras': JSON.stringify(compras.items)
            },
            dataType : 'JSON'
        }).done(function (data) {
            //respuesta despues de guardar la compra con su detalle
            Swal.fire({
                title: 'Registro Guardado exitosamente',
                text: "Listo !!",
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'OK!'
            }).then((result) => {
                if (result.value) {
                    //window.location.href = "/inventario/proveedor/lista"
                }
            })
        })
    })
})