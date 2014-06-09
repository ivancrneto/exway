(function(){
  var app = angular.module('reports', []);

  app.controller('ReportsController', ['$log', '$http', function($log, $http){
    var reportsCtrl = this;

    this.weeklyExpensesSet = [];

    $http.get('/api/reports/weekly').success(function(data){
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
