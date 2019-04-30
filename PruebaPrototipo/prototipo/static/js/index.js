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


    /*if($("#defyejemplo").is(':checked')){
       $("#panel-button").css("display" ,"block");
    }else{
      $("#panel-button").css("display", "none");
    }*/
}


function showCardHandler(event){

    event.preventDefault();
    let word = $("#formulario").find("p").find("input").val();
    
    console.log(word);
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
     /*let elemento = "<h3>" +  Resultados para la palabra + "<p class='ml-2'>" + word + "</p></h3><ul id='list-results'>";
    $(".panel-results").append(elemento); */
    json.allOffsets.forEach(offset => {
        let arrayHiponimos = [];
        let arrayHiperonimos = [];
        
        let resultadoSinonimos = json.resultsSynonyms.find(resultSynonym =>{
            return resultSynonym.offset == offset.offset;
        });
        
        json.resultsHyponyms.forEach(resultHyponym =>{            
            if (resultHyponym.offsetFather == offset.offset){
                arrayHiponimos.push(resultHyponym);
            };
        });

        json.resultsHyperonyms.forEach(resultHyperonym =>{            
            if (resultHyperonym.offsetFather == offset.offset){
                arrayHiperonimos.push(resultHyperonym);
            };
        });
       

        if(resultadoSinonimos != undefined || arrayHiponimos.length > 0 || arrayHiperonimos.length > 0){
            formarFicha(offset, resultadoSinonimos, arrayHiponimos, arrayHiperonimos, contador, json.word);
            
            ++contador;
        }

       
    });

}


function formarFicha(offset, resultadoSinonimos, resultadoHiponimos, resultadoHiperonimos,  numTarjeta, palabra){

    let elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagen/" +  offset.offset + "'></img><div class='results'><p>";
   
    if(resultadoSinonimos != undefined){
        resultadoSinonimos.phraseSynonyms.forEach(phrase =>{
           
            let enlace = phrase.split(" ").pop();
            phrase = phrase.replace(enlace, "");
            elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><img class='image-picto ml-3' src='http://127.0.0.1:8000/imagen/" + resultadoSinonimos.offset + "'></img></li><br>";
        });
    }
    
    if(resultadoHiponimos != undefined){
        resultadoHiponimos.forEach(phrase =>{
            phrase.phraseHyponyms.forEach(p =>{
                console.log("SINONIMOS");
                console.log(resultadoHiponimos);
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
            }); 
        });
    }
   
    if(resultadoHiperonimos != undefined){
        resultadoHiperonimos.forEach(phrase =>{
            phrase.phraseHyperonyms.forEach(p =>{
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                elemento += "<li>" + palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a></li><br>";
            }); 
        });
    }
    
    $("#list-results").append(elemento);
    
}
   
            