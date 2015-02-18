'use strict';

// declare modules
angular.module('Authentication', ['lumx']);
angular.module('Home', ['lumx']);

angular.module('BasicHttpAuthExample', [
    'Authentication',
    'Home',
    'ngRoute',
    'ngCookies',
    'ngMaterial',
    'lumx'
])

.config(['$routeProvider', function ($routeProvider) {

    $routeProvider
        .when('/login', {
            controller: 'LoginController',
            templateUrl: '/views/login',
            hideMenus: true
        })

        .when('/', {
            controller: 'HomeController',
            templateUrl: '/views/home'
        })

        .when('/about', {
            controller: 'HomeController',
            templateUrl: '/views/home'
        })

        .when('/private', {
            controller: 'HomeController',
            templateUrl: '/views/home'
        })

        .otherwise({ redirectTo: '/login' });
}])

.run(['$rootScope', '$location', '$cookieStore', '$http',
    function ($rootScope, $location, $cookieStore, $http) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
        }

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in
            if ($location.path() !== '/login' && !$rootScope.globals.currentUser) {
                $location.path('/login');
            }
        });
    }]);