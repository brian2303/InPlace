let tablaInsumos
let compras = {
    items : {
        proveedor:'',
        fecha:'',
        subtotal:0.00,
        iva:0.0,
        total:0.00,
        insumos : []
    },
    // calcularTotalFactura : function () {
    //     $.each(this.items.insumos,function (pos,dict) {
    //         dict.subtotal = dict.cantidad * dict.preciocompra
    //     })
    // },
    add :function (item) {
        this.items.insumos.push(item)
        this.list()
    },
    list: function () {
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
                        return `<a class="btn btn-danger btn-xs"> 
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
                    max: 1000000000,
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

    //configurando la seleccion del iva
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 19,
        step: 1,
        decimals: 1,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
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
    $("#table-insumos tbody").on('change keyup','input[name="unidades"]',function () {
        let unidades =  parseInt($(this).val())
        let tr = tablaInsumos.cell($(this).closest('td, li')).index()
        let data = tablaInsumos.row(tr.row).node()
        compras.items.insumos[tr.row].cantidad = unidades
        compras.items.insumos[tr.row].subtotal = compras.items.insumos[tr.row].cantidad * compras.items.insumos[tr.row].preciocompra
        $('td:eq(5)',tablaInsumos.row(tr.row).node()).html(`$ ${compras.items.insumos[tr.row].subtotal}`)
    })
    //guardando el estado cada vez que se cambie el precio de compra
    $("#table-insumos tbody").on('change keyup','input[name="precio-compra"]',function () {
        let precioCompra = parseFloat($(this).val())
        let tr = tablaInsumos.cell($(this).closest('td, li')).index()
        let data = tablaInsumos.row(tr.row).node()
        compras.items.insumos[tr.row].preciocompra = precioCompra
        compras.items.insumos[tr.row].subtotal = compras.items.insumos[tr.row].cantidad * compras.items.insumos[tr.row].preciocompra
        $('td:eq(5)',tablaInsumos.row(tr.row).node()).html(`$ ${compras.items.insumos[tr.row].subtotal}`)
    })
})