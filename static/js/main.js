Highcharts.chart('linecontainer', {
    chart: {
        type: 'area'
    },
    title: {
        text: 'Corona India Timeline',
        x:0,
        y:70,
        style: {
            color: '#333333',
            fontWeight: 'bold',
            fontSize:'18px'
        }
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
        categories: data.days.date,
        plotBands: [{
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Cases'
        }
    },
    tooltip: {
        shared: true,
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        area: {
            fillOpacity: 0.5,
            marker: {
                enabled: false,
                symbol: 'circle',
                radius: 2,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
        },
    },
    series: [{
        name: 'Confirmed Cases',
        data: data.days.confirmed,
        color: '#3498db'
    },
    {
        name: 'Recovered',
        data: data.days.recovered,
        color: '#27ae60'
    },
    {
        name: 'Deaths',
        data: data.days.death,
        color: '#34495e'
    }]
});
Highcharts.chart('piecontainer', {
    chart: {
        type: 'pie',
        height: 270
    },
    title: {
        text: data.info.confirmed+' cases',
        verticalAlign: 'middle',
        floating:true,
        x: 0,
        y: -10,
        style: {
            color: '#333333',
            fontWeight: 'bold',
            fontSize:'18px'
        }
    },
    plotOptions: {
        pie: {
            innerSize: 140,
            depth: 25,
            dataLabels: {
                enabled: false
            },
            showInLegend: true,
        }
    },
    series: [{
        type: 'pie',
        name: 'count',
        data: [
            {
                name: 'Active',
                y: data.info.active,
                color: '#3498db'
            },
            {
                name: 'Recovered',
                y: data.info.recovered,
                sliced: true,
                selected: true,
                color: '#2ecc71'
            },
            {
                name: 'Death',
                y: data.info.death,
                color: '#34495e'
            }
        ]
    }]
});
Highcharts.chart('container', {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Statewise Corona Cases',
        style: {
            color: '#333333',
            fontWeight: 'bold',
            fontSize:'18px'
        }
    },
    xAxis: {
        categories: data.statewise.state
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Confirmed Cases'
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
        name: 'Active',
        data: data.statewise.active,
        color: '#3498db'
    }, {
        name: 'Recovered',
        data: data.statewise.discharged,
        color: '#2ecc71'
    }, {
        name: 'Death',
        data: data.statewise.death,
        color: '#34495e'
    }]
});