let idsFichasConDefinicionYejemplo = [];
let clasePanelButtons = "panel-buttons-display-none";


$(function() {

    $("#button-accept").on("click", selectOptionHandler);
    $("#formulario").on("submit", showCardHandler);


});

function selectOptionHandler(){

    if($("#mayusculas").is(':checked')){
        $("body").css("text-transform" ,"uppercase");

    }else{
        $("body").css("text-transform" ,"");

    }


    if($("#defyejemplo").is(':checked')){
        clasePanelButtons = "panel-buttons-display-block";
        $(".panel-buttons").removeClass("panel-buttons-display-none");
        $(".panel-buttons").addClass("panel-buttons-display-block");

    }
}




function showCardHandler(event){

    event.preventDefault();
    let word = $("#formulario").find("p").find("input").val();
    let elemento = "<h3> Resultados para la palabra" + "<p class='ml-2'>" + word + "</p></h3><ul id='list-results'>";
    $(".panel-results").append(elemento); 
    
     $.ajax({
        type:'POST',
        url: 'version1',
        data: {'button-search' : true, 'word' : word},
        success: mostrarJson,
        error: function(data, jqXHR, textStatus, errorThrown){
            console.log(data);

        }
     });

}


function mostrarJson(json){
    $("#list-results").html("");
    let contador = 1;
    console.log(json);
    
    json.allOffsets.forEach(offset => {
        let arrayHiponimos = [];
        let arrayHiperonimos = [];
        
        let resultadoSinonimos = json.resultsSynonyms.find(resultSynonym =>{
            return resultSynonym.offset == offset.offset;
        });

        arrayHiponimos = getArrayResultado(offset, json.resultsHyponyms);
        arrayHiperonimos = getArrayResultado(offset, json.resultsHyperonyms);
       

        if(resultadoSinonimos != undefined || arrayHiponimos.length > 0 || arrayHiperonimos.length > 0){
            formarFicha(offset, resultadoSinonimos, arrayHiponimos, arrayHiperonimos, contador, json.word);
            
            ++contador;
        }
    });
}




function getArrayResultado(offset, array){
   let arrayResultado = [];
    array.forEach(element =>{            
        if (element.offsetFather == offset.offset){
            arrayResultado.push(element);
        };
    });
    return arrayResultado;
}


function getImgContentType(img, callback) {
    let hayImagen = true;
    let xhr = new XMLHttpRequest();
    xhr.open("GET",img, false);
    xhr.onload = function() {
        console.log("HOLIII");

        if (this.readyState == this.DONE) {
            console.log(xhr.getResponseHeader("Content-Type"));   // type
            if (xhr.getResponseHeader("Content-Type") != "application/json") {
                hayImagen = true;
                console.log("HAY IMAGEN");
            }else{
                hayImagen = false;
                console.log(" NO HAY IMAGEN");
            }
            
            callback(hayImagen);
            //console.log(xhr.getResponseHeader("Content-Length")); // size
            // ...
            //return xhr.getResponseHeader("Content-Type");
        }
    };
    xhr.send();
    
}

function formarFicha(offset, resultadoSinonimos, resultadoHiponimos, resultadoHiperonimos,  numTarjeta, palabra){
    //console.log("OFFSET")
    //console.log(offset.offset)
    //httpGetAsync()
   /* getImgContentType("http://127.0.0.1:8000/imagen/" +  offset.offset, (hayImg) => {
            formarFicha2(hayImg, offset, resultadoSinonimos, resultadoHiponimos, resultadoHiperonimos,  numTarjeta, palabra)
    });*/
    getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset, (hayImg) => {
            formarFicha2(hayImg, offset, resultadoSinonimos, resultadoHiponimos, resultadoHiperonimos,  numTarjeta, palabra)
    });
    
    
    
}



function formarFicha2(hayImg, offset, resultadoSinonimos, resultadoHiponimos, resultadoHiperonimos,  numTarjeta, palabra){
    console.log(hayImg)
    let elemento;
    if (hayImg) {
        //elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagen/" +  offset.offset + "'></img><div class='results'><p>";
        elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset + "'></img><div class='results'><p>";
        //let elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset + "'></img><div class='results'><p>"; 
    }else{        
        elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><div class='results'><p>"
    }
    let definicion = [];
    let tieneDef = false;
    let tieneEjemplo = false;
    let ejemplo = [];
    if(resultadoSinonimos != undefined){

        resultadoSinonimos.phraseSynonyms.forEach(phrase =>{

            if(phrase.definition != undefined){
                tieneDef = true;
                definicion += "<p><b> Definición:</b><i>" + phrase.definition + "</i></p>";
           }    

           if(phrase.example != undefined){
                tieneEjemplo = true;
                ejemplo += "<p><b> Ejemplo:</b><i>" + phrase.example + "</i></p>";
           }
    
            
                let enlace = phrase.split(" ").pop();
                phrase = phrase.replace(enlace, "");
                //elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
               
                getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });
                /*getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/

                
        
        });

    }
    
    if(resultadoHiponimos != undefined){
       
        resultadoHiponimos.forEach(phrase =>{
            if(phrase.definition.length != 0){
            tieneDef = true;
                definicion += "<p><b> Definición:</b><i>" + phrase.definition + "</i></p>";
           }    

           if(phrase.example.length != 0){
                tieneEjemplo = true;
                ejemplo += "<p><b> Ejemplo:</b><i>" + phrase.example + "</i></p>";
           }

            phrase.phraseHyponyms.forEach(p =>{              
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                //elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                console.log(enlace)
                getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });
                /*getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
            }); 
        });

    }
   
    if(resultadoHiperonimos != undefined){         
        resultadoHiperonimos.forEach(phrase =>{     

    
            if(phrase.definition.length != 0){
                tieneDef = true;
                definicion += "<p><b> Definición:</b><i>" + phrase.definition + "</i></p>";
           }   

           if(phrase.example.length != 0){
                tieneEjemplo = true;
                ejemplo += "<p><b> Ejemplo:</b><i>" + phrase.example + "</i></p>";
           }
            phrase.phraseHyperonyms.forEach(p =>{
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                //elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                console.log(enlace)
                getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });
                /*getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
            });     
        });

       
    }


    if(tieneDef || tieneEjemplo){
        elemento += "<div id='panel-button' class='" + clasePanelButtons + "'>" +
        "<div class='dropdown show'><a class='btn btn-def dropdown-toggle' href='#' role='button'  data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
           "Definición y Ejemplo</a><div class='dropdown-menu panel-dropdown-def' aria-labelledby='dropdownMenuLink'><div class='panel-def-example-only-button'>" + definicion + ejemplo;

        idsFichasConDefinicionYejemplo.push(numTarjeta);
    }

        
            

    $("#list-results").append(elemento);
}