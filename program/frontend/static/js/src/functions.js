/**
 * Created with JetBrains WebStorm.
 * User: ty
 * Date: 14-10-13
 * Time: 上午9:26
 * To change this template use File | Settings | File Templates.
 */
var Functions=(function(){

    //浏览器前缀
    var prefixes=["Moz",'webkit','ms','O'];

    return {
        /**
         * 获取浏览器前缀
         * @returns prefix {string}
         */
        getPrefix:function(){
            var length=prefixes.length;
            var prefix="";
            for(var i=0;i<length;i++){
                if((prefixes[i]+"Animation") in document.body.style){
                    prefix=prefixes[i];
                }
            }

            return prefix;
        },
        /**
         * 3秒跳转
         * @param url 需要跳转到的url
         */
        timeoutRedirect:function(url){
            setTimeout(function(){
                window.location.href=url;
            },3000);
        },
        /**
         * 产生随机数，可以带前缀
         * @returns retValue {string}
         */
        getRandom:function(){
            var date = new Date();
            var mo = (date.getMonth() + 1) < 10 ? ('0' + '' + (date.getMonth() + 1)) : date.getMonth() + 1;
            var dd = date.getDate() < 10 ? ('0' + '' + date.getDate()) : date.getDate();
            var hh = date.getHours() < 10 ? ('0' + '' + date.getHours()) : date.getHours();
            var mi = date.getMinutes() < 10 ? ('0' + '' + date.getMinutes()) : date.getMinutes();
            var ss = date.getSeconds() < 10 ? ('0' + '' + date.getSeconds()) : date.getSeconds();
            var retValue = date.getFullYear() + '' + mo + '' + dd + '' + hh + '' + mi + '' + ss + '';
            for (var j = 0; j < 4; j++) {
                retValue += '' + parseInt(10 * Math.random()) + '';
            }
            if (arguments.length == 1) {
                return arguments[0] + '' + retValue;
            }else{
                return retValue;
            }
        },
        /**
         * 获取邮箱的域名主体部分
         * @param email {string} 需要获取的邮箱
         * @returns domain {string}
         */
        getEmailDomain:function(email){
            var domain=email.substring(email.indexOf("@")+1);
            domain=domain.substring(0,domain.lastIndexOf("."));
            domain=domain.replace(/vip.|.com|.cn/g,"");
            return domain;
        },
        /**
         * 格式化日期
         * @param format {string} 格式化
         * y:四位数的年份
         * m:两位数的月份
         * d:两位数的日期
         * h:两位数的时间
         * i:两位数的分钟
         * s:两位数的秒钟
         * 支持格式:
         * @param dateTime {number} 毫秒表示的日期
         * @returns string {string}格式好的字符串日期，默认是2014-09-10 12:03:23格式
         */
        formatDate:function(format,dateTime){
            var string,currentDate,year,month,day, h, m, s,fYear,fMonth,fDay,fH,fM,fS;

            if(typeof format ==="number"){
                dateTime=format;
                format=null;
            }

            currentDate =dateTime?new Date(dateTime):new Date();
            fYear=currentDate.getFullYear();
            year=fYear.toString().slice(2);
            fMonth=month=currentDate.getMonth()+1;
            fDay=day=currentDate.getDate();
            fH=h=currentDate.getHours();
            fM=m=currentDate.getMinutes();
            fS=s=currentDate.getSeconds();

            if(fMonth<10){
                fMonth="0"+fMonth;
            }
            if(fDay<10){
                fDay="0"+fDay;
            }
            if(fH<10){
                fH="0"+fH;
            }
            if(fM<10){
                fM="0"+fM;
            }
            if(fS<10){
                fS="0"+fS;
            }

            switch(format){
                case "y-m-d h:m":
                    string=fYear+"-"+fMonth+"-"+fDay+" "+fH+":"+fM;
                    break;
                case "y/m/d h:m:s":
                    string=fYear+"/"+fYear+"/"+fDay+" "+fH+":"+fH+":"+fH;
                    break;
                case "y/m/d h:m":
                    string=fYear+"/"+fMonth+"/"+fDay+" "+fH+":"+fM;
                    break;
                default :
                    string=fYear+"-"+fMonth+"-"+fDay;
                    break;
            }

            return string;
        },
        /**
         * 设置cookie
         * @param name {string} cookie的名称
         * @param value {string} cookie的值
         * @param days {number} cookie的保存时间
         */
        setCookie:function(name,value,days){
            var date = new Date();
            date.setTime(date.getTime()+(days*24*60*60*1000));
            var thisCookie = name + "=" + encodeURIComponent(value) +
                ((days) ? "; expires=" + date.toGMTString() : "");
            document.cookie = thisCookie;
        },
        /**
         * 获取cookie
         * @param name {string} cookie的名称
         * @returns {*}
         */
        getCookie:function(name){
            var nameSG = name + "=";
            if (document.cookie == null || document.cookie.indexOf(nameSG) == -1){
                return null;
            }


            var ca = document.cookie.split(';');
            for(var i=0; i<ca.length; i++) {
                var c = ca[i];
                if (c.charAt(0)==' '){
                    c = c.substring(1,c.length);
                }
                if (c.indexOf(nameSG) == 0){
                    return decodeURIComponent(c.substring(nameSG.length,c.length));
                }
            }

            return null;
        },
        /**
         * 删除cookie
         * @param name {string} cookie的名称
         */
        deleteCookie:function(name){
            var exp = new Date();
            exp.setTime(exp.getTime() - 1);
            var oldValue=this.getCookie(name);
            if(oldValue!=null){
                document.cookie= name + "="+oldValue+";expires="+exp.toGMTString();
            }
        },
        /**
         * 获取文件的信息
         * @param fileName
         * @returns {{filePath: string, filename:string, ext: string}}
         */
        getFileInfo:function(fileName){
            var extPos=fileName.lastIndexOf(".");
            var pathPost=fileName.lastIndexOf("/");
            return {
                filePath:pathPost!=-1?fileName.substring(0,pathPost):"",
                filename:fileName.substring(pathPost+1,extPos),
                ext:fileName.substring(extPos+1)
            }
        },
        /**
         * 检测是否是移动设备
         * @returns {boolean}
         */
        checkMobile:function(){
            var userAgentList = new Array("2.0 MMP", "240320", "AvantGo","BlackBerry", "Blazer",
                "Cellphone", "Danger", "DoCoMo", "Elaine/3.0", "EudoraWeb", "hiptop", "IEMobile", "KYOCERA/WX310K", "LG/U990",
                "MIDP-2.0", "MMEF20", "MOT-V", "NetFront", "Newt", "Nintendo Wii", "Nitro", "Nokia",
                "Opera Mini", "Opera Mobi",
                "Palm", "Playstation Portable", "portalmmm", "Proxinet", "ProxiNet",
                "SHARP-TQ-GX10", "Small", "SonyEricsson", "Symbian OS", "SymbianOS", "TS21i-10", "UP.Browser", "UP.Link",
                "Windows CE", "WinWAP", "Android", "iPhone", "iPod", "iPad", "Windows Phone", "HTC"/*, "GTB"*/);
            var appNameList = new Array("Microsoft Pocket Internet Explorer");

            var userAgent = navigator.userAgent.toString();
            var appName = navigator.appName.toString();
            var agentLength=userAgentList.length,appLength=appNameList.length;
            var i= 0,j=0;

            for (; i<agentLength; i++) {
                if (userAgent.indexOf(userAgentList[i]) >= 0) {
                    return true;
                }
            }

            for (; j<appLength; j++) {
                if (appName.indexOf(appNameList[j]) >= 0) {
                    return true;
                }
            }

            return false;
        },
        /**
         * 显示loading遮盖层
         */
        showLoading:function(){
            $("#loading").removeClass("hidden");
        },
        /**
         * 隐藏loading遮盖层
         */
        hideLoading:function(){
            $("#loading").addClass("hidden");
        },
        /**
         * ajax网络错误处理
         */
        ajaxErrorHandler:function(){
            this.hideLoading();
            $().toastmessage("showErrorToast",config.message.networkError);
        },
        /**
         * ajax后台返回错误处理
         * @param errorCode {string} 错误代码
         */
        ajaxReturnErrorHandler:function(errorCode){
            var me=this;
            var message="";
            switch(errorCode){
                case "UNAUTHORIZED":
                    message=config.message.timeout;
                    this.timeoutRedirect("./",true);
                    break;
                case "NOT_FOUND":
                    message=config.message.notFound;
                    me.timeoutRedirect("./");
                    break;
                case "MATERIAL_NOT_ENOUGH":
                    message=config.message.matNotEnough;
                    break;
                default :
                    message=config.message.systemError;
                    break;
            }
            this.hideLoading();
            $().toastmessage("showErrorToast",message);
        },
        /**
         * plupload版本1.5.7
         * @param params
         * @returns {plupload.Uploader}
         */
        createUploader:function(params){
            var uploader = new plupload.Uploader({
                runtimes:"html5",
                multi_selection:params.multiSelection?params.multiSelection:false,
                max_file_size:params.size,
                browse_button:params.btn,
                container:params.container,
                url:params.url,
                unique_names:false,
                //flash_swf_url:'/lotusprize/js/lib/plupload.flash.swf',
                multipart_params:params.multipartParams,
                filters:[
                    {title:"Media files", extensions:params.filter}
                ]
            });

            //初始化
            uploader.init();

            //文件添加事件
            uploader.bind("FilesAdded", function (up, files) {
                if(typeof params.fileAddedCallback === "function"){
                    params.fileAddedCallback(up,files);
                }

                up.start();
            });

            uploader.bind("UploadProgress", function (up, file) {
                if(typeof params.progressCallback ==="function"){
                    params.progressCallback(file);
                }
            });

            //出错事件
            uploader.bind("Error", function (up, err) {
                var message=err.message;
                if(message.match("Init")==null){
                    if(message.match("size")){
                        $().toastmessage("showErrorToast",config.message.uploadSizeError.replace("${value}",params.size));
                    }else if(message.match("extension")){
                        $().toastmessage("showErrorToast",config.message.uploadExtensionError.replace("${value}",params.filter));
                    }else{
                        $().toastmessage("showErrorToast",config.message.optError);
                    }
                }
                up.refresh();
            });

            //上传完毕事件
            uploader.bind("FileUploaded", function (up, file, res) {
                res=JSON.parse(res.response);
                if(typeof params.uploadedCallback === "function"){
                    params.uploadedCallback(file,res);
                }
            });


            return uploader;
        },

        /**
         * plupload版本1.2.1,采用all版本，需要使用qiniu.js
         * @param params
         * @returns {*}
         */
        createQiNiuUploader:function(params){
            var uploader = Qiniu.uploader({
                runtimes: 'html5',    //上传模式,依次退化
                browse_button: params.btn,       //上传选择的点选按钮，**必需**
                uptoken_url:  params.uploadUrl,
                multi_selection:params.multiSelection?params.multiSelection:false,
                domain:params.domain,
                container: params.container,           //上传区域DOM ID，默认是browser_button的父元素，
                filters: {
                    mime_types : [
                        { title : "media files", extensions : params.filter }
                    ]
                },
                multipart_params:params.multipartParams,
                max_file_size: params.size,
                flash_swf_url: '/asset_hub/static/js/lib/Moxie.swf',  //引入flash,相对路径
                max_retries: 3,                   //上传失败最大重试次数
                chunk_size: '4mb',                //分块上传时，每片的体积
                auto_start: true,                 //选择文件后自动上传，若关闭需要自己绑定事件触发上传
                init: {
                    'Init':function(up,info){
                        //console.log(up.getOption("max_file_size"));
                    },
                    'FilesAdded': function(up, files) {
                        if(typeof params.fileAddedCallback === "function"){
                            params.fileAddedCallback(up,files);
                        }
                    },
                    'BeforeUpload':function(up,file){
                        if(typeof params.beforeUploadCallback === "function"){
                            params.beforeUploadCallback(up,files);
                        }
                    },
                    'UploadProgress': function(up, file) {
                        if(typeof params.progressCallback ==="function"){
                            params.progressCallback(file);
                        }
                    },
                    'FileUploaded': function(up, file, info) {
                        if(typeof params.uploadedCallback === "function"){
                            params.uploadedCallback(file,info);
                        }
                    },
                    'Error': function(up, err, errTip) {
                        $().toastmessage("showErrorToast",errTip);
                        up.refresh();
                    },
                    'Key': function(up, file) {

                        // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
                        // 该配置必须要在 unique_names: false , save_key: false 时才生效
                        var random=Math.floor(Math.random()*10+1)*(new Date().getTime());
                        var filename=file.name;
                        var extPos=filename.lastIndexOf(".");


                        // do something with key here
                        return random+filename.substring(extPos);

                        //return file.name;
                    }
                }
            });

            return uploader;

        }
    }

})();
