$(function () {
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
})