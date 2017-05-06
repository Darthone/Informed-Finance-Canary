'use strict';

describe('Directive: highlight', function () {

  // load the directive's module
  beforeEach(module('ifcApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<highlight></highlight>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the highlight directive');
  }));
});
