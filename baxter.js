




var app = angular.module('baxterApp', []);

app.controller('baxterCtrl', ['$scope',
	function($scope){

		$scope.loadView = function(viewName){
			$scope.view = viewName;
		}
		
	}
]);