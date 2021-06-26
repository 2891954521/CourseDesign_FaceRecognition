package com.attendance.master;

import com.config.Config;
import com.util.ParameterUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;

@WebServlet(name = "newAttendance", value = "/master/newAttendance")
public class newAttendance extends HttpServlet{
 
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
        ParameterUtil.methodError(response);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{

        response.setContentType("text/json");
        JSONObject js = new JSONObject();
        
        HttpSession session  = request.getSession();
        
        Boolean b = (Boolean)session.getAttribute("isLogin");
        
        if(b == null || !b){
            ParameterUtil.setStatus(js, Config.NEED_LOGIN,"请先登录！");
            response.getWriter().print(js);
            return;
        }
        
        if((Integer)session.getAttribute("admin") != 1){
            ParameterUtil.setStatus(js,Config.Forbidden,"权限不足！");
            response.getWriter().print(js);
            return;
        }
        
        Date date = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        
        String startTime = sdf.format(date);
        String endTime = request.getParameter("endTime");
        int lateTime = Integer.parseInt(request.getParameter("lateTime"));
        
        Connection conn = null;
        
        try{
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
    
            ResultSet result = conn.createStatement().executeQuery("SELECT count(1) FROM `user`;");
            result.next();
            
            int total = result.getInt("count(1)");
            result.close();
            
            int column = conn.createStatement().executeUpdate(String.format(
                    "INSERT INTO attendance(startTime,endTime,lateTime,arrive) value('%s','%s','%d',%d);",
                    startTime, endTime, lateTime, total
            ));
            
            if(column == 1){
                ParameterUtil.setStatus(js,Config.HTTP_OK,"操作成功！");
            }else{
                ParameterUtil.setStatus(js,Config.SEVER_ERROR,"操作失败！");
            }
        }catch (Exception e) {
            ParameterUtil.setStatus(js,Config.SEVER_ERROR,"数据库连接异常！" + e.getMessage());
        }finally{
            if(conn != null){
                try{ conn.close(); }catch(SQLException ignored){ }
            }
        }
        
        response.getWriter().print(js);
	}
}
