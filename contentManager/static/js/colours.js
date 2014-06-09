var canvas;
var context;
var p1 = 0.99;
var p2 = 0.99;
var p3 = 0.99;
var er = 0; // extra red
var eg = 0; // extra green
var eb = 0; // extra blue
var func = 'colored'; // used function

window.onload = function() {
    canvas = document.getElementById('panel');
    context = canvas.getContext('2d');

    context.fillStyle = '#888888';
    context.fillRect(0, 0, 530, 280);
	
	context.fillStyle = '#FFFFFF'; // Color del texto
    context.textBaseline = "top"; // Línea base del texto
    context.font = '14px Verdana'; // Tamaño y estilo de la fuente
	context.fillText("Original image" , 80, 2);
	context.fillText("Filter image" , 340, 2);
	

    var imgObj = new Image();
    imgObj.onload = function () {
        context.drawImage(imgObj, 10, 20, 250, 250); 
    }
    imgObj.src = '/static/img/spring.jpg';
};

function Grayscale() {
    func = 'grayscale';
    var imgd = context.getImageData(10, 20, 250, 250);
    var data = imgd.data;
    for (var i = 0, n = data.length; i < n; i += 4) {
        var grayscale = data[i] * p1 + data[i+1] * p2 + data[i+2] * p3;
        data[i]   = grayscale + er; // red
        data[i+1] = grayscale + eg; // green
        data[i+2] = grayscale + eb; // blue
    }
    context.putImageData(imgd, 270, 20);
}

function Colored() {
    func = 'colored';
    var imgd = context.getImageData(10, 20, 250, 250);
    var data = imgd.data;
    for (var i = 0, n = data.length; i < n; i += 4) {
        data[i]   = data[i]*p1+er; // red
        data[i+1] = data[i+1]*p2+eg; // green
        data[i+2] = data[i+2]*p3+eb; // blue
    }
    context.putImageData(imgd, 270, 20);
}

function reset() {
    switch(func) {
        case 'grayscale': resetToGrayscale(); break;
        case 'colored': resetToColored(); break;
    }
}

function changeGrayValue(val) {
    p1 += val;
    p2 += val;
    p3 += val;

    switch(func) {
        case 'grayscale': Grayscale(); break;
        case 'colored': Colored(); break;
    }
}

function changeColorValue(sobj, val) {
    switch (sobj) {
        case 'er': er += val; break;
        case 'eg': eg += val; break;
        case 'eb': eb += val; break;
    }

    switch(func) {
        case 'grayscale': Grayscale(); break;
        case 'colored': Colored(); break;
    }
}

function resetToColored() {
    p1 = 1;
    p2 = 1;
    p3 = 1;
    er = eg = eb = 0;

    Colored();
}
function resetToGrayscale() {
    p1 = 0.3;
    p2 = 0.59;
    p3 = 0.11;
    er = eg = eb = 0;

    Grayscale();
}
