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
        success: function (json){
            console.log(json);
        },
        error: function(data, jqXHR, textStatus, errorThrown){
            console.log(data);

        }
     });


}