(function(){
  var app = angular.module('expenses', []);

  app.controller('ExpensesController', ['$log', '$http', function($log, $http){
    var expensesCtrl = this;

    // this flag controls if the user is editing any table row
    this.editing = false;

    // this keeps the old expense for cases where the user cancels editing
    this.oldExpense = {};

    // currentExpense keeps the data from the adding form
    this.currentExpense = {};

    // this is the list of all expenses that will come from server
    this.expenses = [];

    // get expenses data from api and fill expenses array
    $http.get('/api/expenses/', {format: 'json'}).success(function(data){
      for(i in data){
        data[i]['amount'] = parseFloat(data[i]['amount']);
        expensesCtrl.expenses.push(data[i]);
      }
    });


    this.hideForm = function(){
      expensesCtrl.currentExpense = {};
      expensesCtrl.showForm = false;
    };

    this.deleteExpense = function(expense){
      var url = '/api/expenses/' + expense.id + '/'
      $http.delete(url).
        success(function(data, status){
          if(status == 204){
            var index = expensesCtrl.expenses.indexOf(expense);
            expensesCtrl.expenses.splice(index, 1);
          } else {
            //TODO: put message here
          }
        });
    };

    this.addExpense = function(){
      var data = expensesCtrl.currentExpense;
      data['format'] = 'json';
      $http.post('/api/expenses/', data).
        success(function(data, status){
          if(status == 201){
            expensesCtrl.expenses.push(expensesCtrl.currentExpense);
            expensesCtrl.currentExpense = {};
          } else {
            //TODO: put message here
          }
        });
    };

    // makes the basic steps for editing an expense
    this.startEditing = function(expense){
      expensesCtrl.editing = expensesCtrl.expenses.indexOf(expense);
      expensesCtrl.oldExpense = angular.copy(expense);
    };

    this.saveExpense = function(index) {
      if(expensesCtrl.editing !== false){
        expensesCtrl.editing = false;
      }
    };

    this.cancelEdit = function(index){
      if(expensesCtrl.editing !== false){
        expensesCtrl.expenses[expensesCtrl.editing] = expensesCtrl.oldExpense;
        expensesCtrl.editing = false;
      }
    };

  }]);

  app.controller('ReportsController', function(){

  });
})();
