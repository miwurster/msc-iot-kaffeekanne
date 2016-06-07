angular.module('starter.controllers', [])

.controller('DashCtrl', function($log, $scope, Coffee) {

  $scope.coffee = {};

  Coffee.all().then(function(response) {
    $log.debug(JSON.stringify(response.data));
    $scope.coffee = response.data;
  }).catch(function(response){
    $log.error(JSON.stringify(response));
  });
});
