var error = 0;
$(document).ready(function () {

 if (error == 1){
  error = 0;
 } 

 $("#id_email").change(function () {
       var email = $(this).val();
       var message1 = "Introduzca un correo electrónico válido";
       var regexEmail =  /^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$/;
       var form = $(this).closest("form");

       if ( !(email.match(regexEmail))){
           error_email.style.color = "red";
           error_email.style.border = "1px solid #ccc";
           error_email.innerText = message1;
           id_email.style.border = "2px solid red";
           error = 1;
       }
       else{
           $.ajax({
               url: form.attr("data-forgot-email-url"),
               data: {
                   email: email
               },
               type: 'POST',
               dataType: 'json',
               success: function (data) {
                   emailExist = data.email_exists;
                   if ((emailExist) == false) {
                       error_email.innerHTML = data.error;
                       error_email.style.color = "red";
                       error_email.style.border = "1px solid #ccc";
                       error = 1;
                   }
               }
           })

       }
        /*Sirve para limpiar la pantalla cuando hay un error*/
        $("#id_email").click(function() {
          if (error == 1){
            $("#error_email").empty();
            error_email.style.border = "transparent";
            $("#id_email").val("");
            id_email.style.border = "2px solid #ccc";
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
           error_username.style.border = "1px solid #ccc";
           error_username.innerText = message1;
           id_username.style.border = "2px solid red";
           error = 1;
       }    

        $("#id_username").click(function() {
          if (error == 1){
            $("#error_username").empty();
            error_username.style.border = "transparent";
            id_username.style.border = "2px solid #ccc";
            $("#id_username").val(""); 
            error = 0;
          }
        });
  });

  $("#id_first_name").change(function () {
      var name = $(this).val();
      var message1 = "El nombre debe contener sólo caracteres válidos sin espacio";
      var regexName =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
      var regexNum =  /^[0-9]+$/;
      if ( !(name.match(regexName))){
          error_name.style.color = "red";
          error_name.style.border = "1px solid #ccc";
          error_name.innerHTML = message1;
          id_first_name.style.border = "2px solid red";
          error = 1;
      }

      $("#id_first_name").click(function() {
          if (error == 1) {
              $("#error_name").empty();
              error_name.style.border = "transparent";
              $("#id_first_name").val("");
              id_first_name.style.border = "2px solid #ccc";
              error= 0;
          }
      });
  });

  $("#id_last_name").change(function () {
      var lastname = $(this).val();
      var message1 = "El Apellido debe contener sólo caracteres válidos sin espacio";
      var regexLastname =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
      if ( !(lastname.match(regexLastname))){
          error_lastname.style.color = "red";
          error_lastname.style.border = "1px solid #ccc";
          error_lastname.innerHTML = message1;
          id_last_name.style.border = "2px solid red";
          error= 1;
      }
      $("#id_last_name").click(function() {
          if(error == 1) {
              $("#error_lastname").empty();
              error_lastname.style.border = "transparent";
              $("#id_last_name").val("");
              id_last_name.style.border = "2px solid #ccc";
              error= 0;
          }
      });
  });

  $("#id_password").change(function () {
      var password = $(this).val();
      var message1 = "La contraseña debe tener una longitud entre seis y doce caracteres, alfanumérica, con mínimo una letra " +
                      "mayúscula y contener alguno de estos caracteres especiales: $@!%.#_*?&";
      var regexPassword = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!%.#_*?&]).{6,12}$/;
      if (!(password.match(regexPassword))) {
          error_password.style.color = "red";
          error_password.style.border = "1px solid #ccc";
          error_password.innerHTML = message1;
          id_password.style.border = "2px solid red";
          error=1;
      }

      $("#id_password").click(function() {
          if(error == 1) {
              $("#error_password").empty();
              error_password.style.border = "transparent";
              $("#id_password").val("");
              id_password.style.border = "2px solid #ccc";
              error = 0;
          }
    });

  });

  $("#id_password2").change(function () {
      var password2 = $(this).val();
      var password = $("#id_password").val();
      var message1 = "Las contraseñas no coinciden, por favor verifique";
      if (password2 && (password2 !== password)){
          error_password2.style.color = "red";
          error_password2.style.border = "1px solid #ccc";
          error_password2.innerHTML = message1;
          id_password2.style.border = "2px solid red";
          error = 1;
      }
      $("#id_password2").click(function() {
          if (error = 1) {
              $("#error_password2").empty();
              error_password2.style.border = "transparent";
              $("#id_password2").val("");
              id_password2.style.border = "2px solid #ccc";
          }
    });
  });

/*´Permite mostrar y ocultar la contraseña*/
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

   $("#show-hide-passwd2").click(function(e){
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