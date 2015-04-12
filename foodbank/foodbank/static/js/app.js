var checkbox = {
	restaurant: true,
	food: false,
	query: false
};

var slider = {
  rating: 4,
  distance: 50
};

var pos = {
  lat: 0,
  lon: 0
};

angular.module('myApp', ['ngMaterial'])
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
})
.controller('AppCtrl', function($scope, $mdDialog) {

  $scope.checkbox = checkbox;
  $scope.slider = slider;
  $scope.pos = pos;

  $scope.init = function() {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        $scope.pos.lat = position.coords.latitude;
        $scope.pos.lon = position.coords.longitude;
      }
    );
  }

  $scope.showAdvanced = function(ev) {
    $mdDialog.show({
      templateUrl: '/static/dialog.template.html',
      targetEvent: ev,
    })
  };

  $scope.onOtherChange = function() {
  	if ($scope.checkbox.food === false
  	 && $scope.checkbox.restaurant === false)
  		$scope.checkbox.query = true;
  	else $scope.checkbox.query = false;
  }

  $scope.onQueryChange = function() {
  	$scope.checkbox.food = false;
  	$scope.checkbox.restaurant = false;
  }

  function refresh() {}
});