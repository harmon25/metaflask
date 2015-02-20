'use strict';

angular.module('Authentication')

.controller('LoginController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService', 'LxNotificationService', 
    function ($scope, $rootScope, $location, AuthenticationService, LxNotificationService) {
        // reset login status
        AuthenticationService.ClearToken();

        $scope.login = function () {
            $scope.dataLoading = true;
            AuthenticationService.Login($scope.username, $scope.password, function (response) {
                if (response.success) {
                    $scope.dataLoading = false;
                    LxNotificationService.warning(response.message);
                } else {
                      $location.path('/');
                    AuthenticationService.SetToken(response.token);
                    
                }
            });
        };




    }]);