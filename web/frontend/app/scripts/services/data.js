'use strict';

/**
 * @ngdoc service
 * @name ifcApp.data
 * @description
 * # data
 * Factory in the ifcApp.
 */
angular.module('ifcApp')
  .factory('data', function () {
    // Service logic
    // ...

    var meaningOfLife = 42;

    // Public API here
    return {
      someMethod: function () {
        return meaningOfLife;
      }
    };
  });
