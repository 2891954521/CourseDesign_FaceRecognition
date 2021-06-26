<%
    session.invalidate();
    response.setStatus(302);
    response.setHeader("Location","/index.jsp");
%>