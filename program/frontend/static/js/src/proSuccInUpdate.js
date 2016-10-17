var proSuccInUpdate=(function(config,Functions){

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
                        Functions.timeoutRedirect("instocks");
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
            amount:{
                required:true
            },
            date_instock:{
                required:true
            }
        },
        messages:{
            amount:{
                required:config.validError.required
            },
            date_instock:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            proSuccInUpdate.submitForm(form);
        }
    });
});
