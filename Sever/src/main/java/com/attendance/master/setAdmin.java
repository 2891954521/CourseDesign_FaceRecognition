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
import java.sql.SQLException;

@WebServlet(name = "setAdmin", value = "/master/setAdmin")
public class setAdmin extends HttpServlet{
 
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
			ParameterUtil.setStatus(js,Config.NEED_LOGIN,"请先登录！");
			response.getWriter().print(js);
			return;
		}
		
		if((Integer)session.getAttribute("admin") != 1){
			ParameterUtil.setStatus(js, Config.Forbidden, "权限不足！");
			response.getWriter().print(js);
			return;
		}
		
		String uid = request.getParameter("uid");
		String admin = request.getParameter("admin");
		
		if(uid == null || admin == null){
			ParameterUtil.setStatus(js, Config.PARAMETER_ERROR, "参数错误！");
			response.getWriter().print(js);
			return;
		}
		
		if(!ParameterUtil.isNumber(uid)){
			ParameterUtil.setStatus(js, Config.PARAMETER_ERROR, "学号格式错误！");
			response.getWriter().print(js);
			return;
		}
		
		if(!"0".equals(admin) && !"1".equals(admin)){
			ParameterUtil.setStatus(js, Config.PARAMETER_ERROR, "参数错误！");
			response.getWriter().print(js);
			return;
		}
		
		Connection conn = null;
		
		try{
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			if(conn != null){
				String sql = String.format("UPDATE `user` SET admin = %s WHERE `uid` = %s;",admin,uid);
				int column = conn.createStatement().executeUpdate(sql);
				
				if(column == 1){
					ParameterUtil.setStatus(js, Config.HTTP_OK, "操作成功！");
				}else{
					ParameterUtil.setStatus(js,Config.SEVER_ERROR,"操作失败！");
				}
				
			}else{
				ParameterUtil.setStatus(js,Config.SEVER_ERROR,"连接数据库失败！");
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
