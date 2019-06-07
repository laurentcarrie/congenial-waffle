

var columnDefs = [

  // these are the row groups, so they are all hidden (they are shown in the group column)

      {headerName: 'index', field: 'index'},
      {headerName: 'make', field: 'make',rowGroup:true,type:'make'},
      {headerName: 'model', field: 'model'},
      {headerName: 'price', field: 'price',type:'money'},

];

let gridOptions = {
  columnTypes: {
    dimension: {
      enableRowGroup: true,
      enablePivot: true,
    },
    measure: {
      width: 150,
      aggFunc: 'sum',
      enableValue: true,
      cellClass: 'number',
      valueFormatter: numberCellFormatter,
      cellRenderer:'agAnimateShowChangeCellRenderer',
      allowedAggFuncs: ['avg','sum','min','max'],
      cellClassRules: {'negative': 'x < 0'}
    },
    money: {
      width: 150,
      aggFunc: 'sum',
      enableValue: true,
      cellClass: 'number',
      valueFormatter: moneyCellFormatter,
      cellRenderer:MoneyCellRenderer,
      allowedAggFuncs: ['avg','sum','min','max'],
      cellClassRules: {'negative': 'x < 0'}
    },
    make: {
      width: 150,
      enableValue: true,
      cellClass: 'string',
     // valueFormatter: moneyCellFormatter,
      cellRenderer:MakeCellRenderer
    }
  },

  enableSorting: true,
  enableFilter: true,
  columnDefs: columnDefs,
  enableColResize: true,
  rowModelType: 'enterprise',
  cacheBlockSize: 100,
  rowGroupPanelShow: 'always',
  pivotPanelShow: 'always',
  suppressAggFuncInHeader: true,
  animateRows: false
};

function EnterpriseDatasource() {}

EnterpriseDatasource.prototype.getRows = function (params) {
  let jsonRequest = JSON.stringify(params.request, null, 2);
  console.log(jsonRequest);

  let httpRequest = new XMLHttpRequest();
  httpRequest.open('POST', '/getRows');
  httpRequest.setRequestHeader("Content-type", "application/json");
  httpRequest.send(jsonRequest);
  httpRequest.onreadystatechange = () => {
    if (httpRequest.readyState === 4 && httpRequest.status === 200) {
      let result = JSON.parse(httpRequest.responseText);
      params.successCallback(result.data, result.lastRow);

      updateSecondaryColumns(params.request, result);
    }
  };
};

// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', function () {
  let gridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(gridDiv, gridOptions);
  gridOptions.api.setEnterpriseDatasource(new EnterpriseDatasource());
});

let updateSecondaryColumns = function (request, result) {
  let valueCols = request.valueCols;
  if (request.pivotMode && request.pivotCols.length > 0) {
    let secondaryColDefs = createSecondaryColumns(result.secondaryColumnFields, valueCols);
    gridOptions.columnApi.setSecondaryColumns(secondaryColDefs);
  } else {
    gridOptions.columnApi.setSecondaryColumns([]);
  }
};

let createSecondaryColumns = function (fields, valueCols) {
  let secondaryCols = [];

  function addColDef(colId, parts, res) {
    if (parts.length === 0) return [];

    let first = parts.shift();
    let existing = res.find(r => r.groupId === first);

    if (existing) {
      existing['children'] = addColDef(colId, parts, existing.children);
    } else {
      let colDef = {};
      let isGroup = parts.length > 0;
      if(isGroup) {
        colDef['groupId'] = first;
        colDef['headerName'] = first;
      } else {
        let valueCol = valueCols.find(r => r.field === first);

        colDef['colId'] = colId;
        colDef['headerName'] =  valueCol.displayName;
        colDef['field'] = colId;
        colDef['type'] = 'measure';
      }

      let children = addColDef(colId, parts, []);
      children.length > 0 ? colDef['children'] = children : null;

      res.push(colDef);
    }

    return res;
  }

  fields.sort();
  fields.forEach(field => addColDef(field, field.split('_'), secondaryCols));
  return secondaryCols;
};

function numberCellFormatter(params) {
  let formattedNumber = Math.floor(Math.abs(params.value)).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
  return params.value < 0 ? '(' + formattedNumber + ')' : formattedNumber;
};

function moneyCellFormatter(params) {
  let formattedNumber = Math.floor(params.value).toString() + ' euros';
  return formattedNumber;
};