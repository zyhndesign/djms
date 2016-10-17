var orderMgr=(function(config,Functions){
    var orderId=0;

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "sAjaxSource": config.ajaxUrls.getAllOrders,
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
                        var string="";
                        if(oObj.aData.oldStatus!=-1){
                            string='<span class="detailController glyphicon glyphicon-plus"></span>';
                        }

                        return string;
                    }
                },
                { "mDataProp": "order_no"},
                { "mDataProp": "date_submitted"},
                { "mDataProp": "source"},
                { "mDataProp": "status",
                    "fnRender":function(oObj){
                        var string="";
                        switch(oObj.aData.status){
                            case -1:
                                string="废弃";
                                break;
                            case 0:
                                string="待发货";
                                break;
                            case 1:
                                string="完成";
                                break;
                        }

                        return string;
                    }
                },
                { "mDataProp": "memo"},
                { "mDataProp":"opt",
                    "fnRender":function(oObj) {
                        var string="<a href='"+oObj.aData.id+"' class='setStatus'>设置状态</a>&nbsp;";
                        if(oObj.aData.oldStatus==0){
                            string="<a href='"+oObj.aData.id+"' class='addPro'>添加商品</a>&nbsp;"+string;
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
                                response.aaData[i].oldStatus=response.aaData[i].status;
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
        discardOrder:function(id){
            var me=this;
            Functions.showLoading();
            $.ajax({
                url:config.ajaxUrls.discardOrder.replace(":id",id),
                type:"post",
                dataType:"json",
                success:function(response){
                    if(response.data.success){
                        Functions.hideLoading();
                        $().toastmessage("showSuccessToast",config.message.optSuccess);
                        me.tableRedraw();
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }

                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        setStatus:function(orderId){
            $("#setOrderStatusForm").attr("action",config.ajaxUrls.setOrderStatus.replace(":id",orderId));
            $("#setOrderStatusModal").modal("show");
        },
        setStatusSubmit:function(form){
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
                        $("#setOrderStatusModal").modal("hide");
                        me.tableRedraw();
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        addProOutRecord:function(ids){
            var ids=ids.split("/"),
                orderId=ids[0],
                proId=ids[1];
            $("#myProOutForm").attr("action",config.ajaxUrls.addProOutRecord.replace(":id",orderId).replace(":proId",proId));
            $("#proOutModal").modal("show");
        },
        addProRecord:function(orderId){
            $("#myAddProForm").attr("action",config.ajaxUrls.addProToOrder.replace(":id",orderId));
            $("#addProModal").modal("show");
        },
        addProFormSubmit:function(form){
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
                        $("#addProModal").modal("hide");
                        me.tableRedraw();
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        proOutFormSubmit:function(form){
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
                        $("#proOutModal").modal("hide");
                        me.tableRedraw();
                    }else{
                        if(response.data.invalid_serial_no||response.data.duplicate_serial_no){
                            alert("下列产品编号不存在："+response.data.invalid_serial_no.join("/")+
                                "\r\n下列产品已出库："+response.data.duplicate_serial_no.join("/"));
                            Functions.hideLoading();
                        }else{
                            Functions.ajaxReturnErrorHandler(response.data.error_code);
                        }

                    }
                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        removePro:function(el){
            var ids=el.attr("href").split("/"),
                orderId=ids[0],
                proId=ids[1];

            Functions.showLoading();
            $.ajax({
                url:config.ajaxUrls.removeProInOrder.replace(":id",orderId).replace(":proId",proId),
                type:"post",
                dataType:"json",
                success:function(response){
                    if(response.data.success){
                        Functions.hideLoading();
                        $().toastmessage("showSuccessToast",config.message.optSuccess);
                        el.closest("table").remove();
                    }else{
                        Functions.ajaxReturnErrorHandler(response.data.error_code);
                    }

                },
                error:function(){
                    Functions.ajaxErrorHandler();
                }
            });
        },
        removeProOutRecord:function(el){
            var ids=el.attr("href").split("/"),
                orderId=ids[0],
                proId=ids[1],
                serialNo=ids[2];

            Functions.showLoading();
            $.ajax({
                url:config.ajaxUrls.deleteProOutRecord.replace(":id",orderId).replace(":proId",proId),
                type:"post",
                dataType:"json",
                data:{
                    serial_no:serialNo
                },
                success:function(response){
                    if(response.data.success){
                        Functions.hideLoading();
                        $().toastmessage("showSuccessToast",config.message.optSuccess);
                        el.closest("tr").remove();
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
                tr = el.closest('tr')[0];

            if ( this.ownTable.fnIsOpen(tr) ){
                el.removeClass('shown glyphicon-minus').addClass("glyphicon-plus");
                this.ownTable.fnClose( tr );
                orderId=0;
            }else{
                Functions.showLoading();
                orderId=this.ownTable.fnGetData(tr)["id"];

                $.ajax({
                    url:config.ajaxUrls.getProRecordsByOrderId.replace(":id",orderId),
                    type:"get",
                    dataType:"json",
                    success:function(response){
                        if(response.data.success){
                            el.addClass('shown glyphicon-minus').removeClass("glyphicon-plus");
                            me.ownTable.fnOpen( tr, me.detailContent(orderId,response.data.items), 'details' );
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
        detailContent:function(orderId,records){
            var string='<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;width:100%">';

            //for循环添加tr
            for(var i= 0,length=records.length;i<length;i++){
                string+="<tr><td><table style='padding-left:50px;width:100%'><tr><td>"+records[i]["product_name"]+"</td><td>"+records[i]["quantity"]+
                    "</td><td>"+records[i]["unit_price"]+"</td>" +
                    "<td>"+records[i]["amount"]+"</td><td>"+records[i]["memo"]+"</td>" +
                    "<td><a class='addProOut' href='"+orderId+"/"+records[i]["id"]+"'>出货</a>"+
                    "&nbsp;<a class='removePro' href='"+orderId+"/"+records[i]["id"]+"'>删除</a></td></tr>";
                string+="<tr><td colspan='5'><table  cellpadding='5' cellspacing='0' border='0' style='padding-left:100px;width:100%'>";

                for(var l= 0,len=records[i].outstock_serial_no.length;l<len;l++){
                    string+="<tr><td colspan='4'>"+records[i]["outstock_serial_no"][l]+"</td><td>"+
                        "<a class='removeProOut' href='"+orderId+"/"+records[i]["id"]+"/"+records[i]["outstock_serial_no"][l]+"'>删除</a></td></tr>";
                }

                string+="</table></td></td></tr></table></td></tr>";
            }

            return string+"</table>";
        }
    }
})(config,Functions);

$(document).ready(function(){

    orderMgr.createTable();

    $("#date_outstock").val(Functions.formatDate());

    $("#searchBtn").click(function(e){
        orderMgr.tableRedraw();
    });
    $("#myTable").on("click","a.addProOut",function(){

        orderMgr.addProOutRecord($(this).attr("href"));

        return false;
    }).on("click","a.addPro",function(){

            orderMgr.addProRecord($(this).attr("href"));

            return false;
        }).on("click",".removeProOut",function(){
            if(confirm("确认删除吗？")){
                orderMgr.removeProOutRecord($(this));
            }
            return false;
    }).on("click",".removePro",function(){
            if(confirm("确认删除吗？")){
                orderMgr.removePro($(this));
            }
            return false;
        }).on("click",".detailController",function(){
            orderMgr.showDetail($(this));
        }).on("click",".setStatus",function(){
            orderMgr.setStatus($(this).attr("href"));
            return false;
        }).on("click",".discard",function(){
            if(confirm("确认废弃吗？")){
                orderMgr.discardOrder($(this).attr("href"));
            }
            return false;
        });

    $("#quantity,#unit_price").keyup(function(){
        var unit_price=$("#unit_price").val();
        var quantity=$("#quantity").val();

        $("#amount").val((parseFloat(unit_price?unit_price:0)*parseFloat(quantity?quantity:0)).toFixed(2));
    });
    $("#myAddProForm").validate({
        rules:{
            quantity:{
                required:true
            },
            unit_price:{
                required:true
            },
            date_delivered:{
                required:true
            }
        },
        messages:{
            quantity:{
                required:config.validError.required
            },
            unit_price:{
                required:config.validError.required
            },
            date_delivered:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            orderMgr.addProFormSubmit(form);
        }
    });
    $("#myProOutForm").validate({
        rules:{
            serial_no:{
                required:true
            },
            date_outstock:{
                required:true
            }
        },
        messages:{
            serial_no:{
                required:config.validError.required
            },
            date_outstock:{
                required:config.validError.required
            }
        },
        submitHandler:function(form) {
            orderMgr.proOutFormSubmit(form);
        }
    });
    $("#setOrderStatusForm").validate({

        submitHandler:function(form) {
            orderMgr.setStatusSubmit(form);
        }
    });
});
