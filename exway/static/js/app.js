(function() {
  var app = angular.module('exway', ['ngRoute']).
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
  app.controller('PagesController', function(){
    this.page = 1;

    this.selectPage = function(setPage) {
      this.page = setPage;
    };

    this.isSelected = function(checkPage) {
      return this.page == checkPage;
    };

  });

  app.controller('ExpensesController', function($log){
    var expensesCtrl = this;

    this.expenses = [{
      id: 1,
      description: 'A new monitor for my MacBook',
      date: '06/02/2014',
      time: '15:34 AM',
      amount: 300,
      comment: 'I need that because my older one broke'
    }];

    this.delete = function(expense) {
      var index = expensesCtrl.expenses.indexOf(expense);
      expensesCtrl.expenses.splice(index, 1);
    }

  });

  app.controller('ReportsController', function(){

  });
})();
