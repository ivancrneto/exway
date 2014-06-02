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
      otherwise({redirectTo: '/'});
  });

  app.controller('ExpensesController', function($scope){

  });
})();
