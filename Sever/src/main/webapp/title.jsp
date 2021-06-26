<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8" import="jakarta.servlet.http.Cookie"%>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <link href="/layui/css/layui.css" rel="stylesheet" type="text/css">
</head>
<body>

<div class="layui-header" style="top: 0;left: 0;right: 0;padding: 0 0 0 25px;background-color: #23262E;">

    <ul class="layui-nav layui-layout-left" style="background: 0 0;display: contents">
        <%
            String[] title;
            String[] href;
            if(session.getAttribute("admin") != null && (int)session.getAttribute("admin") == 1){
                title = new String[]{"首页","管理"};
                href = new String[]{"/index.jsp","/master/index.jsp"};
            }else{
                title = new String[]{"首页"};
                href = new String[]{"/index.jsp"};
            }
            String now = request.getParameter("now");
            for(int i=0;i<title.length;i++){
                out.println("<li class='layui-nav-item");
                if(title[i].equals(now))out.println(" layui-this");
                out.println("'><a href='" + href[i] + "'>" + title[i] + "</a></li>");
            }
        %>
    </ul>

    <ul class="layui-nav layui-layout-right" style="background: 0 0;">
        <%
            if(session.getAttribute("isLogin") == null){
            	session.setAttribute("isLogin",false);
            	session.setAttribute("admin",0);
                out.println("<li class='layui-nav-item'><a href='/user/login.jsp'><img src='/images/userpic.gif' class='layui-nav-img'>未登录</a></li>");
            }else if((boolean)session.getAttribute("isLogin")){    %>
                <li class="layui-nav-item"><a><img src="/images/userpic.gif" class="layui-nav-img" alt="">我</a>
                    <dl class="layui-nav-child">
                        <dd><a href="/user/changePassword.jsp">修改密码</a></dd>
                        <dd><a href="/user/logout.jsp">退出登陆</a></dd>
                    </dl>
                </li>
        <%  }else{
            	out.println("<li class='layui-nav-item'><a href='/user/login.jsp'><img src='/images/userpic.gif' class='layui-nav-img'>未登录</a></li>");
            }
        %>
    </ul>
</div>

<script src="/layui/layui.js"></script>

<script>layui.use('element', function(){});</script>

</body>
</html>


