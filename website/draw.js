/*jslint white: true, browser: true, undef: true, nomen: true, eqeqeq: true, plusplus: false, bitwise: true, regexp: true, strict: true, newcap: true, immed: true, maxerr: 14 */
/*global window: false */

/* reveal module-pattern */

/* enable strict mode */
"use strict";



// define redips object container
var redips = {};
var row = 0;
var col = 0;
var draw_erase = 1;

// script configuration
redips.configuration = function () {
	redips.color = 'black'; // default colour
	redips.columns = network_size; // columns (X)
	redips.rows = network_size; // (Y)
	redips.mouse = 0; // pressed mouse button (1 when left button is pressed)
	redips.div = document.getElementById('drawing-table'); // drawing container reference

    
};

// script initialization
redips.init = function () {
	// apply configuration
	redips.configuration();
	// create HTML table
	redips.tableCreate();
	// attach event listener to every TD
//    $("td").click(function(){
//        var col = $(this).attr("class");
//        var row = $(this).parent().attr("class");
//        alert(col);
//    });
	redips.tdEvents();
	// disable drag event for IE
	document.body.ondragstart = function (e) {
		return false;
	};
	// attach onmousedown document level
	document.onmousedown = function (e) {
		// define event
		var evt = e || window.event;
		// needed for FF to disable dragging	
		if (evt.preventDefault) {
			e.preventDefault();
		}
		// set pressed mouse button 
		if (evt.which) {
			redips.mouse = evt.which;
		}
		else {
			redips.mouse = evt.button;
		}
	};
	// attach onmouseup document level
	document.onmouseup = function (e) {
		redips.mouse = 0;
	};
};


// create table HTML and set to the DIV container
redips.tableCreate = function () {
	var tbl = '', // initialize table string
		div, // reference to the drawing table
		i, j; // local variables
	// open loops to create table rows and table cells
	for (i = 0; i < redips.rows; i++) {
		tbl = tbl + '<TR class='+i+'>';
		for (j = 0; j < redips.columns; j++) {
			tbl = tbl + '<TD class='+j+'></TD>';
		}
		tbl = tbl + '</TR>\n';
	}
	// set table HTML to the DIV element
	redips.div.innerHTML = '<TABLE cellspacing="0" cellpadding="0">' + tbl + '</TABLE>';
};


// attach event listener to every TD
redips.tdEvents = function () {
	// collect TD elements from the drawing-table DIV
	var td = redips.div.getElementsByTagName('td'),
		i;
	// loop through every TD and attach onmouseover event listener
	for (i = 0; i < td.length; i++) {
		td[i].onmouseover = redips.mouseover;
		td[i].onmousedown = redips.mousedown;
	}
};

// set color (input parameter is TD reference)
redips.setColor = function (obj) {
    // set table reference (first child of DIV container)
//    var tbl = redips.div.firstChild;
    if(draw_erase==1){draw_erase=-1;}
    else{draw_erase=1;}

    // set the selected colour
    redips.color = obj.style.backgroundColor;
    // set table border colour (selected colour)
    //.tbl.style.borderColor = redips.color;
};

// TD onmouseover event handler
redips.mouseover = function () {
	if (redips.mouse === 1) {
		this.style.backgroundColor = redips.color;
        col = parseInt($(this).attr("class"));
        row = parseInt($(this).parent().attr("class"));
        $("#coordinates").text(row+","+col);
        network_state[row*network_size+col]=draw_erase;
        $("#network").text(network_state);
    }
};


// TD onmousedown event handler
redips.mousedown = function () {
    if(cur_memory_index==memories.length){
        this.style.backgroundColor = redips.color;
        col = parseInt($(this).attr("class"));
        row = parseInt($(this).parent().attr("class"));
        $("#coordinates").text(row+","+col);
        network_state[row*network_size+col]=draw_erase;
        $("#network").text(network_state);
    }
    else{
        var network_state = new Array(network_size*network_size).fill(-1);
        cur_memory_index=memories.length;
        update_visualization();
    }
	
};


// attach onload event listener
if (window.addEventListener) {
	window.addEventListener('load', redips.init, false);
}
else if (window.attachEvent) {
	window.attachEvent('onload', redips.init);
}

function update_visualization(){

    for (var i = 0; i < network_size; i++) {
		for(var j = 0; j < network_size; j++){
            if(network_state[i*network_size+j]==1){
                $("tr."+i).children("td."+j).css('background-color', 'black');
            }
            else{
                $("tr."+i).children("td."+j).css('background-color', 'white');
            }
        }
    }
}
function save_image(){
    var source = document.getElementById('drawing-table').childNodes;
    var destination = document.getElementById('tableB');
    var copy = source.cloneNode(true);
    copy.setAttribute('id', 'tableB');
    destination.parentNode.replaceChild(copy, destination);

    
}
