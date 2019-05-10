let idsFichasConDefinicionYejemplo = [];
let clasePanelButtons = "panel-buttons-display-none";


$(function() {
    $(".loader").hide();
    $("#id_word").attr("placeholder", "Palabra");
    $("#button-accept").on("click", selectOptionHandler);
    $("#formulario").on("submit", showCardHandler);
    $("#text-mayusculas").on("click", selectOptionHandler);

});

function selectOptionHandler(){


    $("body").css("text-transform" ,"uppercase");
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
    let level = $("#level").val();
   
    
     $(".loader").show();
     $("#list-results").html("");
     $(".title").html("");
     $.ajax({
        type:'POST',
        url: '/',
        data: {'button-search' : true, 'word' : word, 'level' : level},
        success: mostrarJson,
        error: function(data, jqXHR, textStatus, errorThrown){
            console.log(data);

        }
     });

}



function mostrarJson(json){
    $(".loader").hide();

    $("#list-results").html("");
    let contador = 1;
    console.log(json);
    
    if(json.allOffsets.length == 0){
        $(".title").html("");
        let elemento = "<h3> No hay resultados para la palabra" + "<p class=' word ml-2'>" + json.word + "</p></h3>";
        console.log(elemento);
        $(".title").append(elemento); 
    }else{

        json.allOffsets.forEach(offset => {
            let arrayMetaforas = [];
            let arraySimiles = [];
            
            if(json.metaphor.length > 0){
                json.metaphor.find(elem =>{             
                    if(elem.type == "SYNONYM" && elem.offset == offset.offset || elem.type == "HYPERONYM" && elem.offsetFather == offset.offset ){
                        arrayMetaforas.push(elem);
                    }
                });
            }      
            if(json.simil.length > 0){ 
                json.simil.find(elem =>{
                    if (elem.offsetFather == offset.offset){
                        arraySimiles.push(elem);
                    }
                });
            }
    
            if(arrayMetaforas.length > 0 || arraySimiles.length > 0){
                $(".title").html("");
                let elemento = "<h3> Resultados para la palabra" + "<p class=' word ml-2'>" + json.word + "</p></h3>";
                console.log(elemento);
                $(".title").append(elemento); 
                obtenerImg(offset, arrayMetaforas, arraySimiles, contador, json.word);
                
                ++contador;
            }
            
        });
    }


    
}


function getImgContentType(img, callback) {
    let hayImagen = true;
    let xhr = new XMLHttpRequest();
    xhr.open("GET",img, false);
    xhr.onload = function() {       

        if (this.readyState == this.DONE) {
           // console.log(xhr.getResponseHeader("Content-Type"));   // type
            if (xhr.getResponseHeader("Content-Type") != "application/json") {
                hayImagen = true;
                
            }else{
                hayImagen = false;
                 
            }
            
            callback(hayImagen);
            //console.log(xhr.getResponseHeader("Content-Length")); // size
            // ...
            //return xhr.getResponseHeader("Content-Type");
        }
    };
    xhr.send();
    
}

function obtenerImg(offset, resultadoMetaforas, resultadoSimiles, numTarjeta, palabra){
   
    //--> LOCAL
   getImgContentType("http://127.0.0.1:8000/imagen/" +  offset.offset, (hayImg) => {
            formarFicha(hayImg, offset, resultadoMetaforas, resultadoSimiles, numTarjeta, palabra);
    });

    //--> HOLSTEIN
    /*
    getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset, (hayImg) => {
            formarFicha(hayImg, offset, resultadoMetaforas, resultadoSimiles, numTarjeta, palabra);
    });*/
    
    
    
}



function formarFicha(hayImg, offset, resultadoMetaforas, resultadoSimiles, numTarjeta, palabra){
    
    let elemento;
    if (hayImg) {
        //--> LOCAL
        elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto' src='http://127.0.0.1:8000/imagen/" +  offset.offset + "'></img><div class='results'><p>";
        
        //--> HOLSTEIN
        //elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset + "'></img><div class='results'><p>";
        
    }else{        
        elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><div class='results'><p>"
    }
    let definicion = [];
    let tieneDef = false;
    let tieneEjemplo = false;
    let ejemplo = [];


    if(resultadoMetaforas.length > 0){
        resultadoMetaforas.forEach(result =>{
            result.metaphor.forEach(metaphor=> {
                let enlace = metaphor.split(" ").pop();
                phrase = metaphor.replace(enlace, "");
                
                
              //--> LOCAL
                getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'>" + palabra + ' ' + phrase + "</div><div class='panel-img ml-2'><img class='image-picto result-picto' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img><a href='#'>" + enlace + "</a></div</li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a class='ml-2' href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });
                // --> HOLSTEIN
                /*getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
            });
           
        });
    } 

    if(resultadoSimiles.length > 0){
        console.log("RESULTADO SIMILES");
        console.log(resultadoSimiles);
        resultadoSimiles.forEach(similResult =>{
            similResult.simil.forEach(simil =>{
               
            let enlace = simil.split(" ").pop();
                phrase = simil.replace(enlace, "");
                
                
              //--> LOCAL
                getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'>" + palabra + ' ' + phrase + "</div><div class='panel-img ml-2'><img class='image-picto result-picto' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img><a href='#'>" + enlace + "</a></div</li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a class='ml-2' href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });
                // --> HOLSTEIN
                /*getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
            });
            
           
        });
        
    }
  /*  if(resultadoSinonimos != undefined){

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
                //--> LOCAL
                getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'>" + palabra + ' ' + phrase + "</div><div class='panel-img ml-2'><img class='image-picto result-picto' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img><a href='#'>" + enlace + "</a></div></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a class='ml-2' href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/

                  //--> HOLSTEIN
                 /* getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
        
       /* });

    }*/
    
   /* if(resultadoHiponimos != undefined){
       
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
                
                
              //--> LOCAL
                getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'>" + palabra + ' ' + phrase + "</div><div class='panel-img ml-2'><img class='image-picto result-picto' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img><a href='#'>" + enlace + "</a></div</li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a class='ml-2' href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
                // --> HOLSTEIN
                /*getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
           /* }); 
        });

    }*/
   /*
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
                
                //--> LOCAL
                getImgContentType("http://127.0.0.1:8000/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'>" + palabra + ' ' + phrase + "</div><div class='panel-img ml-2'><img class='image-picto result-picto' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img><a href='#'>" + enlace + "</a></div></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a class='ml-2' href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
                //--> HOLSTEIN
                /*getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img></li><br>";
                    }else{
                        elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
                    }
                   
                });*/
            /*});     
        });

       
    }*/


    /*if(tieneDef || tieneEjemplo){
        elemento += "<div id='panel-button' class='" + clasePanelButtons + "'>" +
        "<div class='dropdown show'><a class='btn btn-def dropdown-toggle' href='#' role='button'  data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
           "Definición y Ejemplo</a><div class='dropdown-menu panel-dropdown-def' aria-labelledby='dropdownMenuLink'><div class='panel-def-example-only-button'>" + definicion + ejemplo;

        idsFichasConDefinicionYejemplo.push(numTarjeta);
    }*/

        
            

    $("#list-results").append(elemento);
}