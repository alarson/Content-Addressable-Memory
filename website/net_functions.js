
"use strict";


var network_size = 5;

//network weights
var weights = new Array(network_size*network_size);
for(var i=0; i<network_size*network_size; i++) {
    weights[i] = new Array(network_size*network_size).fill(0);
}

//List of network states that have been saved
var memories = [];
var cur_memory_index = 0;

//Matrix to hold current network state vector
var network_state = new Array(network_size*network_size).fill(-1);

function clear_pallette() {
    //clear out network state
    network_state = new Array(network_size*network_size).fill(-1);
    //blank out the image table
    $("#drawing-table td").css("background-color","white");
    $("#network").text(network_state);
}

function store() {
    memories[cur_memory_index]=network_state.slice();
    cur_memory_index+=1;
    var new_weights = math.subtract( outer_product(network_state.slice(),network_state.slice()),numeric.identity(network_size*network_size));
    weights = math.add(weights,new_weights);
    clear_pallette();
    $("#weights").text(weights.toString());
    save_image();
}

function probe_synch(){
    for(var i=0; i<3; i++) {
        //alert("probing");
       setTimeout(update_synch, 1000);
    }
}

function update_synch(){
//    alert(memories);
    var Tx = math.multiply(network_state,weights);
    //alert(Tx);
    for (var i = 0; i < Tx.length; i++) {
        if(Tx[i]!=0){
            Tx[i]=Tx[i]/Math.abs(Tx[i]);
        }
    }
    //alert(Tx);
    network_state = Tx
    update_visualization();
    $("#network").text(network_state);
}
function cross_product(customerArray,debtorArray){
    var customerDebtorMatrix = [];
    for (var i = 0; i < customerArray.length; i++) {
        
        for (var l = 0; l < debtorArray.length; l++) {
            customerDebtorMatrix.push(customerArray[i]*(debtorArray[l]));
            
        }
    return customerDebtorMatrix;
}
}

function update_asynch(){

    //select random node for update
    var node = math.floor(math.random() * (network_state.length));

        
    //sum inputs, and take the sign of the resulting integer
        
    var sum = 0;
    for (var r = 0; r < network_state.length; r++) {
        sum += weights[r][node]*network_state[r];
    }
//    var temp = numeric.sum(cross_product(weights[node],network_state));
     $("#coordinates").text(sum);
    if(sum<0){network_state[node]=-1;}
    else{network_state[node]=1;}

    update_visualization();

    
}

function multiply_matrix(a, b) {
  var aNumRows = a.length, aNumCols = a[0].length,
      bNumRows = b.length, bNumCols = b[0].length,
      m = new Array(aNumRows);  // initialize array of rows
  for (var r = 0; r < aNumRows; ++r) {
    m[r] = new Array(bNumCols); // initialize the current row
    for (var c = 0; c < bNumCols; ++c) {
      m[r][c] = 0;             // initialize the current cell
      for (var i = 0; i < aNumCols; ++i) {
        m[r][c] += a[r][i] * b[i][c];
      }
    }
  }
  return m;
}
function outer_product(a, b) {
  var m = new Array(a.length);  // initialize array of rows
  for (var r = 0; r < a.length; ++r) {
    m[r] = new Array(a.length); // initialize the current row
    for (var c = 0; c < a.length; ++c) {
      m[r][c] = a[r]*b[c];
    }
  }
  return m;
}
function cycle(direction){
//this is a circular manner for cycling saved states
//to view them
    if(memories.length>0){
        switch(direction){
            case 0: //moving left
                if(cur_memory_index>0){
                    cur_memory_index-=1;
                }
                else{
                    cur_memory_index=memories.length-1;
                }
                break;
            case 1: //moving right
                if(cur_memory_index<memories.length-1){
                    cur_memory_index+=1;
                }
                else{
                    cur_memory_index=0;
                }
                break;
        }
        alert(cur_memory_index);
        alert(memories.length)
        network_state=memories[cur_memory_index].slice(0);
        update_visualization();
    }
}
function test_function(){
    for(var i = 0;i<2;i++){
        update_asynch();
    }
    
}
