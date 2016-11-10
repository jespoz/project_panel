chart_actividades = new Highcharts.Chart({
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        renderTo: 'graph-actividades'
    },
    credits: false,
    title: {
        text: null
    },
    tooltip: {
        pointFormat: '<b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b style="font-size: 1.7em;">{point.y}</b>',
                distance: -40
            },
            showInLegend: true
        }
    }
});

$.getJSON('/pie_actividades/', function (data) {
    var datos = [];
    $.each(data.response, function (key, val) {
        datos.push({
            name: val.name,
            y: Math.round(val.data),
            color: val.color
        });
    });
    var series = {data: datos};
    chart_actividades.addSeries(series);
});

chart_encurso = new Highcharts.Chart({
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'bar',
        renderTo: 'graph-encurso'
    },
    credits: false,
    title: {
        text: null
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f}%</b>'
    },
    yAxis: {
    	gridLineWidth: 0,
        min: 0,
        labels: {
        	enabled: false
        },
        title: {
            text: null,
        }
    },
    legend: {
    	enabled: false
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true,
                format: '<b>{y} %</b>',
                color: '#F26013',
                style: {
                	fontSize: '1.2em'
                }
            }
        },
        series: {
            pointWidth: 30
        }
    }
});

$.getJSON('/bar_encurso/', function (data) {
    var datos = [];
    var categorias = [];
    $.each(data.response, function (key, val) {
    	categorias.push(val.name);
        datos.push({
            y: Math.round(val.data)
        });
    });
    chart_encurso.xAxis[0].setCategories(categorias);
    var series = {data: datos, color: '#F0AD4E'};
    chart_encurso.addSeries(series);
});

chart_terminadas = new Highcharts.Chart({
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'bar',
        renderTo: 'graph-terminadas'
    },
    credits: false,
    title: {
        text: null
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f}%</b>'
    },
    yAxis: {
    	gridLineWidth: 0,
        min: 0,
        labels: {
        	enabled: false
        },
        title: {
            text: null,
        }
    },
    legend: {
    	enabled: false
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true,
                format: '<b>{y} %</b>',
                color: '#F26013',
                style: {
                	fontSize: '1.2em'
                }
            }
        },
        series: {
            pointWidth: 30
        }
    }
});

$.getJSON('/bar_terminada/', function (data) {
    var datos = [];
    var categorias = [];
    $.each(data.response, function (key, val) {
    	categorias.push(val.name);
        datos.push({
            y: Math.round(val.data)
        });
    });
    chart_terminadas.xAxis[0].setCategories(categorias);
    var series = {data: datos, color: '#5cb85c'};
    chart_terminadas.addSeries(series);
});