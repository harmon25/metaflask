'use strict';


angular.module('Home')

.controller('LayoutController',
    ['$scope','$rootScope','$mdSidenav','LxNotificationService',
    function ($scope, $rootScope, $mdSidenav, LxNotificationService) {
    	  $scope.toggleSidenav = function(menuId) {
    	  $mdSidenav(menuId).toggle();};

   $scope.notify = function(){
        LxNotificationService.warning('Lorem Ipsum');
          };
    

    }]);


angular.module('Home')

.controller('HomeController',
    ['$scope','$rootScope',
    function ($scope, $rootScope) {
    	$scope.username = $rootScope.globals.currentUser.username

    }]);


