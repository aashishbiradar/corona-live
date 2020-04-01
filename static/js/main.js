function plotDailyGraph()
{

    document.getElementById('daily-btn').style.backgroundColor="grey";
    document.getElementById('cumulative-btn').style.background="#3fb1cb";
    document.getElementById('cumulative-btn').disabled= false;
    document.getElementById('daily-btn').disabled= true;

    Highcharts.chart('linecontainer', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Corona India Timeline',
            x:0,
            y:80,
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
            categories:data.days.date,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Cases'
            }
        },

        tooltip: {
            shared: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Confirmed',
            data: data.days.confirmedincrease,
            color: '#3498db' ,
        }, {
            name: 'Recovered',
            data: data.days.recoveredincrease,
            color: '#27ae60'

        }, {
            name: 'Death',
            data: data.days.deathincrease,
            color: '#34495e'
        }]
    });
}

function plotCumulativeGraph()
{
    document.getElementById('daily-btn').style.backgroundColor= "#3fb1cb";
    document.getElementById('cumulative-btn').style.backgroundColor= "grey";
    document.getElementById('cumulative-btn').disabled= true;
    document.getElementById('daily-btn').disabled= false;

    Highcharts.chart('linecontainer', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Corona India Timeline',
            x:0,
            y:85,
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
                from: 23,
                to:data.days.date.length,
                color: 'rgba(68, 170, 213, .2)',
                label: { 
                text: '21 days lockdown', // Content of the label. 
                align: 'center', // Positioning of the label. 
                //Default to center. x: +10 // Amount of pixels the label will be repositioned according to the alignment. 
                }
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
        series: [ 
    /*    {
            name: '15% increase daily',
            data: data.days.predict,
            color: '#f7df1e'
        },*/
        {
            name: 'Confirmed',
            data: data.days.confirmed,
            color: '#3498db'
        },
        {
            name: 'Recovered',
            data: data.days.recovered,
            color: '#27ae60'
        },
        {
            name: 'Death',
            data: data.days.death,
            color: '#34495e'
        }]
    });
}

plotCumulativeGraph();

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