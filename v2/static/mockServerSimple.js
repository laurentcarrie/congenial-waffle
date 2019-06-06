function ServerSideDatasource(fakeServer) {
    this.fakeServer = fakeServer;
}

ServerSideDatasource.prototype.getRows = function(params) {
    console.log('ServerSideDatasource.getRows: params = ', params);

    var request = params.request;

    // if we are on the top level, then group keys will be [],
    // if we are on the second level, then group keys will be like ['United States']
    var groupKeys = request.groupKeys;
    var doingTopLevel = groupKeys.length === 0;

    if (doingTopLevel) {
        this.fakeServer.getTopLevelCarMakerList(successCallback, request);
    } else {
        var CarMaker = request.groupKeys[0];
        this.fakeServer.getCarMakerDetails(successCallback, CarMaker, request);
    }

    function successCallback(resultForGrid, lastRow) {
        params.successCallback(resultForGrid, lastRow);
    }
};

function FakeServer(allData) {
    this.initData(allData);
}

FakeServer.prototype.initData = function(allData) {
    var topLevelCarMakerGroups = [];
    var bottomLevelCarMakerDetails = {}; // will be a map of [CarMaker name => records]

    allData.forEach( function(dataItem) {
        // get CarMaker this item is for
        var CarMaker = dataItem.CarMaker;

        // get the top level group for this CarMaker
        var childrenThisCarMaker = bottomLevelCarMakerDetails[CarMaker];
        var groupThisCarMaker = _.find(topLevelCarMakerGroups, {CarMaker: CarMaker});
        if (!childrenThisCarMaker) {
            // no group exists yet, so create it
            childrenThisCarMaker = [];
            bottomLevelCarMakerDetails[CarMaker] = childrenThisCarMaker;

            // add a group to the top level
            groupThisCarMaker = {CarMaker: CarMaker, gold: 0, silver: 0, bronze: 0};
            topLevelCarMakerGroups.push(groupThisCarMaker);
        }

        // add this record to the county group
        childrenThisCarMaker.push(dataItem);

        // increment the group sums
        groupThisCarMaker.gold += dataItem.gold;
        groupThisCarMaker.silver += dataItem.silver;
        groupThisCarMaker.bronze += dataItem.bronze;
    });

    this.topLevelCarMakerGroups = topLevelCarMakerGroups;
    this.bottomLevelCarMakerDetails = bottomLevelCarMakerDetails;

    this.topLevelCarMakerGroups.sort(function(a,b) { return a.CarMaker < b.CarMaker ? -1 : 1; });
};

FakeServer.prototype.sortList = function(data, sortModel) {
    var sortPresent = sortModel && sortModel.length > 0;
    if (!sortPresent) {
        return data;
    }
    // do an in memory sort of the data, across all the fields
    var resultOfSort = data.slice();
    resultOfSort.sort(function(a,b) {
        for (var k = 0; k<sortModel.length; k++) {
            var sortColModel = sortModel[k];
            var valueA = a[sortColModel.colId];
            var valueB = b[sortColModel.colId];
            // this filter didn't find a difference, move onto the next one
            if (valueA==valueB) {
                continue;
            }
            var sortDirection = sortColModel.sort === 'asc' ? 1 : -1;
            if (valueA > valueB) {
                return sortDirection;
            } else {
                return sortDirection * -1;
            }
        }
        // no filters found a difference
        return 0;
    });
    return resultOfSort;
};

// when looking for the top list, always return back the full list of countries
FakeServer.prototype.getTopLevelCarMakerList = function(callback, request) {

    var lastRow = this.getLastRowResult(this.topLevelCarMakerGroups, request);
    var rowData = this.getBlockFromResult(this.topLevelCarMakerGroups, request);

    // put the response into a timeout, so it looks like an async call from a server
    setTimeout( function() {
        callback(rowData, lastRow);
    }, 1000);
};

FakeServer.prototype.getCarMakerDetails = function(callback, CarMaker, request) {

    var CarMakerDetails = this.bottomLevelCarMakerDetails[CarMaker];

    var CarMakerDetailsSorted = this.sortList(CarMakerDetails, request.sortModel);

    var lastRow = this.getLastRowResult(CarMakerDetailsSorted, request);
    var rowData = this.getBlockFromResult(CarMakerDetailsSorted, request);

    // put the response into a timeout, so it looks like an async call from a server
    setTimeout( function() {
        callback(rowData, lastRow);
    }, 1000);
};

FakeServer.prototype.getBlockFromResult = function(data, request) {
    return data.slice(request.startRow, request.endRow);
};

FakeServer.prototype.getLastRowResult = function(result, request) {
    // we mimic finding the last row. if the request exceeds the length of the
    // list, then we assume the last row is found. this would be similar to hitting
    // a database, where we have gone past the last row.
    var lastRowFound = (result.length <= request.endRow);
    var lastRow = lastRowFound ? result.length : null;
    return lastRow;
};