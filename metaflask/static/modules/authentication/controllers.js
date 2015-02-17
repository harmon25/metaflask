'use strict';

angular.module('Authentication')

.controller('LoginController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',  
    function ($scope, $rootScope, $location, AuthenticationService) {
        // reset login status
        AuthenticationService.ClearCredentials();

        $scope.login = function () {
            $scope.dataLoading = true;
            AuthenticationService.Login($scope.username, $scope.password, function (response) {
                if (response.success) {
                    var auth_user = response.username
                    var auth_role = response.role
                    AuthenticationService.SetCredentials(auth_user, $scope.password, auth_role);
                    $location.path('/');
                } else {
                    $scope.dataLoading = false;
                    $scope.error = true;
                    $scope.error_msg = response.message;
                    
                }
            });
        };
    }]);