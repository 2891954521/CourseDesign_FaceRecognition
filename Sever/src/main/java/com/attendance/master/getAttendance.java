package com.attendance.master;

import com.config.Config;
import com.util.ParameterUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;

@WebServlet(name = "getAttendance", value = "/master/getAttendance")
public class getAttendance extends HttpServlet{
	
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
		response.setContentType("text/json");
		JSONObject js = new JSONObject();
		
		String time = request.getParameter("time");
		
		if(time != null && !"".equals(time)){
			queryAttendanceLog(js,time);
		}else queryAttendance(js);
		
		response.getWriter().print(js);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
		ParameterUtil.methodError(response);
	}
	
	private void queryAttendance(JSONObject js){
		Connection conn = null;
		try{
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			
			ResultSet result = conn.createStatement().executeQuery("SELECT `startTime`,`endTime`,`lateTime`,`arrive`,`actual`,`late` FROM `attendance`");

			ParameterUtil.setStatus(js, Config.HTTP_OK, "查询成功！");
			JSONArray data = new JSONArray();
			
			while(result.next()){
				data.put(new JSONObject()
						.put("startTime", result.getString("startTime").split("\\.")[0])
						.put("endTime", result.getString("endTime").split("\\.")[0])
						.put("lateTime", result.getInt("lateTime"))
						.put("arrive", result.getInt("arrive"))
						.put("actual", result.getInt("actual"))
						.put("late", result.getInt("late")));
			}
			
			js.put("data", data);

		}catch(Exception e){
			ParameterUtil.setStatus(js, Config.SEVER_ERROR, "数据库连接异常！" + e.getMessage());
		}finally{
			if(conn != null){
				try{ conn.close(); }catch(SQLException ignored){ }
			}
		}
	}
	
	private void queryAttendanceLog(JSONObject js, String time){
		Connection conn = null;
		try{
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			
			ResultSet result = conn.createStatement().executeQuery("SELECT `uid`,`time`,`status` FROM `attendance_log` WHERE `attendanceTime` = '" + time + "';");
			
			ParameterUtil.setStatus(js, Config.HTTP_OK, "查询成功！");
			JSONArray data = new JSONArray();
			
			while(result.next()){
				data.put(new JSONObject()
						.put("uid", result.getString("uid"))
						.put("time", result.getString("time").split("\\.")[0])
						.put("status", result.getInt("status")));
			}
			
			js.put("data", data);
			
		}catch(Exception e){
			ParameterUtil.setStatus(js, Config.SEVER_ERROR, "数据库连接异常！" + e.getMessage());
		}finally{
			if(conn != null){
				try{ conn.close(); }catch(SQLException ignored){ }
			}
		}
	}
}
