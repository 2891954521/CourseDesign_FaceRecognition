<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="description" content="考勤管理平台" />
    <link href="/css/style.css" rel="stylesheet" type="text/css" />
    <link rel="icon" href="/favicon.ico"/>
    <title>考勤管理平台</title>
</head>
<body>

<noscript>
    <strong>We're sorry but my website doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
</noscript>

<jsp:include page="/title.jsp">
    <jsp:param name="now" value="" />
</jsp:include>

<iframe id="formSubmit" name="formSubmit" style="display:none;"></iframe>

<div style="background-color: #1E9FFF">

    <div class="layui-row">

        <div class="layui-col-xs4 layui-col-md8" style="padding-left: 5%;padding-top: 5%;">
            <h1>考勤管理平台</h1>
        </div>

        <div class="layui-col-xs8 layui-col-md4">

            <div class="layui-card layui-panel" style="margin: 32px 32px">

                <div class="layui-card-header" style="color: #1E9FFF; text-align: center; font-size: 24px; letter-spacing: 5px; padding: 12px">登陆</div>

                <div class="layui-card-body">


                    <form class="layui-form" method="post" action="/api/userLogin" target="formSubmit">

                        <div class="layui-form-item">
                            <label class="layui-form-label">学号</label>
                            <div class="layui-input-inline">
                                <input type="text" name="name" required placeholder="请输入学号" autocomplete="on" class="layui-input">
                            </div>
                        </div>

                        <div class="layui-form-item">
                            <label class="layui-form-label">密码</label>
                            <div class="layui-input-inline">
                                <input type="password" name="password" required placeholder="请输入密码" autocomplete="on" class="layui-input">
                            </div>
                        </div>

                        <div class="layui-form-item" style="padding: 0 48px 0">
                            <button class="layui-btn layui-btn-fluid" lay-submit="">登陆</button>
                        </div>

                        <div style="padding-right: 32px; text-align: right;">
                            <a href="/user/register.jsp" style="color: gray;">新用户注册</a>
                        </div>

                    </form>

                </div>
            </div>
        </div>
    </div>
</div>

<script>
    const frame = document.getElementById('formSubmit');
    frame.onload = frame.onreadystatechange = function(){
        if(!(this.readyState && this.readyState !== 'complete')){
            const json = JSON.parse(this.contentDocument.body.innerText.match(new RegExp("(\{.*?\})"))[0]);
            if(json.code === 200){
                window.location.href = '/index.jsp';
            }else{
                layer.msg(json.msg,{icon:2});
            }
        }
    }
</script>

</body>
</html>
