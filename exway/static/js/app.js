(function() {
  var app = angular.module('exway', []).
    config(function($httpProvider, $interpolateProvider) {
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
    });
})();
