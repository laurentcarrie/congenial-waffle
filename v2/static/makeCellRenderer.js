// function to act as a class
function MakeCellRenderer () {}

// gets called once before the renderer is used
MakeCellRenderer.prototype.init = function(params) {
    // create the cell
    this.eGui = document.createElement('div');
    //this.eGui.innerHTML = '<span class="my-css-class"><button class="btn-simple">Push Me</button><span class="my-value"></span></span>';
    this.eGui.innerHTML = '<span color="red"><span class="my-value"></span></span>';

    // get references to the elements we want
    //this.eButton = this.eGui.querySelector('.btn-simple');
    this.eValue = this.eGui.querySelector('.my-value');

    // set value into cell
    if (params.value == 'Renault') {
        country = 'fr'
    }    
    else if (params.value == 'Peugeot') {
        country = 'fr'
    }    
    else if (params.value == 'Toyota') {
        country = 'jp'
    }    
    else  {
        country = 'de'
    }


    this.eValue.innerHTML = '<span >' + '<img class="flag" border="0" with="15" height="10" src="https://flags.fmcdn.net/data/flags/mini/' + country + '.png">                            ' +
        (params.valueFormatted ? params.valueFormatted : params.value) + '</span>';

    // add event listener to button
    //this.eventListener = function() {
      //  console.log('button was clicked!!');
    //};
    // this.eButton.addEventListener('click', this.eventListener);
};

// gets called once when grid ready to insert the element
MakeCellRenderer.prototype.getGui = function() {
    return this.eGui;
};

// gets called whenever the user gets the cell to refresh
MakeCellRenderer.prototype.refresh = function(params) {
    // set value into cell again
    this.eValue.innerHTML = params.valueFormatted ? params.valueFormatted : params.value;
    // return true to tell the grid we refreshed successfully
    return true;
};

// gets called when the cell is removed from the grid
MakeCellRenderer.prototype.destroy = function() {
    // do cleanup, remove event listener from button
   // this.eButton.removeEventListener('click', this.eventListener);
};