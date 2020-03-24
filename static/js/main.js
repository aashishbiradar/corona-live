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
            name: 'Browser share',
            data: [
                ['Active Cases',(parseInt(info.total)-parseInt(info.death)-parseInt(info.cured)-parseInt(info.migrated))],
                ['Cured', parseFloat(info.cured)],
                ['Migrated',info.migrated],
                ['Died', info.death]
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
            text: 'Statewise Stats'
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