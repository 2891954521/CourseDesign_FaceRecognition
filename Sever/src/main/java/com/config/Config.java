package com.config;

public class Config{
	
	// 数据库名称
	public static String DATABASE_NAME = "attendance_platform";
	
	// 用户表
	//public static String TABLE_USER = "user";
	
	// 考勤表
	//public static String TABLE_LESSONS = "attendance";
	
	// 考勤记录表
	//public static String TABLE_LESSONS = "attendance_log";
	
	// MySQL用户
	public static String SQL_USER = "attendance";
	
	// MySQL密码
	public static String SQL_PASSWORD = "MkZfRUvYQV6p1gRS";
	
	// 操作成功
	public static int HTTP_OK = 200;
	
	// 未登录
	public static int NEED_LOGIN = 401;
	
	// 权限不足
	public static int Forbidden = 403;
	
	// 参数错误
	public static int PARAMETER_ERROR = 443;
	
	// 服务器错误
	public static int SEVER_ERROR = 500;
	
	// 请求方法错误
	public static int METHOD_ERROR = 501;
}
