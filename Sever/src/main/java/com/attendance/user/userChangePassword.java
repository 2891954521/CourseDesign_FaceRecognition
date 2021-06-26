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

@WebServlet(name = "userChangePassword", value = "/api/userChangePassword")
public class userChangePassword extends HttpServlet{
	
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse response) throws IOException{
		ParameterUtil.methodError(response);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException{
		
		response.setContentType("text/html");
		
		JSONObject js = new JSONObject();
		
		String oldPassword = request.getParameter("oldPassword");
		String newPassword = request.getParameter("newPassword");
		String conformPassword = request.getParameter("conformPassword");
		
		if(oldPassword == null|| newPassword == null || conformPassword == null){
			ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"请输入密码！");
			response.getWriter().print(js);
			return;
		}
		
		Integer uid = (Integer)request.getSession().getAttribute("uid");

		if(uid == null){
			ParameterUtil.setStatus(js,Config.NEED_LOGIN,"请先登录！");
			response.getWriter().print(js);
			return;
		}
		
		if(!newPassword.equals(conformPassword)){
			ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"两次输入的密码不一致！");
			response.getWriter().print(js);
			return;
		}
		
		oldPassword = EncryptionUtil.getMD5str(oldPassword);
		
		Connection conn = null;
		
		try {
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			if(conn != null){
				String sql = String.format("SELECT `uid` FROM `user` WHERE `uid` = '%s' AND `password` = '%s';",uid,oldPassword);
				ResultSet result = conn.createStatement().executeQuery(sql);
				
				if(result.next()){
					result.close();
					
					sql = String.format("UPDATE `user` SET password = '%s' WHERE `uid` = '%s'",EncryptionUtil.getMD5str(newPassword),uid);
					int column = conn.createStatement().executeUpdate(sql);
					
					if(column == 1){
						ParameterUtil.setStatus(js,Config.HTTP_OK,"修改成功！");
					}else{
						ParameterUtil.setStatus(js,Config.SEVER_ERROR,"修改失败！");
					}
					
				}else{
					ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"原密码错误！");
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
