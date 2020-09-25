// configuracion inicial de idioma
Highcharts.setOptions({
    lang: {
        downloadCSV:'Descargar CSV',
        downloadJPEG:'Descargar imagen JPEG',
        downloadPDF:'Descargar PDF',
        downloadPNG:'Descargar imagen PNG',
        downloadSVG:'Descargar vector de imagen',
        downloadXLS:'Descargar XLS',
        printChart: 'Imprimir grafico',
        viewFullscreen:'Ver en pantalla completa',
        viewData :'Ver en formato de tabla',
        hideData: 'Ocultar tabla'
    }
});
// Renderiza el grafico de ventas mensuales
function RenderizarGraficoVentas(listaDeMeses) {
    
    let date = new Date()
    let year = date.getFullYear()
    Highcharts.chart('containersale', {


        title: {
            text: `Reporte de ventas ${year}`
        },
    
        subtitle: {
            text: 'InPlace'
        },
    
        yAxis: {
            title: {
                text: 'Valor'
            },
            tickInterval: 1000000,
            max: 5000000
        },
    
        xAxis: {
            categories: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
                'Mayo',
                'Junio',
                'Julio',
                'Agosto',
                'Septiembre',
                'Octubre',
                'Noviembre',
                'Diciembre',
            ]
        },
    
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
    
        series: [{
            name: 'Ventas',
            data: JSON.parse(listaDeMeses)
        }],
    
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }
    
    });
}
//Grafico para mostrar los 10 productos con stock mas bajo
function renderizarGraficoStockBajo(nombre,cantidad) {
    Highcharts.chart('containerlowerstock', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Top 10 insumos con stock bajo'
        },
        subtitle: {
            text: 'InPlace'
        },
        xAxis: {
            categories: nombre,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Cantidad'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Insumos',
            data: cantidad,
        }]
    });
}