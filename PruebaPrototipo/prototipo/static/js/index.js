$(function() {

    $("#button-send").on("click", selectOptionHandler);

});

function selectOptionHandler(){

    if($("#mayusculas").is(':checked')){
        console.log(word)
        $("#id_word").val(word).toLowerCase();

    }
}