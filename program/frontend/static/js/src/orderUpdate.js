var orderUpdate=(function(config,Functions){

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
                        Functions.timeoutRedirect("productorders");
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

    $("#source").change(function(){
        if($(this).val()=="线下"){
            $("#order_no").val("O"+Date.now()).attr("readonly","readonly");
        }else{
            $("#order_no").val("").removeAttr("readonly");
        }
    });

    $("#myForm").validate({
        rules:{
            order_no:{
                required:true
            },
            date_submitted:{
                required:true
            }
        },
        messages:{
            order_no:{
                required:config.validError.required
            },
            date_submitted:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            orderUpdate.submitForm(form);
        }
    });
});
