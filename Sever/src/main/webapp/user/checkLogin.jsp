<%@ page import="jakarta.servlet.http.Cookie" %>
<%
    if(session.getAttribute("isLogin") == null){
        session.setAttribute("isLogin", false);
        session.setAttribute("admin", 0);
    }else if(!(boolean)session.getAttribute("isLogin")){
        response.sendRedirect("/usr/login.jsp");
        return;
    }
%>