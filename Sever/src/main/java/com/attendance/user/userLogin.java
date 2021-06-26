package com.attendance.user;

import com.config.Config;
import com.util.EncryptionUtil;
import com.util.ParameterUtil;
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

@WebServlet(name = "onUserLogin", value = "/api/userLogin")
public class userLogin extends HttpServlet{
 
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException{
		ParameterUtil.methodError(response);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException{
		response.setContentType("text/html");
		
		JSONObject js = new JSONObject();
		
		String name = request.getParameter("name");
		String password = request.getParameter("password");
		
		if(name == null || password == null){
			ParameterUtil.setStatus(js, Config.PARAMETER_ERROR,"请输入用户名和密码！");
			response.getWriter().print(js);
			return;
		}
		
		password = EncryptionUtil.getMD5str(password);
		
		Connection conn = null;
		try {
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			if(conn != null){
				String sql = String.format("SELECT `uid`,`admin` FROM `user` WHERE `password` = '%s' AND `uid` = '%s';",password,name);
				ResultSet result = conn.createStatement().executeQuery(sql);
				if(result.next()){
					HttpSession session = request.getSession();
					session.setAttribute("isLogin",true);
					session.setAttribute("uid",result.getInt("uid"));
					session.setAttribute("admin",result.getInt("admin"));
					ParameterUtil.setStatus(js,Config.HTTP_OK,"登陆成功！");
				}else{
					ParameterUtil.setStatus(js,Config.PARAMETER_ERROR,"用户名或密码错误！");
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
