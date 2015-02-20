'use strict';

// declare modules
angular.module('Authentication', []);
angular.module('Home', []);

angular.module('BasicHttpAuthExample', [
    'Authentication',
    'Home',
    'ngRoute',
    'ngCookies',
    'ngResource',
    'ngMaterial',
    'lumx'
])

.config(['$routeProvider', function ($routeProvider) {

    $routeProvider
        .when('/login', {
            controller: 'LoginController',
            templateUrl: '/views/login',
            access: { roles: 'all' }
        })

        .when('/', {
            controller: 'HomeController',
            templateUrl: '/views/home',
            access: { roles: ['user'] }
        })

        .when('/about', {
            controller: 'HomeController',
            templateUrl: '/views/about',
            access: { roles: ['user'] }
        })

        .when('/private', {
            controller: 'HomeController',
            templateUrl: '/views/home',
            access: { roles: ['admin'] }
        })

        .otherwise({ redirectTo: '/login' });
}])

.run(['$rootScope', '$location', '$cookieStore', '$http',
    function ($rootScope, $location, $cookieStore, $http) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'Bearer ' + $rootScope.globals.currentUser.token; // jshint ignore:line
          }

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in
            if ($location.path() !== '/login' && !$rootScope.globals.currentUser.token) {
                $location.path('/login');
            }
        });
    }]);