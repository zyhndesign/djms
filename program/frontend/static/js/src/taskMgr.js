var taskMgr=(function(config,Functions){

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "sAjaxSource": config.ajaxUrls.getAllTasks,
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
                { "mDataProp": "more",
                    "fnRender":function(oObj) {
                        return '<span class="detailController glyphicon glyphicon-plus"></span>';
                    }
                },
                { "mDataProp": "textile_worker_fullname"},
                { "mDataProp": "product_name"},
                { "mDataProp": "date_started"},
                { "mDataProp": "quantity_expected"},
                { "mDataProp": "date_expected"},
                { "mDataProp": "finished",
                    "fnRender":function(oObj){
                        return oObj.aData.finished?"完成":"未完成";
                    }
                },
                { "mDataProp": "memo"},
                { "mDataProp":"opt",
                    "fnRender":function(oObj) {
                        var string="";
                        if(!oObj.aData.oldFinished){
                            string="<a href='tasks/"+oObj.aData.id+"/update'>修改</a>&nbsp;"+
                                "<a href='"+oObj.aData.id+"' class='matOut'>原材料分发</a>&nbsp;"+
                                "<a href='"+oObj.aData.id+"' class='proIn'>收货</a>&nbsp;";
                        }else{
                            string="<a href='"+oObj.aData.id+"' class='checkProIn'>收货记录</a>";
                        }

                        return  string;
                    }
                }
            ] ,
            "fnServerParams": function ( aoData ) {
                aoData.push({
                    "name": "content",
                    "value":  $("#name").val()
                });
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
                            for (var i = 0, iLen = response.aaData.length; i < iLen; i++) {
                                response.aaData[i].opt="opt";
                                response.aaData[i].more="more";
                                response.aaData[i].oldFinished=response.aaData[i].finished;
                            }

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
        matOutFormSubmit:function(form){
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
                        me.tableRedraw();
                        $(form).resetForm();
                        $("#matOutModal").modal("hide");
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        proInFormSubmit:function(form){
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
                        me.tableRedraw();
                        $(form).resetForm();
                        $("#proInModal").modal("hide");
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        checkProIn:function(taskId){
            Functions.showLoading();
            $.ajax({
                url:config.ajaxUrls.getProIn.replace(":id",taskId),
                type:"get",
                dataType:"json",
                success:function(response){
                    if(response.data.success){
                        Functions.hideLoading();
                        $("#proInForm").attr("action",config.ajaxUrls.addProIn.replace(":id",taskId));
                        $("#date_finished").val(response.data.result.date_finished);
                        $("#quantity_qualified").val(response.data.result.quantity_qualified);
                        $("#quantity_defective").val(response.data.result.quantity_defective);
                        $("#level").val(response.data.result.level);
                        $("#proInModal").modal("show");
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }

                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        showDetail:function(el){
            var me=this,
                tr = el.closest('tr')[0],
                taskId;

            if ( this.ownTable.fnIsOpen(tr) ){
                el.removeClass('shown glyphicon-minus').addClass("glyphicon-plus");
                this.ownTable.fnClose( tr );
            }else{
                Functions.showLoading();
                taskId=this.ownTable.fnGetData(tr)["id"];

                $.ajax({
                    url:config.ajaxUrls.getMatOut.replace(":id",taskId),
                    type:"get",
                    dataType:"json",
                    success:function(response){
                        if(response.data.success){
                            el.addClass('shown glyphicon-minus').removeClass("glyphicon-plus");
                            me.ownTable.fnOpen( tr, me.detailContent(response.data.materials), 'details' );
                            Functions.hideLoading();
                        }else{
                            Functions.ajaxReturnErrorHandler(response.data.error_code);
                        }

                    },
                    error:function(){
                        Functions.ajaxErrorHandler();
                    }
                });

            }
        },
        detailContent:function(records){
            var string='<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;width:100%">';

            //for循环添加tr
            for(var i= 0,length=records.length;i<length;i++){
                string+="<tr><td>"+records[i].material_name+"</td><td>"+records[i].amount+"</td>" +
                    "<td>"+records[i].unit+"</td></tr>";
            }

            return string+"</table>";
        }
    }
})(config,Functions);

$(document).ready(function(){

    taskMgr.createTable();

    $("#searchBtn").click(function(e){
        taskMgr.tableRedraw();
    });
    $("#myTable").on("click","a.proIn",function(){
        $("#proInModal").modal("show");
        $("#proInForm").attr("action",config.ajaxUrls.addProIn.replace(":id",$(this).attr("href")));
        return false;
    }).on("click","a.matOut",function(){
            $("#matOutForm").attr("action",config.ajaxUrls.addMatOut.replace(":id",$(this).attr("href")));
            $("#matOutModal").modal("show");
            return false;
        }).on("click","a.checkProIn",function(){
            taskMgr.checkProIn($(this).attr("href"));
            return false
        }).on("click",".detailController",function(){
            taskMgr.showDetail($(this));
        });

    $("#matOutForm").validate({
        rules:{
            amount:{
                required:true
            }
        },
        messages:{
            amount:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            taskMgr.matOutFormSubmit(form);
        }
    });

    $("#proInForm").validate({
        rules:{
            date_finished:{
                required:true
            },
            amount_qualified:{
                required:true
            },
            amount_defective:{
                required:true
            }
        },
        messages:{
            date_finished:{
                required:config.validError.required
            },
            amount_qualified:{
                required:config.validError.required
            },
            amount_defective:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            taskMgr.proInFormSubmit(form);
        }
    });
});
