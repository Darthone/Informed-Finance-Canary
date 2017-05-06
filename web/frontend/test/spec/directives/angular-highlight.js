'use strict';

describe('Directive: angularHighlight', function () {

  // load the directive's module
  beforeEach(module('ifcApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<angular-highlight></angular-highlight>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the angularHighlight directive');
  }));
});
