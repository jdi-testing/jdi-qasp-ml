var script = document.createElement("script")
script.type = "text/javascript";

if (script.readyState){  //IE
    script.onreadystatechange = function(){
        if (script.readyState == "loaded" ||
                script.readyState == "complete"){
            script.onreadystatechange = null;
            console.log('script executed'); //callback();
        }
    };
} else {  //Others
    script.onload = function(){
        console.log('script executed'); //callback();
    };
}

script.src = 'http://localhost:5000/js/build-dataset.js';
console.log('loading script...')
document.getElementsByTagName("head")[0].appendChild(script);