$(document).ready(function () {

       $("#id_first_name").change(function () {
           alert("funcion");
           var name = $(this).val();
           var message1 = "El nombre debe contener sólo caracteres válidos sin espacio";
           var regex =  /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ]*$/;
           var regexNum =  /^[0-9]+$/;
           var vacio = "";
           alert(name);
           if ( !(name.match(regex))){
               $("#error").innerText = message1;
           }
           if (name.length === 0) {
               alert("El nombre no puede estar vacío");
               $("#error").innerText = message1;
           }
       })
    });

