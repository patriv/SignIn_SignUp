var error = 0;

function styleError(id, NameError, message1) {
    NameError.innerHTML = message1;
    NameError.style.visibility = "visible";
    id.style.border = "2px solid red";
    error= 1;
}

function clearScreen(id, NameError){
    if (error === 1){
        $("#error_email").empty();
        error_email.style.border = "transparent";
        $("#id_email").val("");
        id_email.style.border = "2px solid #ccc";
        $("#error_email").fadeToggle(0);
        error_email.style.visibility="hidden";
        error = 0;
    }
}


$(document).ready(function () {
    if (error === 1){
        error = 0;
    }

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
          if(error === 1) {
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

      if (current === 'hide'){
        $(this).prev().attr('type','text');
        $(this).removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close').attr('action','show');
      }
      if (current === 'show'){
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