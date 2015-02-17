'use strict';


angular.module('Home')

.controller('LayoutController',
    ['$scope','$rootScope','$mdSidenav', 
    function ($scope, $rootScope, $mdSidenav) {
    	  $scope.toggleSidenav = function(menuId) {
    	  $mdSidenav(menuId).toggle();}

    }]);


angular.module('Home')

.controller('HomeController',
    ['$scope','$rootScope',
    function ($scope, $rootScope) {
    	$scope.username = $rootScope.globals.currentUser.username

    }]);


