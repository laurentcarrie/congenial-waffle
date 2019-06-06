var map = function () {

    var key = this.model ;
    var value = this.price ;
    emit(key, this.price) ;

};


var reduce = function (key, values) {

    var reducedObject = {
        model: key,
        total_price: 0,
    };

    double sum=0 ;
    for (var index=0;index<values.length;++index) {
        sum += values[index]
    }

    return sum ;

};

var reduce2 = function (key, prices) {
    return Array.sum(prices);
}

db.cars.mapReduce(map, reduce, {out: "totals"});

db.totals.find({})

