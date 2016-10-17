var proCategoryMgr=(function(config,Functions){

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "bPaginate": false,
            "sAjaxSource": config.ajaxUrls.getAllProCategories,
            "bInfo":true,
            "bLengthChange": false,
            "bFilter": false,
            "bSort":false,
            "bAutoWidth": false,
            "iDisplayLength":config.perLoadCount.table,
            "sPaginationType":"full_numbers",
            "oLanguage": {
                "sUrl":config.dataTable.langLocation
            },
            "aoColumns": [
                { "mDataProp": "name"},
                { "mDataProp": "description"}
            ] ,
            "fnServerParams": function ( aoData ) {

            },
            "fnServerData": function(sSource, aoData, fnCallback) {

                //回调函数
                $.ajax({
                    "dataType":'json',
                    "type":"get",
                    "url":sSource,
                    "data":aoData,
                    "success": function (response) {
                        response=response.data;
                        if(response.success===false){
                            Functions.ajaxReturnErrorHandler(response.error_code);
                        }else{
                            var json = {
                                "sEcho" : response.sEcho
                            };

                            json.aaData=response.aaData;
                            json.iTotalRecords = response.iTotalRecords;
                            json.iTotalDisplayRecords = response.iTotalDisplayRecords;
                            fnCallback(json);
                        }

                    }
                });
            },
            "fnFormatNumber":function(iIn){
                return iIn;
            }
        });

        return ownTable;
    }

    return {
        ownTable:null,
        createTable:function(){
            this.ownTable=createTable();
        },
        tableRedraw:function(){
            this.ownTable.fnSettings()._iDisplayStart=0;
            this.ownTable.fnDraw();
        },
        submitForm:function(form){
            var me=this;
            Functions.showLoading();
            $(form).ajaxSubmit({
                dataType:"json",
                headers:{
                    "X-Requested-With":"XMLHttpRequest"
                },
                success:function(response){
                    if(response.data.success){
                        Functions.hideLoading();
                        $().toastmessage("showSuccessToast",config.message.optSuccess);
                        $(form).resetForm();
                        me.tableRedraw();
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

    proCategoryMgr.createTable();

    $("#myForm").validate({
        rules:{
            name:{
                required:true,
                maxlength:32
            }
        },
        messages:{
            name:{
                required:config.validError.required,
                maxlength:config.validError.maxLength.replace("${max}",32)
            }
        },
        submitHandler:function(form) {
            if(confirm("分类不能修改和删除，请仔细核对信息后再添加")){
                proCategoryMgr.submitForm(form);
            }else{
                return false;
            }
        }
    });
});
