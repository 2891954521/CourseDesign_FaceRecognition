package com.attendance.api;

import com.config.Config;
import com.util.ParameterUtil;
import jakarta.servlet.ServletException;
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
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;

@WebServlet(name = "signIn", value = "/api/signIn")
public class signIn extends HttpServlet{
	
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
		response.setContentType("text/json");
		JSONObject js = new JSONObject();
		
		String uid = request.getParameter("uid");
		
		if(uid == null || "".equals(uid) || !ParameterUtil.isNumber(uid)){
			ParameterUtil.setStatus(js, Config.PARAMETER_ERROR, "学号格式错误！");
			response.getWriter().print(js);
			return;
		}
		
		Connection conn = null;
		try{
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/" + Config.DATABASE_NAME, Config.SQL_USER, Config.SQL_PASSWORD);
			
			ResultSet result = conn.createStatement().executeQuery("SELECT `startTime`,`endTime`,`lateTime` FROM `attendance` ORDER BY `startTime` DESC LIMIT 1;");
			
			if(!result.next()){
				ParameterUtil.setStatus(js, Config.HTTP_OK, "暂无考勤！");
				response.getWriter().print(js);
				return;
			}
			
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
			
			Date startTime = sdf.parse(result.getString("startTime"));
			Date endTime = sdf.parse(result.getString("endTime"));
			Date currentTime = new Date();
			
			String t = sdf.format(currentTime);
			
			if(currentTime.getTime() - endTime.getTime() > 600000){
				ParameterUtil.setStatus(js, Config.HTTP_OK, "暂无考勤！");
				response.getWriter().print(js);
				return;
			}
			
			int lateTime = result.getInt("lateTime");
			int minute = (int)((currentTime.getTime() - startTime.getTime()) / 60000);
			
			result.close();
			
			result = conn.createStatement().executeQuery("SELECT `status` FROM `attendance_log` WHERE `attendanceTime` = '" + sdf.format(startTime) + "' AND `uid` = '" + uid + "' LIMIT 1;");
			
			int status;
			
			if(result.next()){
				if(result.getInt("status") != 0){
					if(endTime.getTime() - currentTime.getTime() > 0){
						status = 3;
						ParameterUtil.setStatus(js, Config.HTTP_OK, "早退！");
					}else{
						status = 4;
						ParameterUtil.setStatus(js, Config.HTTP_OK, "签退成功！");
					}
					int column = conn.createStatement().executeUpdate(String.format(
							"UPDATE `attendance_log` SET `status` = %d WHERE `attendanceTime` = '%s' AND `uid` = '%s';",
							status, sdf.format(startTime), uid
					));
					if(column == 0){
						ParameterUtil.setStatus(js, Config.SEVER_ERROR, "签退失败！");
					}
				}
			}else{
				if(minute > lateTime){
					status = 2;
					ParameterUtil.setStatus(js, Config.HTTP_OK, "迟到！");
				}else{
					status = 1;
					ParameterUtil.setStatus(js, Config.HTTP_OK, "签到成功！");
				}
				int column = conn.createStatement().executeUpdate(String.format(
						"INSERT INTO attendance_log(uid,attendanceTime,time,status) value('%s','%s','%s',%d);",
						uid, sdf.format(startTime), sdf.format(currentTime), status
				));
				if(column == 0){
					ParameterUtil.setStatus(js,Config.SEVER_ERROR,"签到失败！");
				}else{
					String sql = status == 1 ?
							"UPDATE `attendance` SET `actual` = `actual` + 1 WHERE `startTime` = '" + sdf.format(startTime) + "';" :
							"UPDATE `attendance` SET `actual` = `actual` + 1,`late` = `late` + 1 WHERE `startTime` = '" + sdf.format(startTime) + "';" ;
					column = conn.createStatement().executeUpdate(sql);
					if(column == 0){
						ParameterUtil.setStatus(js, Config.SEVER_ERROR, "签到失败！");
					}
				}
			}
		}catch(Exception e){
			e.printStackTrace();
			ParameterUtil.setStatus(js, Config.SEVER_ERROR, "数据库连接异常！" + e.getMessage());
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
