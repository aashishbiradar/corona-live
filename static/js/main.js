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