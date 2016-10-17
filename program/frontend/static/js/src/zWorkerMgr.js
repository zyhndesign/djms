var zWorkerMgr=(function(config,Functions){

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "sAjaxSource": config.ajaxUrls.getAllZWorkers,
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
                { "mDataProp": "fullname"},
                { "mDataProp": "idcard"},
                { "mDataProp": "tel"},
                { "mDataProp": "address"},
                { "mDataProp": "is_manager",
                    "fnRender":function(oObj){
                        return oObj.aData.is_manager?"是":"否";
                    }
                },
                { "mDataProp": "manager_fullname"},
                { "mDataProp": "memo"},
                { "mDataProp":"opt",
                    "fnRender":function(oObj) {
                        var string="<a href='workers/"+oObj.aData.id+"/update'>修改</a>";

                        return  string;
                    }
                }
            ] ,
            "fnServerParams": function ( aoData ) {
                aoData.push({
                    "name": "fullname",
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
        }
    }
})(config,Functions);

$(document).ready(function(){

    zWorkerMgr.createTable();

    $("#searchBtn").click(function(e){
        zWorkerMgr.tableRedraw();
    });
});
