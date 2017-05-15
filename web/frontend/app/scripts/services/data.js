'use strict';

/**
 * @ngdoc service
 * @name ifcApp.data
 * @description
 * # data
 * Factory in the ifcApp.
 */
angular.module('ifcApp')
  .factory('data', function ($http) {

    var baseUrl = "http://marsha:5001/";
    var articlesUrl = baseUrl + "articles?";
    var stockUrl = baseUrl + "stock?";

    return {
      getTickers: function () {
        return [
                {sym:'TGT', name:'Target Corporation'}, 
                {sym:'GM', name:'General Motors Company'}, 
                {sym:'UAA', name:'Under Armour Inc'}
        ];
      },
      getStockData: function (start, end, sym, params) {
        var url = stockUrl + "start=" + start + "&end=" + end + "&symbol=" + sym + "&params=" + angular.toJson(params);
        return $http({
             url: url, 
             method: "GET",
        });
      },
      getArticles: function (start, end, sym) {
        var url = articlesUrl + "start=" + start + "&end=" + end + "&symbol=" + sym;
        return $http({
             url: url, 
             method: "GET",
        });
      }

    };
  });
