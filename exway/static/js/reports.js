(function(){
  var app = angular.module('reports', []);

  app.controller('ReportsController', ['$log', '$http', '$scope', function($log, $http, $scope){
    var reportsCtrl = this;

    this.weeklyExpensesSet = [];

    $scope.reportPromise = $http.get('/api/reports/weekly');
    $scope.reportPromise.success(function(data){
      for(var i in data){
        for(var j in data[i].expenses) {
          var expense = data[i].expenses[j];

          expense['amount'] = parseFloat(expense['amount']);
        }
        reportsCtrl.weeklyExpensesSet.push(data[i]);
      }
    });
  }]);

})();
