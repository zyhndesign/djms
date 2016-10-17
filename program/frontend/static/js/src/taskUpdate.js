var taskUpdate=(function(config,Functions){

    return {
        submitForm:function(form){
            Functions.showLoading();
            $(form).ajaxSubmit({
                dataType:"json",
                headers:{
                    "X-Requested-With":"XMLHttpRequest"
                },
                success:function(response){
                    if(response.data.success){
                        $().toastmessage("showSuccessToast",config.message.optSuccRedirect);
                        Functions.timeoutRedirect("tasks");
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        }
    }
})(config,Functions);

$(document).ready(function(){

    $("#myForm").validate({
        rules:{
            date_started:{
                required:true
            },
            amount_expected:{
                required:true
            },
            date_expected:{
                required:true
            }
        },
        messages:{
            date_started:{
                required:config.validError.required
            },
            amount_expected:{
                required:config.validError.required
            },
            date_expected:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            taskUpdate.submitForm(form);
        }
    });
});
