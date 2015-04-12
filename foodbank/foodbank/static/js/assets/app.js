var checkbox = {
	restaurant: true,
	food: false,
	query: false
};

var slider = {
  	rating: 4,
  	distance: 160
};

var search = {text: ""};

angular.module('myApp', ['ngMaterial'])
.controller('AppCtrl', function($scope, $mdDialog) {

  $scope.checkbox = checkbox;
  $scope.slider = slider;
  $scope.search = search;

  $scope.showAdvanced = function(ev) {
    $mdDialog.show({
      templateUrl: '/static/js/dialog.template.html',
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
});