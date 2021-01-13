$(document).ready(function(){
    function renderChart(id, data, labels){
        var ctx = $('#' + id)
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales',
                    data: data,
                    backgroundColor: 'rgba(8, 197, 30, 0.2)',
                    borderColor: 'rgba(8, 197, 30, 1)',
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    function getSalesData(type, id){
        var url = '/analytics/sales/data/';
        var method = 'GET'
        var data = {"type": type}
        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function(responseData){
                renderChart(id, responseData.data, responseData.labels);
            },
            error: function(error){
                $.alert("An error occure")
            }
        })
    }

    // getSalesData('week', 'thisWeekSales');
    // getSalesData('4weeks', 'fourWeekSales');

    var chartsToReander = $('.cfe-render-chart');

    $.each(chartsToReander, function(index, html){
        var $this = $(this)
        if ($this.attr('data-type') && $this.attr('id')) {
            getSalesData($this.attr('data-type'), $this.attr('id'))
        }
    })
})