
 
     
    var pos = {
      lat: 23.7630794081,
      lon: 90.3613094203
    };
     
    var dest = {
      lat: 23.7630794081,
      lon: 90.3613094203
    };
     
    angular.module('myApp', ['ngMaterial'])
    .config(function($interpolateProvider){
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    })
    .controller('AppCtrl', function($scope, $mdDialog) {
     
      
      
      $scope.pos = pos;
      $scope.dest = dest;
      $scope.selectedIndex = 100;
     
      var directionsService = new google.maps.DirectionsService();
      directionsDisplay = new google.maps.DirectionsRenderer();
      var source = new google.maps.LatLng(pos.lat, pos.lon);
      var mapOptions = {
        zoom:13,
        center: source
      };
      var map = new google.maps.Map(document.getElementById('map'), mapOptions);
      directionsDisplay.setMap(map);
     
     
      $scope.init = function() {
        navigator.geolocation.getCurrentPosition(
          function(position) {
            $scope.pos.lat = position.coords.latitude;
            $scope.pos.lon = position.coords.longitude;
          }
        );
      };
     
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
      };
     
      $scope.onQueryChange = function() {
            $scope.checkbox.food = false;
            $scope.checkbox.restaurant = false;
      };
     
      $scope.reload = function() {
         
     
        var start = source;
        var end = new google.maps.LatLng(dest.lat, dest.lon);
        var request = {
          origin:start,
          destination:end,
          travelMode: google.maps.TravelMode.DRIVING
        };
     
        directionsService.route(request, function(response, status) {
          if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
          }
        });
      };
     
      function refresh() {}
    });

