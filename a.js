var map = function() {emit(this.model,this.price);};
var reduce = function(key,prices) {

    return Array.sum(prices) ;
};

db.cars.mapReduce(map,reduce,{ out: "totals" });

db.totals.find({})

