var matInUpdate=(function(config,Functions){

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
                        Functions.timeoutRedirect("materialorders");
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        getSupByMatId:function(matId){
            $.ajax({
                method:"get",
                dataType:"json",
                url:config.ajaxUrls.getSpByMaterialId.replace(":id",matId),
                success:function(response){
                    if(response.data.success){
                        var string="";
                        for(var i= 0,len=response.data.sp.length;i<len;i++){
                            string+="<option value='"+response.data.sp[i]["id"]+"'>"+response.data.sp[i]["name"]+"</option>";
                        }
                        $("#sp").html(string);
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            })
        }
    }
})(config,Functions);

$(document).ready(function(){

    $("#material").change(function(){
        matInUpdate.getSupByMatId($(this).val());
    });
    matInUpdate.getSupByMatId($("#material").val());


    $("#amount_buy,#unit_price").keyup(function(){
        var unit_price=$("#unit_price").val();
        var quantity=$("#amount_buy").val();

        $("#amount_price").val((parseFloat(unit_price?unit_price:0)*parseFloat(quantity?quantity:0)).toFixed(2));
    });

    $("#myForm").validate({
        rules:{
            amount_by:{
                required:true
            },
            unit_price:{
                required:true
            },
            date_buy:{
                required:true
            }
        },
        messages:{
            amount_by:{
                required:config.validError.required
            },
            unit_price:{
                required:config.validError.required
            },
            date_buy:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            matInUpdate.submitForm(form);
        }
    });
});
