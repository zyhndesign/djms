var proSuccInMgr=(function(config,Functions){

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "sAjaxSource": config.ajaxUrls.getAllProSucc,
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
                { "mDataProp": "serial_no"},
                { "mDataProp": "product_name"},
                { "mDataProp": "date_instock"},
                { "mDataProp": "instock",
                    "fnRender":function(oObj){
                        return oObj.aData.instock?"在库":"出库";
                    }
                },
                { "mDataProp":"opt",
                    "fnRender":function(oObj) {
                        var string="<a href='"+oObj.aData.id+"' class='remove'>删除</a>&nbsp;";

                        return  string;
                    }
                }
            ] ,
            "fnServerParams": function ( aoData ) {
                aoData.push({
                    "name": "content",
                    "value":  $("#name").val()
                },{
                    "name":"stock_status",
                    "value":$("#status").val()
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
        remove:function(id){
            Functions.showLoading();
            var me=this;
            $.ajax({
                url:config.ajaxUrls.deleteProSucc.replace(":id",id),
                type:"post",
                dataType:"json",
                /*data:{
                 id:id
                 },*/
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
        }
    }
})(config,Functions);

$(document).ready(function(){

    proSuccInMgr.createTable();

    $("#searchBtn").click(function(e){
        proSuccInMgr.tableRedraw();
    });
    $("#myTable").on("click","a.remove",function(){
        if(confirm("确定删除吗？")){
            proSuccInMgr.remove($(this).attr("href"));
        }

        return false;
    });
});
