(function() {
  var app = angular.module('exway', ['ngRoute']).
    config(function($httpProvider, $interpolateProvider) {
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
    });

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

  app.controller('PagesController', function(){
    this.page = 1;

    this.selectPage = function(setPage) {
      this.page = setPage;
    };

    this.isSelected = function(checkPage) {
      return this.page == checkPage;
    };

  });

  app.controller('ExpensesController', function(){

  });

  app.controller('ReportsController', function(){

  });
})();
