package com.attendance.master;

import com.config.Config;
import com.util.ParameterUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;

@WebServlet(name = "getUsers", value = "/master/getUsers")
public class getUsers extends HttpServlet{
	
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
		response.setContentType("text/json");
		
		JSONObject js = new JSONObject();
		
		HttpSession session  = request.getSession();
		
		Boolean b = (Boolean)session.getAttribute("isLogin");
		
		if(b == null || !b){
			ParameterUtil.setStatus(js,Config.NEED_LOGIN,"请先登录！");
			response.getWriter().print(js);
			return;
		}

		if((Integer)session.getAttribute("admin") != 1){
			ParameterUtil.setStatus(js,Config.Forbidden,"权限不足！");
			response.getWriter().print(js);
			return;
		}
		
		Connection conn = null;
		
		try{
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			if(conn != null){

				ResultSet result = conn.createStatement().executeQuery("SELECT `uid`,`name`,`admin` FROM `user`;");
				
				ParameterUtil.setStatus(js,Config.HTTP_OK,"查询成功！");
				
				JSONObject data = new JSONObject();
				JSONArray users = new JSONArray();
				
				while(result.next()){
					users.put(new JSONObject()
							.put("uid",result.getInt("uid"))
							.put("name",result.getString("name"))
							.put("admin",result.getInt("admin"))
					);
				}
				
				result.close();
				
				data.put("users",users);
				data.put("total",users.length());
				
				js.put("data",data);
			}else{
				ParameterUtil.setStatus(js,Config.SEVER_ERROR,"连接数据库失败！");
			}
		}catch(Exception e){
			ParameterUtil.setStatus(js,Config.SEVER_ERROR,"数据库连接错误！" + e.getMessage());
		}finally{
			if(conn != null){
				try{ conn.close(); }catch(SQLException ignored){ }
			}
		}
		
		response.getWriter().print(js);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
		ParameterUtil.methodError(response);
	}
}
