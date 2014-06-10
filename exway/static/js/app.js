(function() {
  var app = angular.module('exway', ['ngRoute', 'cgBusy', 'expenses', 'reports']).
    config(function($httpProvider, $interpolateProvider) {
      // this is importants because is the standard header that django uses to
      // identify ajax requests
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

      // this is needed in order to distinguish between django template variable
      // substitution token
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
    });

  // app routes configurations
  app.config(function($routeProvider){
    $routeProvider.
      when('/', {
        templateUrl: 'partials/expenses.html',
        controller: 'ExpensesController'
      }).
      when('/reports', {
        templateUrl: 'partials/reports.html',
        controller: 'ReportsController'
      }).
      otherwise({redirectTo: '/'});
  });

  // controller user to handle menu clicks and add the properly classes to make
  // the user see that some menu item/url is currently active
  app.controller('PagesController', ['$location', '$log', function($location, $log){
    this.page = 1;

    this.currentUrl = function() {
      return $location.path();
    };

    this.selectPage = function(setPage) {
      this.page = setPage;
    };

    this.isSelected = function(checkPage) {
      return this.page == checkPage;
    };

  }]);

  // app filters
  app.filter('time', ['$filter', '$log', function($filter, $log){
    return function(input, format) {
      var time = moment.utc();
      time = time.toISOString().split('T')[0] + 'T' + input;
      time = moment.utc(time);

      return time.format(format);
    }
  }]);

})();
