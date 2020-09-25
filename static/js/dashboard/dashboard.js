
function RenderizarGraficoVentas(listaDeMeses) {
    
    let date = new Date()
    let year = date.getFullYear()
    Highcharts.chart('container', {
    
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