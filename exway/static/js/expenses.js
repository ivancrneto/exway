(function(){
  var app = angular.module('expenses', []);

  app.controller('ExpensesController', function(){
    var expensesCtrl = this;

    this.currentExpense = {};
    this.expenses = [];

    this.hideForm = function(){
      expensesCtrl.currentExpense = {};
      expensesCtrl.showForm = false;
    };

    this.deleteExpense = function(expense){
      var index = expensesCtrl.expenses.indexOf(expense);
      expensesCtrl.expenses.splice(index, 1);
    };

    this.addExpense = function(){
      expensesCtrl.expenses.push(expensesCtrl.currentExpense);
      expensesCtrl.currentExpense = {}
    };

  });

  app.controller('ReportsController', function(){

  });
})();
