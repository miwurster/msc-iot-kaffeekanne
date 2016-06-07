angular.module('starter.services', [])

.filter('datefilter', function(){
  return function(value) {
    var v = new Date(value * 1000);
    return v.toLocaleString();
  };
})

.factory('Coffee', function($http, $q) {

  return {
    all: function() {
      var deferred = $q.defer();
      $http.get('https://kaffee-api.eu-gb.mybluemix.net/state')
        .then(function successCallback(response) {
            deferred.resolve(response);
        }, function errorCallback(response) {
            deferred.reject(response);
        });
      return deferred.promise;
    }
  };
});
