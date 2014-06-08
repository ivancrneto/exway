(function(){
  var app = angular.module('expenses', ['ngCookies', 'ui-rangeSlider']);

  // configure csrf token for app because django requires it for safety
  app.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;

  });

  app.controller('ExpensesController', ['$log', '$http', '$scope', function($log, $http, $scope){

    $scope.demo1 = {
        min: 0,
        max: 1000
    };

    var expensesCtrl = this;

    // this controls if the user is editing any table row, using expense id as key
    this.editing = {};

    // this keeps the old expense for cases where the user cancels editing,
    // using the expense id as key
    this.oldExpenses = {};

    // currentExpense keeps the data from the adding form
    this.currentExpense = {};

    // this is the list of all expenses that will come from server
    this.expenses = [];

    // get expenses data from api and fill expenses array
    $http.get('/api/expenses/', {format: 'json'}).success(function(data){
      for(i in data){
        data[i]['amount'] = parseFloat(data[i]['amount']);
        expensesCtrl.expenses.push(data[i]);

        // initializing editing and oldExpenses arrays with the ids of the expenses
        expensesCtrl.editing[data.id] = false;
        expensesCtrl.oldExpenses[data.id] = false;
      }
    });

    this.hideForm = function(){
      expensesCtrl.currentExpense = {};
      expensesCtrl.showForm = false;
    };

    // method for adding a new expense
    this.addExpense = function(){
      var data = expensesCtrl.currentExpense;
      $http.post('/api/expenses/', data).
        success(function(data, status){
          if(status == 201){
            data['amount'] = parseFloat(data['amount']);
            expensesCtrl.expenses.push(data);
            expensesCtrl.currentExpense = {};
          } else {
            //TODO: put message here
          }
        });
    };

    // method for deleting a expense using the button in table row
    this.deleteExpense = function(expense){
      var url = '/api/expenses/' + expense.id + '/';
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

    // makes the basic steps for editing an expense
    this.startEditing = function(expense){
      expensesCtrl.editing[expense.id] = expensesCtrl.expenses.indexOf(expense);
      expensesCtrl.oldExpenses[expense.id] = angular.copy(expense);
    };

    // saves an expense after editing
    this.saveExpense = function(expense) {
      if(expensesCtrl.editing[expense.id] !== false){
        var data = angular.copy(expensesCtrl.expenses[expensesCtrl.editing[expense.id]]);
        // sets the model to old one first
        expensesCtrl.expenses[expensesCtrl.editing[expense.id]] = expensesCtrl.oldExpenses[expense.id];

        var url = '/api/expenses/' + data.id + '/';
        $http.put(url, data).
          success(function(data, status){
            if(status == 200){
              data['amount'] = parseFloat(data['amount']);
              expensesCtrl.expenses[expensesCtrl.editing[expense.id]] = data;
            } else {
              //TODO: put a message here
            }
          }).
          then(function() {
            expensesCtrl.editing[expense.id] = false;
          });
      }
    };

    // cancels expense editing
    this.cancelEdit = function(expense){

      if(expensesCtrl.editing[expense.id] !== false){
        expensesCtrl.expenses[expensesCtrl.editing[expense.id]] = expensesCtrl.oldExpenses[expense.id];
        expensesCtrl.editing[expense.id] = false;
      }
    };

  }]);

  app.controller('ReportsController', function(){

  });
})();
