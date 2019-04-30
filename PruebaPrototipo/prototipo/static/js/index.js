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
     /*let elemento = "<h3>" +  Resultados para la palabra + "<p class='ml-2'>" + word + "</p></h3><ul id='list-results'>";
    $(".panel-results").append(elemento); */
    json.allOffsets.forEach(offset => {
        let resultado = json.resultsSynonyms.find(resultSynonym =>{
            return resultSynonym.offset == offset.offset;
        });
        if(resultado != undefined){
            formarFicha(resultado, contador, json.word);
            ++contador;
        }

       
    });

}


function formarFicha(resultado, numTarjeta, palabra){
    let elemento =  "<div id ='card" + numTarjeta + "' class='panel-words mt-4 pt-3 pb-3 col-8 '><div class='number-panel pt-3 ml-3'><p>" + numTarjeta + ".</p></div><div class='results'><p>";
    
    resultado.phraseSynonyms.forEach(phrase =>{
        let enlace = phrase.split(" ").pop();
        phrase = phrase.replace(enlace, "");
        elemento += palabra + ' ' + phrase + "<a href='#'>" + enlace + "</a><br>";
    });
    console.log(elemento);
    $("#list-results").append(elemento);
    
}
   
            