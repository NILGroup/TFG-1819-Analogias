$(function() {

    $("#button-accept").on("click", selectOptionHandler);


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