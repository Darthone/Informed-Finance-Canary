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

    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

		$scope.articles = [
      {
        title: 'foo',
        date: '20140313T00:00:00',
        text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sit amet enim ac lectus pellentesque lobortis ac eu lorem. Suspendisse auctor massa mi, id dapibus odio suscipit nec. Aenean maximus accumsan accumsan. Donec maximus suscipit dolor, vitae finibus nibh dictum in. Vestibulum fringilla pretium purus in maximus. Nam semper congue arcu, convallis interdum nibh placerat ac. Fusce scelerisque lobortis elit eu blandit. Etiam volutpat accumsan leo viverra malesuada. Aliquam erat volutpat. Duis metus quam, tempor vel porta vel, feugiat a ex. Sed sollicitudin, neque vel feugiat molestie, turpis nulla blandit felis, quis cursus magna lacus eu mi.          Aliquam erat volutpat. Duis nec tempus turpis. Curabitur ultrices, augue ut tempus sollicitudin, urna mauris viverra odio, quis vestibulum dui risus vel velit. Aliquam urna nisl, pretium sit amet condimentum a, tempus sit amet purus. Donec quam odio, faucibus non vehicula ac, dignissim volutpat magna. Donec placerat libero sem, eu luctus nulla faucibus in. Ut feugiat lectus et enim ultrices accumsan. Duis cursus enim at nunc scelerisque, vel blandit odio rutrum. Ut tempus nulla nibh, ac vestibulum orci auctor in. Duis tincidunt elementum finibus. Maecenas eget risus vel dui efficitur convallis non ut justo. Integer faucibus nisi quis auctor elementum. Morbi rutrum odio pretium, feugiat lorem eget, tempor risus. Cras porttitor placerat malesuada.          Integer cursus ultricies consectetur. In sapien ex, condimentum vitae mattis id, fringilla id ex. Aenean eget ex volutpat, tincidunt nibh eu, egestas sem. Quisque id ante aliquet, elementum lectus at, convallis ipsum. Aenean luctus, ex ut pharetra imperdiet, velit nibh semper tellus, vel semper ligula diam sit amet tortor. Quisque mattis elit ex, at ornare lectus porta aliquet. Sed orci est, pellentesque quis egestas tempus, rutrum sit amet urna. Fusce eu mi nisl.",
        keywords: ['Curabitur ultrices', 'vel blandit', 'tortor', 'faucibus'],
        url: 'google.com'
      }
    ]

    $scope.ranges =  {
         'Last 30 Days': [moment().subtract(29, 'days'), moment()],
         'Last 90 Days': [moment().subtract(89, 'days'), moment()],
         'Last Year': [moment().subtract(1, 'years'), moment()],   
         'Last 5 Years': [moment().subtract(5, 'years'), moment()],
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
				loading: false,
				useHighStocks: true
		};


  }]);



