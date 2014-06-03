(function(){
  var app = angular.module('expenses', []);

  app.controller('ExpensesController', function(){
    var expensesCtrl = this;

    this.expenses = [{
      id: 1,
      description: 'A new monitor for my MacBook',
      date: '06/02/2014',
      time: '15:34 AM',
      amount: 300,
      comment: 'I need that because my older one broke'
    }];

    this.deleteExpense = function(expense) {
      var index = expensesCtrl.expenses.indexOf(expense);
      expensesCtrl.expenses.splice(index, 1);
    }

  });

  app.controller('ReportsController', function(){

  });
})();
