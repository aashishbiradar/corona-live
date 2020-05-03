var d = document;

//load json
var loadJson = function (url, onload) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
             onload(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
};

function plotDailyGraph()
{

    d.getElementById('daily-btn').style.backgroundColor="grey";
    d.getElementById('cumulative-btn').style.background="#3fb1cb";
    d.getElementById('cumulative-btn').disabled= false;
    d.getElementById('daily-btn').disabled= true;

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


function get_title()
{
    return "Corona " + data.type + " Timeline";
}

function plotCumulativeGraph()
{
    Highcharts.chart('linecontainer', {
        chart: {
            type: 'area'
        },
        title: {
            text: get_title(),
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
            // plotBands: [{
            //     from: 53,
            //     to:data.days.date.length,
            //     color: 'rgba(68, 170, 213, .2)',
            //     label: { 
            //     text: '21 days lockdown', // Content of the label. 
            //     align: 'center', // Positioning of the label. 
            //     //Default to center. x: +10 // Amount of pixels the label will be repositioned according to the alignment. 
            //     }
            // }]
        },
        yAxis: {
            title: {
                text: 'Cases',
                enabled: false
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

    // d.getElementById('daily-btn').style.backgroundColor= "#3fb1cb";
    // d.getElementById('cumulative-btn').style.backgroundColor= "grey";
    // d.getElementById('cumulative-btn').disabled= true;
    // d.getElementById('daily-btn').disabled= false;
}

function showBtns() {
    // d.getElementsByClassName('btn-section')[0].style.display = 'block';
}

plotCumulativeGraph();
 

Highcharts.chart('piecontainer', {
    chart: {
        type: 'pie',
        height: 270,
        events: {
            load: showBtns
        }
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
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b> ({point.percentage:.2f}%)'
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

if(false)
{
    var stateChartHeight = (Math.max((data.statewise.state.length * 36),200) + 'px');
    Highcharts.chart('statemap', {
        chart: {
            type: 'bar',
            height: stateChartHeight
        },
        title: {
            text: '',
            // style: {
            //     color: '#333333',
            //     fontWeight: 'bold',
            //     fontSize:'18px'
            // }
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
            name: 'Confirmed',
            data: data.statewise.confirmed,
            color: '#3498db'
        }]
    });
}

new Tablesort(document.getElementById('statewise-table'));

d.querySelectorAll('.state-table tr').forEach(function(tr) {
    tr.addEventListener('click', function() {
        link = this.getElementsByTagName('a')[0];
        link && link.click();
    });
});

/* Map function */

function mapFunction(geojson)
{
    var mapdata = [];
    for(i in geojson.features)
    {
        var dt_nm = geojson.features[i].properties.st_nm;
        var dt_in = data.statewise.state.indexOf(dt_nm);
        mapdata.push([dt_nm,data.statewise.confirmed[dt_in] || 0])
    }
    var series = [{
        data: mapdata,
        name : 'Confirmed',
    }]

    Highcharts.mapChart('india-map', {
        chart: {
            map: geojson,
        },
        title: {
            text: ''
        },
        plotOptions: {
            map: {
                allAreas: false,
                keys: ['st_nm', 'value'],
                joinBy: 'st_nm',
                states: {
                    hover: {
                        color: 'black'
                    }
                },
                dataLabels: {
                    enabled: false,
                },
            }
        },
        colorAxis: {
            min: 0,
            max: data.statewise.confirmed[0],
            minColor: '#FFFFFF',
            maxColor: '#08306b',
            lineColor: 'white',
            lineWidth: 10,
        },
        legend: {
            enabled: false,
        },
        mapNavigation: {
            enabled: false,
        },
        tooltip: {
            //headerFormat: '<span style="font-size:10px">Confirmed</span><br/>',
            pointFormat: '{point.st_nm}: <b>{point.value}</b> cases',
        },
        series: series,
    });
}

    




if(data.type == "India")
{
    var statekey = data.type.toLowerCase().replace(/ /g,"")
    loadJson('/static/maps/'+statekey+'.json',function(geojson){
        mapFunction(geojson);
    });
}

//State map
function plotStateMap(geojson)
{
    var red = [];
    var orange = [];
    var green = [];
    for(i in geojson.features)
    {
        var dt_nm = geojson.features[i].properties.district;
        var dt_in = data.statewise.state.indexOf(dt_nm);
        var dt_cases =  data.statewise.confirmed[dt_in] || 0;
        if (data.zone.red.indexOf(dt_nm) != -1) {
            red.push([dt_nm, dt_cases]);
        } else if(data.zone.orange.indexOf(dt_nm) != -1) {
            orange.push([dt_nm, dt_cases]);
        } else {
            green.push([dt_nm, dt_cases]);
        }
    }

    var series = [{
        data: orange,
        name : 'Orange Zone',
        color: 'orange'
    },{
        data: green,
        keys: ['district', 'value'],
        name : 'Green Zone',
        color: 'green'
    },{
        data: red,
        keys: ['district', 'value'],
        name : 'Red Zone',
        color: 'red'
    }];

   Highcharts.mapChart('statemap', {
        chart: {
            map: geojson,
        },
        title: {
            text: ''
        },
        plotOptions: {
            map: {
                allAreas: false,
                keys: ['district', 'value'],
                joinBy: 'district',
                states: {
                    hover: {
                        color: 'black'
                    }
                },
                dataLabels: {
                    enabled: false,
                },
            }
        },
        mapNavigation: {
            enabled: false,
        },
        tooltip: {
            //headerFormat: '<span style="font-size:10px">Confirmed</span><br/>',
            pointFormat: '{point.district}: <b>{point.value}</b> cases',
        },
        series: series,
    });
}

if(data.type != "India")
{
    var statekey = data.type.toLowerCase().replace(/ /g,"")
    loadJson('/static/maps/'+statekey+'.json',function(geojson){
        plotStateMap(geojson);
    });
}
// state timeline
function plotStatewiseTimeline(timelineData)
{
    var states = [];
    var marked_states =['Karnataka','Maharashtra','Gujarat','Delhi','Rajasthan']
    for(i in timelineData)
    {
        if(i != 'date' && i!= 'Total')
        {
            if(marked_states.includes(i))
            {
                details = {
                    name: i,
                    data: timelineData[i],
                }
                states.push(details)
            }
            else
                {
                    details = {
                        name: i,
                        data: timelineData[i],
                        visible:false
                    }
                    states.push(details)
                }
        }
    } 

    Highcharts.chart('statetimeline-confirmed', {
        chart: {
            type: 'areaspline',
            height: 600
        },
        title: {
            text: 'Statewise Confirmed  Cases Timeline'
        },
        legend: {
            align: 'right',
            verticalAlign: 'top',
            layout: 'vertical',
            x: 0,
            y: 0,
            borderWidth: 1,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF'
        },
        xAxis: {
            categories: timelineData.date,
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' '
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0
            },
            series: {
                marker: {
                    enabled: false,
                    symbol: "circle",
                    radius: 2
                }
            }
        },
        series: states
    }); 
}

window.innerWidth > 700 
&& data.type == "India" 
&& loadJson('/statewise-timeline/', function(d){plotStatewiseTimeline(d);});

// load twitter timeline on scroll
var twitterLoaded = false;

var getDocHeight = function() {
    return Math.max(
        d.body.scrollHeight, d.documentElement.scrollHeight,
        d.body.offsetHeight, d.documentElement.offsetHeight,
        d.body.clientHeight, d.documentElement.clientHeight
    )
}

var amountscrolled = function (){
    var winheight= window.innerHeight || (document.documentElement || document.body).clientHeight
    var docheight = getDocHeight()
    var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop
    var trackLength = docheight - winheight
    var pctScrolled = Math.floor(scrollTop/trackLength * 100) // gets percentage scrolled (ie: 80 or NaN if tracklength == 0)
    return pctScrolled;
}

window.addEventListener("scroll", function(){
    var scrl = amountscrolled();
    if(!twitterLoaded && scrl > 50) {
        var twitterBox = d.getElementsByClassName('twitter-box')[0];
        twitterBox.innerHTML =
        ('<a class="twitter-timeline" data-width="500px" href="https://twitter.com/coronaindia_ml?ref_src=twsrc%5Etfw">Tweets by coronaindia_ml</a>');
        var s = d.createElement("script");
        s.charset = 'utf-8';
        s.type = "text/javascript";
        s.async = true;
        s.src = "https://platform.twitter.com/widgets.js";
        d.body.appendChild(s);
        s.onload = function () { twitterBox.style.display = 'block'; };
        twitterLoaded = true;
    }
}, false)

