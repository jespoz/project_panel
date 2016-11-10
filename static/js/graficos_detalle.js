$('#graph').highcharts({

        chart: {
            type: 'gauge',
            margin: 10,
            backgroundColor: 'transparent'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '120%',
            startAngle: -90,
            endAngle: 90,
            background: null
        },

        tooltip: {
            enabled: false
        },
        
        yAxis: {
            tickPositions: [0, 40, 70, 90, 110, 130],
            tickmarkPlacement: 'on',
            tickLength: 54,
            minorTickLength: 1,
            min: 0,
            max: 130,
            labels: {
              distance: 20,
              format: '{value}%'
            },
            plotBands: [{
              from: 0,
              to: 70,
              color: '#CC0000',
              thickness: '50%'
            }, {
              from: 70,
              to: 90,
              color: '#F26013',
              thickness: '50%'
            }, {
              from: 90,
              to: 110,
              color: '#5CB85C',
              thickness: '50%'
            }, {
              from: 110,
              to: 130,
              color: '#00669E',
              thickness: '50%'
            }]        
        },

        plotOptions: {
            gauge: {
              dataLabels: {
                enabled: false
              },
              dial: {
                baseLength: '0%',
                baseWidth: 10,
                radius: '100%',
                rearLength: '0%',
                topWidth: 1
              }
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'Avance',
            data: [0]
        }]
});

setTimeout(function () {
    var chart = $('#graph').highcharts(),
        point,
        newVal,
        inc;

    var valor = $('#graph').data('value');

    if (valor > 100) {
      valor = 130;
    }

    if (chart) {
        point = chart.series[0].points[0];
        newVal = point.y + parseFloat(valor);

        point.update(newVal);
    }
}, 1000);
