var saleStat=(function(config,Functions){

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "sAjaxSource": config.ajaxUrls.getAllPosts,
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
                { "mDataProp": "material_name"},
                { "mDataProp": "sp_name"},
                { "mDataProp": "amount_buy"},
                { "mDataProp": "unit"},
                { "mDataProp": "unit_price"},
                { "mDataProp": "amount_price"},
                { "mDataProp": "date_buy"},
                { "mDataProp": "memo"},
                { "mDataProp":"opt",
                    "fnRender":function(oObj) {
                        var string="<a href='"+oObj.aData.id+"' class='remove'>删除</a>&nbsp;";

                        return  string;
                    }
                }
            ] ,
            "fnServerParams": function ( aoData ) {
                aoData.push({
                    "name": "startDate",
                    "value":  $("#startDate").val()
                },{
                    "name": "endDate",
                    "value": $("#endDate").val()
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

                $("#currentStartDate").text($("#startDate").val()?$("#startDate").val():"1970-01-01");
                $("#currentEndDate").text($("#endDate").val()?$("#endDate").val():Functions.formatDate());
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

    //saleStat.createTable();

    $("#searchBtn").click(function(e){
        saleStat.tableRedraw();
    });
});
