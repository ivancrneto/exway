(function(){
  var app = angular.module('expenses', []);

  app.controller('ExpensesController', ['$http', function($http){
    var expensesCtrl = this;

    this.currentExpense = {};
    this.expenses = [];

    // get expenses data from api and fill expenses array
    $http.get('/api/expenses/', {format: 'json'}).success(function(data){
      expensesCtrl.expenses = data;
    });


    this.hideForm = function(){
      expensesCtrl.currentExpense = {};
      expensesCtrl.showForm = false;
    };

    this.deleteExpense = function(expense){
      var index = expensesCtrl.expenses.indexOf(expense);
      expensesCtrl.expenses.splice(index, 1);
    };

    this.addExpense = function(){
      var data = expensesCtrl.currentExpense;
      data['format'] = 'json';
      $http.post('/api/expenses/', data).
        success(function(data, status){
          if(status == 201){
            expensesCtrl.expenses.push(expensesCtrl.currentExpense);
            expensesCtrl.currentExpense = {};
          }
        });
    };

  }]);

  app.controller('ReportsController', function(){

  });
})();
