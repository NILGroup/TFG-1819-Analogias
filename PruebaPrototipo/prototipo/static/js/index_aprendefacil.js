let idsFichasConDefinicionYejemplo = [];
let clasePanelButtons = "panel-buttons-display-none";
let claseMostrarPictos = "pos-ini-none";
let clasePosicionPictos = "panel-img";
let posicionMet = "p-met";
let buttonSendPulsado = false;

let existMetaphor = false;
let existSimil = false;
$(function() {
    $(".loader").hide();
    $("#id_word").attr("placeholder", "Palabra");
     
    $("#formulario").on("submit", showCardHandler);
    $("#mayusculas").on("click", selectOptionHandler);
    $("#minusculas").on("click", selectOptionHandler);
     
    $("#defyejemplo").on("click", defyejemploCheckboxHandler);
    $("#defyejemplo-ocultar").on("click", defyejemploCheckboxHandler);

    $("#pictos").on("click", pictosCheckboxHandler);
    $("#pictos-oculto").on("click", pictosCheckboxHandler);

    $("#button-send").on("click", selectOptionHandler);
    $("#list-results").on("click", ".word-search", wordSearchHandler);
   
  
    
});


function wordSearchHandler(){

    let word = $(this).text();
    let level = $("#level").val();
   
     $(".loader").show();
     $("#list-results").html("");
     $(".title").html("");
     $("#id_word").val(word);
    let url = "/word=" + word + "&level=" + level;
     $.ajax({
        type:'GET',
        url: 'https://holstein.fdi.ucm.es/tfg-analogias' + url,
        //url: url,        
        success: mostrarJson,
        error: function(data, jqXHR, textStatus, errorThrown){
            console.log(data);

        }
     });
}

/* Metodo que hace que aparezca o desaparezca la definicion y el ejemplo cuando ya han salido los resultados */
function pictosCheckboxHandler(){
    if (buttonSendPulsado){
        if($("#pictos").is(':checked')){        
            claseMostrarPictos = "pos-ini-block";            
            $(".image-picto").removeClass("pos-ini-none");
            $(".image-picto").addClass("pos-ini-block");
    
            clasePosicionPictos = "position-img";
            $(".position-metaphor").removeClass("panel-img");
            $(".position-metaphor").addClass("position-img");

            posicionMet = "position-p-img";
            $(".p-met").addClass("position-p-img");
        }


        if($("#pictos-oculto").is(':checked')){ 
            claseMostrarPictos = "pos-ini-none";            
            $(".image-picto").removeClass("pos-ini-block");
            $(".image-picto").addClass("pos-ini-none");
    
            clasePosicionPictos = "panel-img";
            $(".position-metaphor").removeClass("position-img");
            $(".position-metaphor").addClass("panel-img");

            posicionMet = "p-met";
            $(".p-met").addClass("p-met");
            $(".p-met").removeClass("position-p-img");  
    
        }
        /*let texto = $("#text-pictos").find("span").text(); 
     
        if (texto == "Mostrar pictos"){
            $("#text-pictos").find("span").text("Ocultar pictos"); 
            claseMostrarPictos = "pos-ini-block";            
            $(".image-picto").removeClass("pos-ini-none");
            $(".image-picto").addClass("pos-ini-block");
    
            clasePosicionPictos = "position-img";
            $(".position-metaphor").removeClass("panel-img");
            $(".position-metaphor").addClass("position-img");

            posicionMet = "position-p-img";
            $(".p-met").addClass("position-p-img");
            //$(".p-met").removeClass("p-met");
            

        }else if(texto == "Ocultar pictos"){
            $("#text-pictos").find("span").text("Mostrar pictos"); 
            claseMostrarPictos = "pos-ini-none";            
            $(".image-picto").removeClass("pos-ini-block");
            $(".image-picto").addClass("pos-ini-none");
    
            clasePosicionPictos = "panel-img";
            $(".position-metaphor").removeClass("position-img");
            $(".position-metaphor").addClass("panel-img");

            posicionMet = "p-met";
            $(".p-met").addClass("p-met");
            $(".p-met").removeClass("position-p-img");   
        }
        
        $("#pictos").prop("checked", false);*/
        
        }
}

