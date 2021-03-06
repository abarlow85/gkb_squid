angular.module('bikeSelect').service('boolService', function(){
	var select = {
		"bike": false,
		"component": false,
		"other":false,
		"product":{
			status: false
		}
	};

	var service = {};

	service.toggleSelect = function(item){
		for (var part in select){
			if (part == item && !select[item]){
				if (part == 'product'){
					select[item]['status'] = true;
				}else{
					select[item] = true;
				}
			}else{
				if (part == 'product'){
					select[part]['status'] = false;
					if (select[part]['type']){select[part]['type'] = ''}
				}else{
					select[part] = false;
				};
			}
		}
	};

	service.insertNewProduct = function(pType){
		select.product.status = true;
		selec.product.type = pType;
	}

	service.returnSelect = function(item){
		return select[item];
	};

	return service;
});
