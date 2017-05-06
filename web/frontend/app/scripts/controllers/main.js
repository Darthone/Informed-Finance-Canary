'use strict';

/**
 * @ngdoc function
 * @name ifcApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ifcApp
 */
angular.module('ifcApp')
  .controller('MainCtrl', ['$scope', function ($scope) {

		$scope.articles = {data:[
      {
        title: 'foo',
        date: '20140313T00:00:00',
        text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sit amet enim ac lectus pellentesque lobortis ac eu lorem. Suspendisse auctor massa mi, id dapibus odio suscipit nec. Aenean maximus accumsan accumsan. Donec maximus suscipit dolor, vitae finibus nibh dictum in. Vestibulum fringilla pretium purus in maximus. Nam semper congue arcu, convallis interdum nibh placerat ac. Fusce scelerisque lobortis elit eu blandit. Etiam volutpat accumsan leo viverra malesuada. Aliquam erat volutpat. Duis metus quam, tempor vel porta vel, feugiat a ex. Sed sollicitudin, neque vel feugiat molestie, turpis nulla blandit felis, quis cursus magna lacus eu mi.          Aliquam erat volutpat. Duis nec tempus turpis. Curabitur ultrices, augue ut tempus sollicitudin, urna mauris viverra odio, quis vestibulum dui risus vel velit. Aliquam urna nisl, pretium sit amet condimentum a, tempus sit amet purus. Donec quam odio, faucibus non vehicula ac, dignissim volutpat magna. Donec placerat libero sem, eu luctus nulla faucibus in. Ut feugiat lectus et enim ultrices accumsan. Duis cursus enim at nunc scelerisque, vel blandit odio rutrum. Ut tempus nulla nibh, ac vestibulum orci auctor in. Duis tincidunt elementum finibus. Maecenas eget risus vel dui efficitur convallis non ut justo. Integer faucibus nisi quis auctor elementum. Morbi rutrum odio pretium, feugiat lorem eget, tempor risus. Cras porttitor placerat malesuada.          Integer cursus ultricies consectetur. In sapien ex, condimentum vitae mattis id, fringilla id ex. Aenean eget ex volutpat, tincidunt nibh eu, egestas sem. Quisque id ante aliquet, elementum lectus at, convallis ipsum. Aenean luctus, ex ut pharetra imperdiet, velit nibh semper tellus, vel semper ligula diam sit amet tortor. Quisque mattis elit ex, at ornare lectus porta aliquet. Sed orci est, pellentesque quis egestas tempus, rutrum sit amet urna. Fusce eu mi nisl.",
        keywords: ['Curabitur ultrices', 'vel blandit', 'tortor', 'faucibus'],
        url: 'https://www.google.com'
      },
	    {
        title: 'Some really long and important Title',
        date: '20170413T00',
        text: 'this is just a really short article',
        keywords: ['short'],
        url: 'https://www.youtube.com'
      }
    ]};

    /*$scope.hoverIn = function(){
				this.hoverEdit = true;
		};

		$scope.hoverOut = function(){
				this.hoverEdit = false;
		};
*/
    //$scope.show = false;

    $scope.ranges =  {
         'Last 30 Days': [moment().subtract(29, 'days'), moment()],
         'Last 90 Days': [moment().subtract(89, 'days'), moment()],
         'Last Year': [moment().subtract(1, 'years'), moment()],   
         'Last 5 Years': [moment().subtract(5, 'years'), moment()],
    } 

    $scope.selected = {ticker:null, calcs:[]}

    $scope.tickers = {data:[{sym:'TGT', name:'Target Corporation'}, {sym:'GM', name:'General Motors Company'}, {sym:'UAA', name:'Under Armour Inc Class A'}]};

    //TODO BACKEND
    //$scope.tickers.data = getTickers();

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
    $scope.datePicker.date = {startDate: moment().subtract(29, 'days'), endDate: moment()};

    $scope.chartConfig = {
				options: {
						chart: {
								type: 'line',
								zoomType: 'x'
						}
				},
				series: [{
						data: [10, 15, 12, 8, 7, 1, 1, 19, 15, 10]
				}],
				title: {
						text: 'Hello'
				},
				xAxis: {currentMin: 0, currentMax: 10, minRange: 1},
				loading: true,
				useHighStocks: true,

		};

    $scope.showChart = false;

    $scope.createChart = function () {
      $scope.showChart = true;
      //TODO
      //backend stuff
      setTimeout(myFunction, 3000);
				setTimeout(function(){ 
					//$scope.chartConfig.loading = false;
				}, 3000);  
    }
      
  }]);

