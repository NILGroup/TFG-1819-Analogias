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
       $("#panel-button").css("display" ,"block");
    }else{
      $("#panel-button").css("display", "none");
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


function formarFicha(offset, resultadoSinonimos, resultadoHiponimos, resultadoHiperonimos,  numTarjeta, palabra){
    
    let elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagen/" +  offset.offset + "'></img><div class='results'><p>";
    let definicion = [];
    let ejemplo = [];
    if(resultadoSinonimos != undefined){
        resultadoSinonimos.phraseSynonyms.forEach(phrase =>{

            if(phrase.definition != undefined){
                definicion += "<p><b> Definición:</b><i>" + phrase.definition + "</i></p>";
           }    

           if(phrase.example != undefined){
                ejemplo += "<p><b> Ejemplo:</b><i>" + phrase.example + "</i></p>";
           }

            let enlace = phrase.split(" ").pop();
            phrase = phrase.replace(enlace, "");
            elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagenByPalabra/" + enlace + "'></img></li><br>";
        });

    }
    
    if(resultadoHiponimos != undefined){
       
        resultadoHiponimos.forEach(phrase =>{
            if(phrase.definition.length != 0){
                definicion += "<p><b> Definición:</b><i>" + phrase.definition + "</i></p>";
           }    

           if(phrase.example.length != 0){
                ejemplo += "<p><b> Ejemplo:</b><i>" + phrase.example + "</i></p>";
           }

            phrase.phraseHyponyms.forEach(p =>{              
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
            }); 
        });

    }
   
    if(resultadoHiperonimos != undefined){         
        resultadoHiperonimos.forEach(phrase =>{     

    
            if(phrase.definition.length != 0){
                definicion += "<p><b> Definición:</b><i>" + phrase.definition + "</i></p>";
           }   

           if(phrase.example.length != 0){
                ejemplo += "<p><b> Ejemplo:</b><i>" + phrase.example + "</i></p>";
           }
            phrase.phraseHyperonyms.forEach(p =>{
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
            });     
        });

       
    }
    
    elemento += "<div id='panel-button' class='panel-buttons'>" +
        "<div class='dropdown show'><a class='btn btn-def dropdown-toggle' href='#' role='button'  data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
           "Definición y Ejemplo</a><div class='dropdown-menu panel-dropdown-def' aria-labelledby='dropdownMenuLink'><div class='panel-def-example-only-button'>" + definicion + ejemplo;
        
        
            

    $("#list-results").append(elemento);
    
}
   
            