/* Metodo que hace que aparezca o desaparezca la definicion y el ejemplo cuando ya han salido los resultados */
function defyejemploCheckboxHandler(){
    if (buttonSendPulsado){
        if($("#defyejemplo").is(':checked')){
            clasePanelButtons = "panel-buttons-display-block";       
            $(".panel-buttons").removeClass("panel-buttons-display-none");
            $(".panel-buttons").addClass("panel-buttons-display-block");
            $(".color-no-defyejemplo").removeClass("panel-buttons-display-none");
            $(".color-no-defyejemplo").addClass("panel-buttons-display-block");
         }
    
         if($("#defyejemplo-ocultar").is(':checked')){
            clasePanelButtons = "panel-buttons-display-none";       
            $(".panel-buttons").removeClass("panel-buttons-display-block");
            $(".panel-buttons").addClass("panel-buttons-display-none");
            $(".color-no-defyejemplo").removeClass("panel-buttons-display-block");
            $(".color-no-defyejemplo").addClass("panel-buttons-display-none");
         }
        /*let texto = $("#text-defyejemplo").find("span").text(); 
     
        if (texto == "Mostrar definición y ejemplo"){
            $("#text-defyejemplo").find("span").text("Ocultar definición y ejemplo"); 
            clasePanelButtons = "panel-buttons-display-block";
            $(".panel-buttons").removeClass("panel-buttons-display-none");
            $(".panel-buttons").addClass("panel-buttons-display-block");
            $(".color-no-defyejemplo").removeClass("panel-buttons-display-none");

        }else if(texto == "Ocultar definición y ejemplo"){
            $("#text-defyejemplo").find("span").text("Mostrar definición y ejemplo"); 
            clasePanelButtons = "panel-buttons-display-none";
            $(".panel-buttons").removeClass("panel-buttons-display-block");
            $(".panel-buttons").addClass("panel-buttons-display-none");
            $(".color-no-defyejemplo").addClass("panel-buttons-display-none");   
        }
        
        $("#defyejemplo").prop("checked", false);*/
        
        }
}


