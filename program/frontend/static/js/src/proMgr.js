var proMgr=(function(config,Functions){

    /**
     * 创建datatable
     * @returns {*|jQuery}
     */
    function createTable(){

        var ownTable=$("#myTable").dataTable({
            "bServerSide": true,
            "sAjaxSource": config.ajaxUrls.getAllPro,
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
                { "mDataProp": "drawing",
                    "fnRender":function(oObj) {
                        return  "<img class='thumb' src='"+oObj.aData.drawing+"'>";
                    }
                },
                { "mDataProp": "name"},
                { "mDataProp": "materials_name",
                    "fnRender":function(oObj){
                        return oObj.aData.materials_name.join(",");
                    }
                },
                { "mDataProp": "man_hours"},
                { "mDataProp": "category_name"},
                { "mDataProp": "serial_number"},
                { "mDataProp": "price"},
                { "mDataProp": "reed"},
                { "mDataProp": "attachment",
                    "fnRender":function(oObj){
                        return "<a href='"+oObj.aData.attachment+"'>下载</a>";
                    }
                },
                { "mDataProp": "memo"},
                { "mDataProp":"opt",
                    "fnRender":function(oObj) {
                        var string="<a href='products/"+oObj.aData.id+"/update'>修改</a>";

                        return  string;
                    }
                }
            ] ,
            "fnServerParams": function ( aoData ) {
                aoData.push({
                    "name": "name",
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

    proMgr.createTable();

    $("#searchBtn").click(function(e){
        proMgr.tableRedraw();
    });
});
