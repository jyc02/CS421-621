//this function handles the functionality of the calculator
// w3schools are referenced for builtin functions
function calc(value){
    if (value == 'pow'){
        document.getElementById("display").value = document.getElementById("display").value * document.getElementById("display").value;
    } else if (value == 'sqrt'){
        document.getElementById("display").value = Math.sqrt(document.getElementById("display").value);
    } else if (value == 'sin'){
        document.getElementById("display").value = Math.sin(document.getElementById("display").value);
    } else if (value == 'cos'){
        document.getElementById("display").value = Math.cos(document.getElementById("display").value);
    } else if (value == 'tan'){
        document.getElementById("display").value = Math.tan(document.getElementById("display").value);
        console.log("tan passed");
    } else if (value == '='){
        document.getElementById("display").value = eval(document.getElementById("display").value);
    }else if(value == ''){
        document.getElementById("display").value = value;
    } else {
        document.getElementById("display").value += value;
    }
}
