$(document).ready(function(){
    
    (function($) {
        "use strict";

    
    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                name: {
                    required: true,
                    minlength: 2
                },
                subject: {
                    required: true,
                    minlength: 4
                },
                number: {
                    required: true,
                    minlength: 5
                },
                email: {
                    required: true,
                    email: true
                },
                message: {
                    required: true,
                    minlength: 20
                }
            },
            messages: {
                name: {
                    required: "Vamos, tienes un nombre, ¿no?",
                    minlength: "Tu nombre debe consistir en al menos 2 caracteres"
                },
                subject: {
                    required: "Vamos, tienes un asunto, ¿no?",
                    minlength: "Tu asunto debe consistir en al menos 4 caracteres"
                },
                number: {
                    required: "Vamos, tienes un número, ¿no?",
                    minlength: "Tu número debe consistir en al menos 5 caracteress"
                },
                email: {
                    required: "Sin correo electrónico, no hay mensaje"
                },
                message: {
                    required: "um... sí, tienes que escribir algo para enviar este formulario.",
                    minlength: "¿Eso es todo? ¿En serio?"
                }
            },
            submitHandler: function(form) {
                $(form).ajaxSubmit({
                    type:"POST",
                    data: $(form).serialize(),
                    url:"contact_process.php",
                    success: function() {
                        $('#contactForm :input').attr('disabled', 'disabled');
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor','default');
                            $('#success').fadeIn()
                            $('.modal').modal('hide');
		                	$('#success').modal('show');
                        })
                    },
                    error: function() {
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $('#error').fadeIn()
                            $('.modal').modal('hide');
		                	$('#error').modal('show');
                        })
                    }
                })
            }
        })
    })
        
 })(jQuery)
})