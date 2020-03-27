Highcharts.chart('linecontainer', {
    chart: {
        type: 'areaspline'
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
        data: data.days.infected
    }]
});

var infectedTotal = (parseInt(data.info.infected)+parseInt(data.info.cured)+parseInt(data.info.migrated)+parseInt(data.info.death));
Highcharts.chart('piecontainer', {
    chart: {
        type: 'pie',
        height: 270
    },
    title: {
        text: infectedTotal+' cases',
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
                y: parseInt(data.info.infected),
                color: '#3498db '
            },
            {
                name: 'Recovered',
                y: parseInt(data.info.cured),
                sliced: true,
                selected: true,
                color: '#2ecc71'
            },
            {
                name: 'Migrated',
                y: parseInt(data.info.migrated),
                color: '#9b59b6'
            },
            {
                name: 'Death',
                y: parseInt(data.info.death),
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
        name: 'Indian',
        data: data.statewise.indian,
        color: '#3498db'
    }, {
        name: 'Foreign Nationals',
        data: data.statewise.foreign,
        color: '#9b59b6'
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