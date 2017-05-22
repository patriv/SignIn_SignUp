var error = 0;
$(document).ready(function () {

 if (error == 1){
  error = 0;
 } 

 $("#id_email").change(function () {
       var email = $(this).val();
       var message1 = "Introduzca un correo electrónico válido";
       var regexEmail =  /^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$/;

       if ( !(email.match(regexEmail))){
           error_email.style.color = "red";
           error_email.style.border = "1px solid black";          
           error_email.innerText = message1;
           id_email.style.border = "2px solid red";
           error = 1;
       }    
          
          
        $("#id_email").click(function() {
          if (error == 1){
            $("#error_email").empty();
            error_email.style.border = "transparent";
            id_email.style.border = "inherit";
            $("#id_email").val(""); 
            error = 0;
          }
        });

     
  });


  $("#id_username").change(function () {
       var username = $(this).val();
       var message1 = "Introduzca un username válido";
       var regexEmail =  /^[a-zA-Z0-9\._-]{2,}$/;


       if ( !(username.match(regexEmail))){
           error_username.style.color = "red";
           error_username.style.border = "1px solid black";          
           error_username.innerText = message1;
           id_username.style.border = "2px solid red";
           error = 1;
       }    
          
          
        $("#id_username").click(function() {
          if (error == 1){
            $("#error_username").empty();
            error_username.style.border = "transparent";
            id_username.style.border = "inherit";
            $("#id_username").val(""); 
            error = 0;
          }
        });

     
  });


   $("#show-hide-passwd").click(function(e){
      e.preventDefault();
      var current = $(this).attr('action');
    
      if (current == 'hide'){
      
        $(this).prev().attr('type','text');
        $(this).removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close').attr('action','show');
         

      } 

      if (current == 'show'){
        $(this).prev().attr('type','password');
        $(this).removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open').attr('action','hide');

      }

    });

});