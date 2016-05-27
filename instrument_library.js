var app = angular.module('instrumentLibraryApp', []);

app.controller('instrumentLibraryCtrl', ['$scope', '$http',
	function($scope, $http){
		
		console.log('i am running')

		$scope.View = "A";

	}
]);

