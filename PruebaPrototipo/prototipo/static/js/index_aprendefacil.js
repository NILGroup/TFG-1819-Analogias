let idsFichasConDefinicionYejemplo = [];
let clasePanelButtons = "panel-buttons-display-none";
let claseMostrarPictos = "pos-ini-none";
let clasePosicionPictos = "panel-img";
let posicionMet = "p-met";

let existMetaphor = false;
let existSimil = false;
$(function() {
    $(".loader").hide();
    $("#id_word").attr("placeholder", "Palabra");
    $("#button-accept").on("click", selectOptionHandler);
    $("#formulario").on("submit", showCardHandler);
    $("#mayusculas").on("click", selectOptionHandler);
     
    $("#button-send").on("click", selectOptionHandler);
    $("#defyejemplo-oculto").on("click", selectOptionHandler);
    
    
});




function selectOptionHandler(){
    
    if($("#mayusculas").is(':checked')){
        
        $("#mayusculas").val("Convertir a minúsculas"); 
        $("body").css("text-transform" ,"uppercase");

    } else{
        $("body").css("text-transform" ,"");
    }

    if($("#minusculas").is(':checked')){
        $(".minusculas").html("");
        $(".mayusculas").append("<div class=' mayusculas center-content border-color-right'><input type='checkbox' id='mayusculas' class='options ml-3'><a id='text-mayusculas' class='options dropdown-item' href='#'>Convertir a mayúsculas</a></input></div>");
        $("body").css("text-transform" ,"lowercase");

    }

    if($("#defyejemplo").is(':checked')){
       // $(".def-example").css("display", "block");
       $(".defyejemplo").html("");
        $(".defyejemplo").append("<div class=' defyejemplo-oculto center-content border-color-right'><input type='checkbox' id='defyejemplo-oculto' class='options ml-3'><a class='dropdown-item' href='#'>Ocultar definición y ejemplo</a></input></div>");
       clasePanelButtons = "panel-buttons-display-block";
       
       $(".panel-buttons").removeClass("panel-buttons-display-none");
        $(".panel-buttons").addClass("panel-buttons-display-block");
    }else{
        clasePanelButtons = "panel-buttons-display-none";
    }
    /*}else{
        $(".def-example").css("display", "none"); 
    }*/


    if($("#defyejemplo-oculto").is(':checked')){
        // $(".def-example").css("display", "block");
        $(".defyejemplo-oculto").html("");
         $(".defyejemplo-oculto").append("<div class=' defyejemplo center-content border-color-right'><input type='checkbox' id='defyejemplo' class='options ml-3'><a class='dropdown-item' href='#'>Mostrar definición y ejemplo</a></input></div>");
         clasePanelButtons = "panel-buttons-display-none";
       
     }



    if($("#pictos").is(':checked')){
        claseMostrarPictos = "pos-ini-block";
        clasePosicionPictos = "position-img";
        $(".image-picto").removeClass("pos-ini-none");
        $(".image-picto").addClass("pos-ini-block");

        posicionMet = "position-p-img";
        $(".panel-img").removeClass("panel-img");
        $(".panel-img").addClass("position-img");
        $(".p-met").removeClass("p-met");
        $(".p-met").addClass("position-p-img");
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
        url: 'https://holstein.fdi.ucm.es/tfg-analogias/',
        //url: '/',
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
         
        $(".title").append(elemento); 
    }else{

        json.allOffsets.forEach(offset => {
             console.log("offset");
             console.log(offset);
            let arrayMetaforas = [];
            let arraySimiles = [];
            let arrayContent = [];
            
            if(json.metaphor.length > 0){
                 
                json.metaphor.find(elem =>{             
                    if(elem.type == "SYNONYM" && elem.offset == offset.offset || elem.type == "HYPERONYM" && elem.offsetFather == offset.offset ){
                        existMetaphor = true;
                        arrayMetaforas.push(elem);
                    }
                });
            }      
            if(json.simil.length > 0){ 
                 
                json.simil.find(elem =>{
                    if (elem.offsetFather == offset.offset){
                        existSimil = true;
                        arraySimiles.push(elem);
                    }
                });
            }
            
            if(json.content.length > 0){
                 
                json.content[1].metaphor.forEach(elem =>{
                     
                    if(elem.type == "SYNONYM" && elem.offset == offset.offset || elem.type == "HYPERONYM" && elem.offsetFather == offset.offset || elem.type == "HYPONYM" && elem.offsetFather == offset.offse ){
                        arrayContent.push(elem);
                    }
                });
            }

            
            if(arrayMetaforas.length > 0 || arraySimiles.length > 0){
                $(".title").html("");
                let elemento = "<h3> Resultados para la palabra" + "<p class=' word ml-2'>" + json.word + "</p></h3>";
                
                $(".title").append(elemento); 
                obtenerImg(offset, arrayMetaforas, arraySimiles, arrayContent, contador, json.word);
                
                ++contador;
            }
            

            
        });

        if(!existMetaphor && !existSimil){
            let elemento = "<h3> No hay resultados para la palabra" + "<p class=' word ml-2'>" + json.word + "</p></h3>";
            $(".title").append(elemento); 
        }
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

function obtenerImg(offset, resultadoMetaforas, resultadoSimiles, resultadoDefEjemplo, numTarjeta, palabra){
   
    //--> LOCAL
  /* getImgContentType("http://127.0.0.1:8000/imagen/" +  offset.offset, (hayImg) => {
            formarFicha(hayImg, offset, resultadoMetaforas, resultadoSimiles, resultadoDefEjemplo, numTarjeta, palabra);
    });*/

    //--> HOLSTEIN
    
    getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset, (hayImg) => {
            formarFicha(hayImg, offset, resultadoMetaforas, resultadoSimiles, resultadoDefEjemplo, numTarjeta, palabra);
    });
    
    
    
}



function formarFicha(hayImg, offset, resultadoMetaforas, resultadoSimiles, resultadoDefEjemplo, numTarjeta, palabra){
    
    let elemento;
    if (hayImg) {
        //--> LOCAL
       // elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto' src='http://127.0.0.1:8000/imagen/" +  offset.offset + "'></img><div class='results'><p>";
        
        //--> HOLSTEIN
       elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto " + claseMostrarPictos + "' src='https://holstein.fdi.ucm.es/tfg-analogias/imagen/" +  offset.offset + "'></img><div class='results'><p>";
       
        
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
    
                // --> HOLSTEIN
                getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'><i class='material-icons color-list mr-3'>lens</i>" + palabra + ' ' + phrase +
                        "</div><div class='panel-img mt-3 " + clasePosicionPictos + " ml-2'><img class='image-picto " + claseMostrarPictos + 
                        " result-picto' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img>" +
                        "<p class='" + posicionMet + "'>" + enlace + "</p></div></li><hr>";
                    }else{
                        elemento += "<li><i class='material-icons color-list mr-3'>lens</i>" + palabra + ' ' + phrase + 
                        "<p class='ml-2 mt-3'>" + enlace + "</p></li><hr>";
                       // "<a class='ml-2' href='/'>" + enlace + "</a></li><hr>";
                    }
                   
                });
                
            });
           
        });
    } 

    if(resultadoSimiles.length > 0){
       
        resultadoSimiles.forEach(similResult =>{             
            similResult.simil.forEach(simil =>{
               
            let enlace = simil.split(" ").pop();
                phrase = simil.replace(enlace, "");
                
                // --> HOLSTEIN
                getImgContentType("https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace, (hayImg)=>{
                    if(hayImg){
                        elemento += "<li><div class='panel-word'><i class='material-icons color-list mr-3'>lens</i>" + palabra + ' ' + phrase + 
                        "</div><div class='panel-img mt-3 " + clasePosicionPictos + "  ml-2'><img class='image-picto " + claseMostrarPictos + 
                        " result-picto' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img>" +
                        "<p>" + enlace + "<p></div></li><hr>";
                    }else{
                        elemento += "<li><i class='material-icons color-list mr-3'>lens</i>" + palabra + ' ' + phrase + 
                        "<p class='ml-2 mt-3'>" + enlace + "</p></li><hr>";
                    }
                   
                });
                
            });
            
           
        });
        
    }

   
    if(resultadoDefEjemplo.length > 0){
        resultadoDefEjemplo.forEach(result =>{
            console.log("def");
            console.log(result.definition);
            tieneDef = true;
            definicion += "<p><b> Definición:</b><i>" + result.definition + "</i></p>";
            
            if(result.example.length > 0){
                result.example.forEach(exam =>{
                    tieneEjemplo = true;
                    ejemplo += "<p><b> Ejemplo:</b><i>" + result.example + "</i></p>";
                    console.log("ejemplo");
                    console.log(exam);
                });
            }
            
        });
    }


    if(tieneDef || tieneEjemplo){
        /*elemento += "<div id='panel-button' class='def-example'>" +
        "<div class='dropdown show'><a class='btn btn-def dropdown-toggle' href='#' role='button'  data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
        "Definición y Ejemplo</a><div class='dropdown-menu panel-dropdown-def' aria-labelledby='dropdownMenuLink'><div class='panel-def-example-only-button'>" + definicion + ejemplo;
    }*/
        elemento += "<div id='panel-button' class='" + clasePanelButtons + "'>" +
        "<div class='dropdown show'><a class='btn btn-def dropdown-toggle' href='#' role='button'  data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
        "Definición y Ejemplo</a><div class='dropdown-menu panel-dropdown-def' aria-labelledby='dropdownMenuLink'><div class='panel-def-example-only-button'>" + definicion + ejemplo;
    }
    
    $("#list-results").append(elemento);
    
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

        
            

    
}