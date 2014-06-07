(function(){
  var app = angular.module('reports', []);

  app.controller('ReportsController', ['$log', '$http', function($log, $http){
    this.weeklyExpensesSet = [
      {
        "initialDate": "2014-06-01",
        "finalDate": "2014-06-07",
        "expenses": [
          {
            "id": 1, 
            "description": "This is a fake expense in order to test the api", 
            "amount": "337", 
            "date": "2014-06-06", 
            "time": "10:50:00", 
            "comment": "this is an api test", 
            "created_on": "2014-06-07T18:18:52.971Z", 
            "user": "admin"
          }],
        "total": "337",
        "average": "48.14"
      }];
  }]);

})();
