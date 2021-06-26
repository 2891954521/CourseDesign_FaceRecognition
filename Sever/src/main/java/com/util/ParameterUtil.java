package com.util;

import com.config.Config;
import jakarta.servlet.http.HttpServletResponse;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

/*
 * 用于处理参数的类
 */

public class ParameterUtil{
	
	// 判断字符串是否为纯数字
	public static boolean isNumber(String s){
		char[] id = s.toCharArray();
		if(id.length == 0) return false;
		for(char c:id) if(!Character.isDigit(c)) return false;
		return true;
	}
	
	// 设置返还的json数据
	public static void setStatus(JSONObject js, int code, String msg){
		try{
			js.put("code",code);
			js.put("msg",msg);
		}catch(JSONException ignored){ }
	}
	
	
	public static void methodError(HttpServletResponse response) throws IOException{
		response.setContentType("text/json");
		JSONObject js = new JSONObject();
		ParameterUtil.setStatus(js, Config.METHOD_ERROR,"请求方法错误！");
		response.getWriter().print(js);
	}
}
