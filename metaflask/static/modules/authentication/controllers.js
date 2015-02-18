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
                    var auth_roles = response.roles
                    AuthenticationService.SetCredentials(auth_user, $scope.password, auth_roles);
                    $location.path('/');
                } else {
                    $scope.dataLoading = false;
                    $scope.error = true;
                    $scope.error_msg = response.message;
                    
                }
            });
        };
    }]);