function selectOptionHandler(){
    let texto = $("#text-mayusculas").find("span").text(); 
    
     buttonSendPulsado = true;

     if($("#mayusculas").is(':checked')){
        $("body").css("text-transform" ,"uppercase");
     }


     if($("#minusculas").is(':checked')){
        $("body").css("text-transform" ,"");
     }

     
     if($("#defyejemplo").is(':checked')){
        clasePanelButtons = "panel-buttons-display-block";       
        $(".panel-buttons").removeClass("panel-buttons-display-none");
        $(".panel-buttons").addClass("panel-buttons-display-block");
        $(".color-no-defyejemplo").removeClass("panel-buttons-display-none");
        $(".color-no-defyejemplo").addClass("panel-buttons-display-block");
     }

     if($("#defyejemplo-ocultar").is(':checked')){
        clasePanelButtons = "panel-buttons-display-none";       
        $(".panel-buttons").removeClass("panel-buttons-display-block");
        $(".panel-buttons").addClass("panel-buttons-display-none");
        $(".color-no-defyejemplo").removeClass("panel-buttons-display-block");
        $(".color-no-defyejemplo").addClass("panel-buttons-display-none");
     }



     if($("#pictos").is(':checked')){        
        claseMostrarPictos = "pos-ini-block";
        clasePosicionPictos = "position-img";
        $(".image-picto").removeClass("pos-ini-none");
        $(".image-picto").addClass("pos-ini-block");

        posicionMet = "position-p-img";
        $(".panel-img").removeClass("panel-img");
        $(".panel-img").addClass("position-img");   
        $(".p-met").addClass("position-p-img");
    }

    /*if($("#pictos-oculto").is(':checked')){ 
        claseMostrarPictos = "pos-ini-none";            
        $(".image-picto").removeClass("pos-ini-block");
        $(".image-picto").addClass("pos-ini-none");

        clasePosicionPictos = "panel-img";
        $(".position-metaphor").removeClass("position-img");
        $(".position-metaphor").addClass("panel-img");

        posicionMet = "p-met";
        $(".p-met").addClass("p-met");
        $(".p-met").removeClass("position-p-img");   

    }*/
    
    /*if($("#mayusculas").is(':checked')){
        if (texto == "Convertir a minúsculas"){
            $("#text-mayusculas").find("span").text("Convertir a mayúsculas"); 
            $("body").css("text-transform" ,"");

        }else if(texto == "Convertir a mayúsculas"){

            $("#text-mayusculas").find("span").text("Convertir a minúsculas"); 
            $("body").css("text-transform" ,"uppercase");
        }
        $("#mayusculas").prop("checked", false);
    }*/
   

   /* if($("#defyejemplo").is(':checked')){
        $("#text-defyejemplo").find("span").text("Ocultar definición y ejemplo"); 
       clasePanelButtons = "panel-buttons-display-block";       
        $(".panel-buttons").removeClass("panel-buttons-display-none");
        $(".panel-buttons").addClass("panel-buttons-display-block");
        $(".color-no-defyejemplo").removeClass("panel-buttons-display-none");
        $(".color-no-defyejemplo").addClass("panel-buttons-display-block");
            
            
        $("#defyejemplo").prop("checked", false);
    }
     */
    

    /*if($("#pictos").is(':checked')){
        $("#text-pictos").find("span").text("Ocultar pictos"); 
        claseMostrarPictos = "pos-ini-block";
        clasePosicionPictos = "position-img";
        $(".image-picto").removeClass("pos-ini-none");
        $(".image-picto").addClass("pos-ini-block");

        posicionMet = "position-p-img";
        $(".panel-img").removeClass("panel-img");
        $(".panel-img").addClass("position-img");   
        $(".p-met").addClass("position-p-img");
        $("#pictos").prop("checked", false);
    }  */  
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
            $.getJSON('https://holstein.fdi.ucm.es/nlp-api/analisis/'+json.word, function(data) {
                console.log(data);
            });
           
        }

        existMetaphor = false;
        existSimil = false;
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
                        "</div><div class='position-metaphor panel-img mt-3 " + clasePosicionPictos + " ml-2'><img class='image-picto " + claseMostrarPictos + 
                        " result-picto' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img>" +
                        "<p class='word-search " + posicionMet + "'>" + enlace + "</p></div></li><hr>";
                    }else{
                        elemento += "<li><i class='material-icons color-list mr-3'>lens</i>" + palabra + ' ' + phrase + 
                        "<p class='word-search ml-2 mt-3'>" + enlace + "</p></li><hr>";
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
                        "</div><div class='position-metaphor panel-img mt-3 " + clasePosicionPictos + "  ml-2'><img class='image-picto " + claseMostrarPictos + 
                        " result-picto' src='https://holstein.fdi.ucm.es/tfg-analogias/imagenByPalabra/" + enlace + "'></img>" +
                        "<p class='word-search' >" + enlace + "<p></div></li><hr>";
                    }else{
                        elemento += "<li><i class='material-icons color-list mr-3'>lens</i>" + palabra + ' ' + phrase + 
                        "<p class='word-search ml-2 mt-3'>" + enlace + "</p></li><hr>";
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
        elemento += "<div id='panel-button' class='panel-buttons " + clasePanelButtons + "'>" +
        "<div class='dropdown show'><a class='btn btn-def dropdown-toggle' href='#' role='button'  data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
        "Definición y Ejemplo</a><div class='dropdown-menu panel-dropdown-def' aria-labelledby='dropdownMenuLink'><div class='panel-def-example-only-button'>" + definicion + ejemplo;
    } else {
        elemento += "<div class='color-no-defyejemplo pl-3 pr-3 pt-2 pb-2 " + clasePanelButtons + "'>NO HAY DEFINICIÓN NI EJEMPLO</div>"
    }
    
    $("#list-results").append(elemento);
    
 

        
            

    
}