package com.attendance.user;

import com.config.Config;
import com.util.EncryptionUtil;
import com.util.ParameterUtil;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;

@WebServlet(name = "userRegister", value = "/api/userRegister")
public class userRegister extends HttpServlet{
 
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException{
        ParameterUtil.methodError(response);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException{
	    
        response.setContentType("text/html");
        
        JSONObject js = new JSONObject();
        
        String name = request.getParameter("name");
        String uid = request.getParameter("uid");
        String password = request.getParameter("password");
        String conformPassword = request.getParameter("conformPassword");
        
        if(name == null|| uid == null || password == null || conformPassword == null){
            ParameterUtil.setStatus(js,Config.NEED_LOGIN,"请输入用户名或学号或密码！");
            response.getWriter().print(js);
            return;
        }
        
        if(!ParameterUtil.isNumber(uid)){
            ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"学号只能是正整数！");
            response.getWriter().print(js);
            return;
        }

        if(!password.equals(conformPassword)){
            ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"两次输入的密码不一致！");
            response.getWriter().print(js);
            return;
        }
        
        password = EncryptionUtil.getMD5str(password);
        
        Connection conn = null;
        
        try{
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
            if(conn != null){
                String sql = String.format("SELECT `uid` FROM `user` WHERE `uid` = '%s';",uid);
                ResultSet result = conn.createStatement().executeQuery(sql);
                if(result.next()){
                    ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"学号已存在！");
                }else{
                    result.close();
                    
                    sql = String.format("INSERT INTO user(uid,name,password,admin) value('%s','%s','%s',0)",uid,name,password);
                    int column = conn.createStatement().executeUpdate(sql);
                    
                    if(column == 1){
                        ParameterUtil.setStatus(js,Config.HTTP_OK,"注册成功！");
                    }else{
                        ParameterUtil.setStatus(js,Config.SEVER_ERROR,"注册失败！");
                    }
                }
                result.close();
            }else{
                ParameterUtil.setStatus(js,Config.SEVER_ERROR,"连接数据库失败！");
            }
        }catch (Exception e) {
            ParameterUtil.setStatus(js,Config.SEVER_ERROR,"数据库连接失败！" + e.getMessage());
        }finally{
            if(conn != null){
                try{ conn.close(); }catch(SQLException ignored){ }
            }
        }
        
        response.getWriter().print(js);
    }
}
