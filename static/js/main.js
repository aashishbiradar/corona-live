if(true)
{
    Highcharts.chart('linecontainer', {
        chart: {
            type: 'areaspline'
        },
        title: {
            text: 'Corona Cases'
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 150,
            y: 100,
            floating: true,
            borderWidth: 1,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF'
        },
        xAxis: {
            categories: days.date,
            plotBands: [{ // visualize the weekend
                from: 4.5,
                to: 6.5,
                color: 'rgba(68, 170, 213, .2)'
            }]
        },
        yAxis: {
            title: {
                text: 'Total Infected'
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' cases'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.5
            }
        },
        series: [{
            name: 'Infected',
            data: days.total
        }]
    });
}
if(true)
{
    Highcharts.chart('piecontainer', {
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: 'Total Cases till '
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y}</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'share',
            data: [
                ['Active Cases',(parseInt(info.total)-parseInt(info.death)-parseInt(info.cured)-parseInt(info.migrated))],
                {
                    name: 'Cured',
                    y: parseInt(info.cured),
                    sliced: true,
                    selected: true
                },
                ['Migrated',parseInt(info.migrated)],
                ['Died', parseInt(info.death)]
            ]
        }]
    });
}
if (typeof data != 'undefined' && data) {
    Highcharts.chart('container', {
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Statewise Corona Cases'
        },
        xAxis: {
            categories: data.state
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Corona Cases'
            }

        },
        legend: {
            reversed: true
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        series: [{
            name: 'Indian',
            data: data.indian
        }, {
            name: 'Foreign',
            data: data.foreign
        }, {
            name: 'Discharged',
            data: data.discharged
        }, {
            name: 'Death',
            data: data.death
        }]
    });
}