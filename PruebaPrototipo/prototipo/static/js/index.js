$(function() {

    $("#button-accept").on("click", selectOptionHandler);
    $("#button-send").on("click", showCardHandler)

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


function showCardHandler(){

    let data = JSON.parse("resultsSynonyms")
    console.log(data)
    /*let card = "<div id='card' class='panel-words mt-4 pt-3 pb-3 col-8'><div class='results'>hola</div></div>"
    console.log("CARD")
    $("#list-results").append(card)*/
}