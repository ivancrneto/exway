(function(){
  var app = angular.module('expenses', ['ngCookies', 'ui-rangeSlider']);

  // configure csrf token for app because django requires it for safety
  app.run(function($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
  });

  app.controller('ExpensesController', ['$log', '$http', '$scope', '$filter', function($log, $http, $scope, $filter){

    var expensesCtrl = this;

		// model containing the values for the expenses filter
    var expensesFilterDefault = {
        amountMin: 0,
        amountMax: 1000,
    };
    var expensesFilter = angular.copy(expensesFilterDefault);

		// model containing the values for the expenses filter
    this.getAmounts = function() {
      $http.get('/api/expenses/amounts/').success(function(data){
        expensesCtrl.expensesFilterDefault = {
          amountMin: parseFloat(data.min),
          amountMax: parseFloat(data.max),
        };
        expensesCtrl.expensesFilter = angular.copy(expensesCtrl.expensesFilterDefault);
      });
    };
    this.getAmounts();

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
		this.getExpenses = function(params){
			expensesCtrl.expenses = [];
			$scope.expensesPromise = $http.get('/api/expenses/', {params: params});
      $scope.expensesPromise.success(function(data){
				for(i in data){
					data[i]['amount'] = parseFloat(data[i]['amount']);
					data[i]['date'] = moment.utc(data[i]['date']).format('MM/DD/YYYY');
          data[i]['time'] = $filter('time')(data[i]['time'], 'hh:mm A');
					expensesCtrl.expenses.push(data[i]);

					// initializing editing and oldExpenses arrays with the ids of the expenses
					expensesCtrl.editing[data.id] = false;
					expensesCtrl.oldExpenses[data.id] = false;
				}
			});
		};

		this.applyFilter = function(){
      var params = angular.copy(expensesCtrl.expensesFilter);
      if(params.dateFrom){
        params.dateFrom = moment.utc(new Date(params.dateFrom));
        params.dateFrom = params.dateFrom.toISOString().split('T')[0];
      }
      if(params.dateTo) {
        params.dateTo = moment.utc(new Date(params.dateTo));
        params.dateTo = params.dateTo.toISOString().split('T')[0];
      }
			this.getExpenses(params);
		};

		this.clearFilter = function(){
			this.expensesFilter = angular.copy(this.expensesFilterDefault);
			this.applyFilter();
		};

    this.hideForm = function(){
      expensesCtrl.currentExpense = {};
      expensesCtrl.showForm = false;
      $scope.submitted = false;
    };

    // method for adding a new expense
    this.addExpense = function(){
      var data = angular.copy(expensesCtrl.currentExpense);
      data.date = moment.utc(new Date(data.date));
      data.date = data.date.toISOString().split('T')[0];
      $http.post('/api/expenses/', data).
        success(function(data, status){
          if(status == 201){
            data['amount'] = parseFloat(data['amount']);
            data['date'] = moment.utc(data['date']).format('MM/DD/YYYY');
            data['time'] = $filter('time')(data['time'], 'hh:mm A');
            expensesCtrl.expenses.push(data);
            expensesCtrl.currentExpense = {};

            // update amounts filter
            expensesCtrl.getAmounts();
            expensesCtrl.hideForm();
          }
        }).
        error(function(data, status) {
          expensesCtrl.currentExpense.errors = ['An unexpected error occurred. Please try again.'];
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

        data.date = moment.utc(new Date(data.date));
        data.date = data.date.toISOString().split('T')[0];
        var url = '/api/expenses/' + data.id + '/';
        $http.put(url, data).
          success(function(data, status){
            if(status == 200){
              data['amount'] = parseFloat(data['amount']);
              data['date'] = moment.utc(data['date']).format('MM/DD/YYYY');
              data['time'] = $filter('time')(data['time'], 'hh:mm A');
              expensesCtrl.expenses[expensesCtrl.editing[expense.id]] = data;
              // update amounts filter
              expensesCtrl.getAmounts();
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

    // method for configuring expenses module datepickers
    this.initDatePickers = function(){
      $('#dateFromFilter').datetimepicker({pickTime: false});
      $("#dateFromFilter").on("dp.show dp.change", function (e) {
        $scope.$apply(function() {
          expensesCtrl.expensesFilter.dateFrom = e.date.format('MM/DD/YYYY');
        });
      });

      $('#dateToFilter').datetimepicker({pickTime: false});
      $("#dateToFilter").on("dp.show dp.change", function (e) {
        $scope.$apply(function() {
          expensesCtrl.expensesFilter.dateTo = e.date.format('MM/DD/YYYY');
        });
      });

      $('#currentExpenseDate').datetimepicker({pickTime: false});
      $("#currentExpenseDate").on("dp.show dp.change", function (e) {
        $scope.$apply(function() {
          expensesCtrl.currentExpense.date = e.date.format('MM/DD/YYYY');
        });
      });

      $('#currentExpenseTime').datetimepicker({pickDate: false});
      $("#currentExpenseTime").on("dp.show dp.change", function (e) {
        $scope.$apply(function() {
          expensesCtrl.currentExpense.time = e.date.format('hh:mm A');
        });
      });
    };

		this.getExpenses({});
    this.initDatePickers();
  }]).directive('ngDateEdit', function($log) {
    return {
      restrict: 'A',
      link: function(scope, element, attributes) {
        element.datetimepicker({pickTime: false});

        element.bind("dp.show dp.change", function (e) {
          scope.$apply(function(elem) {
            elem.expense.date = e.date.format('MM/DD/YYYY');
          });
        });
      }
    }
  }).directive('ngTimeEdit', function($log) {
    return {
      restrict: 'A',
      link: function(scope, element, attributes) {
        element.datetimepicker({pickDate: false});

        element.bind("dp.show dp.change", function (e) {
          scope.$apply(function(elem) {
            elem.expense.time = e.date.format('hh:mm A');
          });
        });
      }
    }
  });

})();
