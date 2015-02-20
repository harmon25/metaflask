'use strict';

angular.module('Authentication')

.factory('AuthenticationService',
    ['$http', '$cookieStore', '$rootScope', 
    function ($http, $cookieStore, $rootScope) {
        var service = {};

        service.Login = function (username, password, callback) {

            /* Dummy authentication for testing, uses $timeout to simulate api call
             ----------------------------------------------*/
            //$timeout(function () {
            //    var response = { success: username === 'test' && password === 'test' };
            //    if (!response.success) {
            //        response.message = 'Username or password is incorrect';
            //    }
            //    callback(response);
            //}, 1000);


            /* Use this for real authentication
             ----------------------------------------------*/
            $http.post('/auth', { username: username, password: password })
                .success(function (response, headers) {
                    callback(response);
                    console.log(response);
                    console.log(headers);
                }).
                error(function (response, headers){
                    callback(response);
                    console.log(response);
                    console.log(headers);
                });

        };

        service.SetToken = function (token) {

            $rootScope.globals = {
                currentUser: {
                    token: token
                }
            };

            $http.defaults.headers.common['Authorization'] = 'Bearer ' + token; // jshint ignore:line
            $cookieStore.put('globals', $rootScope.globals);
        };

        service.ClearToken = function () {
            $rootScope.globals = {};
            $cookieStore.remove('globals');
            $http.defaults.headers.common.Authorization = 'Basic ';
        };

        return service;
    }])

