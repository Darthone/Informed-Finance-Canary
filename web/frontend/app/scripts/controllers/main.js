'use strict';

/**
 * @ngdoc function
 * @name ifcApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ifcApp
 */
angular.module('ifcApp')
  .controller('MainCtrl', ['$scope', 'data', function ($scope, data) {
    // Contols what options pop up on the calendar
    $scope.ranges =  {
         'Last 30 Days': [moment().subtract(29, 'days'), moment()],
         'Last 90 Days': [moment().subtract(89, 'days'), moment()],
         'Last Year': [moment().subtract(1, 'years'), moment()],   
         'Last 5 Years': [moment().subtract(5, 'years'), moment()],
    } 

    // options to add calculations
    $scope.calcOpts = [ 
      {name: 'mavg', prop: {window: 10}, description:"Simple moving average"},
      {name: 'rsi', prop: {window: 14}, description:"Relative Strength Index is a momentum oscillator that measures the speed and change of price movements"},
      {name: 'ema', prop: {window: 12}, description:"Exponential moving average"},
      {name: 'macd', prop: {signal: 9, fast: 12, slow: 26}, description:"Moving average convergence divergence is a trend-following momentum indicator that shows the relationship between two moving averages of prices"},
      {name: 'mom', prop: {window: 1}, description:"Momentum Measures the change in price"},
      {name: 'rocr', prop: {window: 3}, description:"Rate of Change Compute"},
      {name: 'atr', prop: {window: 14}, description:"Average True Range Shows volatility of market"},
      {name: 'mfi', prop: {window: 14}, description:"Money Flow Index Relates typical price with Volume"},
      {name: 'adx', prop: {window: 14, adx: 14}, description:"Average Directional Index Discover if trend is developing"},
      {name: 'cci', prop: {window: 12}, description:"Commodity Channel Index Identifies cyclical turns in stock price"},
      {name: 'obv', prop: {window: 14}, description:"On Balance Volume is a momentum indicator that uses volume flow"},
      {name: 'trix', prop: {window: 15 }, description:"Triple Exponential Moving Average Smooth the insignificant movements"}
    ]


    $scope.selected = {ticker:null, calcs:[]}
    $scope.tickers = {data: data.getTickers()};

    $scope.articles = {data: []};
    $scope.getArticles = function() {
      if ($scope.selected.ticker == null) 
        return;

      if ($scope.showChart == true){
				$scope.createChart(); // updated chart on date change
			}
      var start, end;
      try {
        start = moment($scope.datePicker.date.startDate).format("YYYY-MM-DD");
        end = moment($scope.datePicker.date.endDate.endDate).format("YYYY-MM-DD");
      } catch (err) {
        console.log(err)
        start =  $scope.datePicker.date.startDate.format("YYYY-MM-DD");
        end =  $scope.datePicker.date.endDate.format("YYYY-MM-DD");
      }

      data.getArticles(start, end, $scope.selected.ticker.sym).then(function (response) {
        $scope.articles.data = response.data.data;
      });

    }

    $scope.copyCalc = function (ind) {
      var cur = $scope.selected.calcs[ind];
      var dupe = angular.copy(cur);
      dupe.id = ind; // this is a hack
      $scope.selected.calcs.splice(ind + 1, 0, dupe);
    }

    $scope.addBasicCalcs = function () {
      $scope.selected.calcs.push($scope.calcOpts[0]); //sma
      $scope.selected.calcs.push($scope.calcOpts[1]); //rsi
      $scope.selected.calcs.push($scope.calcOpts[3]); //macd
    };

    $scope.addAdvancedCalcs = function () {
      $scope.selected.calcs.push($scope.calcOpts[4]); //mom
      $scope.selected.calcs.push($scope.calcOpts[5]); //rocr
      $scope.selected.calcs.push($scope.calcOpts[6]); //atr
      $scope.selected.calcs.push($scope.calcOpts[7]); //mfi
      $scope.selected.calcs.push($scope.calcOpts[8]); //adx
      $scope.selected.calcs.push($scope.calcOpts[9]); //cci
      $scope.selected.calcs.push($scope.calcOpts[10]); //obv
      $scope.selected.calcs.push($scope.calcOpts[11]); //trix
    }

    $scope.datePicker = {date: null};
    $scope.datePicker.date = {
      startDate: moment().subtract(29, 'days'),
      endDate: moment()
    };

    var groupingUnits = [
      [
        'week', // unit name
        [1, 2, 3] // allowed multiples
      ], [
        'month',
        [1, 2, 3, 4, 6]
      ]
    ];

    var chart = {
      chart:{
        zoomType: 'x',
        height: '65%'
      },
      title: {
          text: 'Hello'
      },
      yAxis: [
        {
          labels: {
            align: 'right',
            x: -3
          },
          title: {
            text: 'OHLC'
          },
          height: '60%',
          lineWidth: 2
        }, {
          labels: {
            align: 'right',
            x: -3
          },
          title: {
            text: 'Volume'
          } ,
          top: '65%',
          height: '35%',
          offset: 0,
          lineWidth: 2
        }
      ],
      foo: [{
        name: 'Stock',
        type: 'candlestick',
        data: [],
        tooltip: {
          valueDecimals: 2
        },
				indicators: [],
        dataGrouping: {
          units: groupingUnits
        }
      }, {
        type: 'column',
        name: 'Volume',
        data: [],
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits
        }
      }],
      tooltip: {
				split: true
			},
      plotOptions: {
			  candlestick: {
					color: 'red',
					upColor: 'green'
			  }
      },
    };
  

    $scope.showChart = false;
    $scope.showGears = false;

    $scope.createChart = function () {
      $scope.showGears = true;
      $scope.showChart = !$scope.showChart;

      var start, end;
      var params = [];
      angular.forEach($scope.selected.calcs, function (item) {
        params.push({type: item.name, param: item.prop});
      });

      try {
        start = moment($scope.datePicker.date.startDate).format("YYYY-MM-DD");
        end = moment($scope.datePicker.date.endDate.endDate).format("YYYY-MM-DD");
      } catch (err) {
        console.log(err);
        start =  $scope.datePicker.date.startDate.format("YYYY-MM-DD");
        end =  $scope.datePicker.date.endDate.format("YYYY-MM-DD");
      }

      data.getStockData(start, end, $scope.selected.ticker.sym, params).then(function (response) {
        chart.title.text = $scope.selected.ticker.name;
        chart.series = chart.foo;
        chart.series[0].data = response.data.ohlc;
        chart.series[1].data = response.data.volume;
        angular.forEach(response.data.columns, function(col) {
          chart.series.push({
            type: 'line',
            name: col,
            data: response.data[col],
            dataGrouping: { units: groupingUnits}
          });
        });
        $scope.showGears = false;
        $scope.showChart = true; // something funky happens here 
        // Removed for now. See https://stackoverflow.com/questions/16216722/highcharts-hidden-charts-dont-get-re-size-properly
        $('#myChart').highcharts('StockChart', chart);
      });
    }
      
  }]);

