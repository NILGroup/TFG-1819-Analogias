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
    let contador = 1;
    console.log(json);
     /*let elemento = "<h3>" +  Resultados para la palabra + "<p class='ml-2'>" + word + "</p></h3><ul id='list-results'>";
    $(".panel-results").append(elemento); */
    json.allOffsets.forEach(offset => {
        let arrayHiponimos = [];
        let resultadoSinonimos = json.resultsSynonyms.find(resultSynonym =>{
            return resultSynonym.offset == offset.offset;
        });
        let resultadoHiponimos = json.resultsHyponyms.forEach(resultHyponym =>{
            
            if (resultHyponym.offsetFather == offset.offset){
                arrayHiponimos.push(resultHyponym);
            };
        });
       

        if(resultadoSinonimos != undefined || arrayHiponimos.size > 0){
            formarFicha(resultadoSinonimos, arrayHiponimos, contador, json.word);
            
            ++contador;
        }

       
    });

}


function formarFicha(resultadoSinonimos, resultadoHiponimos, numTarjeta, palabra){
    let elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><div class='results'><p>";
    console.log("RESULTADO SINONIMOS");
    console.log(resultadoSinonimos);
    console.log("RESULTADO HIPONIMOS");
    console.log(resultadoHiponimos);
    if(resultadoSinonimos != undefined){
        resultadoSinonimos.phraseSynonyms.forEach(phrase =>{
        
            let enlace = phrase.split(" ").pop();
            phrase = phrase.replace(enlace, "");
            elemento += palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><br>";
        });
    }
    
    if(resultadoHiponimos != undefined){
        resultadoHiponimos.forEach(phrase =>{
            phrase.phraseHyponyms.forEach(p =>{
                let enlace = p.split(" ").pop();
                phrase = p.replace(enlace, "");
                elemento += palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><br>";
            });
            
           
        });
    }
   
    
    $("#list-results").append(elemento);
    
}
   
            