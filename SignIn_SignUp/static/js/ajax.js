$(document).ready(function(){

    $("#aj").click(function(){

        $.ajax(

            {

                url: "static/js/helloWord.txt",

                success: function(result){
                    $("#view").html(result);

                },

                error: function(result){

                    $("#view").html("ERROR");

                }

            });

        });

    });


$(document).ready(function(){

    $("#guardar").click(function(){

        $.ajax(

            {

                success: function(){
                    $("#register").html("Registrado!");

                },

                error: function(result){

                    $("#register").html("ERROR");

                }

            });

        });

    });