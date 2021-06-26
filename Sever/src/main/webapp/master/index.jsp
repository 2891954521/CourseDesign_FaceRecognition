<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8" %>

<%@include file="/user/checkLogin.jsp" %>

<%
	if(session.getAttribute("admin") == null || (int)session.getAttribute("admin") != 1){
		response.sendRedirect("/user/login.jsp");
		return;
	}
%>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="description" content="考勤管理平台"/>
	<link href="/css/style.css" rel="stylesheet" type="text/css"/>
	<link rel="icon" href="/favicon.ico"/>
	<script src="/js/util.js"></script>
	<title>考勤管理平台</title>
</head>
<body>

<noscript>
	<strong>We're sorry but my website doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
</noscript>

<jsp:include page="/title.jsp">
	<jsp:param name="now" value="管理"/>
</jsp:include>

<iframe id="formSubmit" name="formSubmit" style="display:none;"></iframe>

<div class="layui-tab layui-tab-brief" style="margin: 0;background: #fff;">

	<ul class="layui-tab-title" style="background-color: #FFFFFF">
		<li class="layui-this">考勤系统</li>
		<li>用户管理</li>
	</ul>

	<div class="layui-tab-content">

		<div class="layui-tab-item layui-show" style="padding: 12px">

			<form class="layui-form" method="post" action="/master/newAttendance" target="formSubmit">

				<div class="layui-form-item">
					<label class="layui-form-label">结束时间</label>
					<div class="layui-input-inline">
						<input type="text" class="layui-input" name="endTime" id="endTime" placeholder="yyyy-MM-dd HH:mm:ss">
					</div>
				</div>

				<div class="layui-form-item">
					<label class="layui-form-label">迟到时间(分钟)</label>
					<div class="layui-input-inline">
						<input type="number" class="layui-input" name="lateTime" lay-verify="required" autocomplete="off" value="10">
					</div>
				</div>

				<div class="layui-form-item">
					<div class="layui-input-block">
						<button type="submit" class="layui-btn" lay-submit="true" lay-filter="formDemo">开始考勤</button>
					</div>
				</div>

			</form>

			<fieldset class="layui-elem-field layui-field-title" style="padding: 12px;">
				<legend>考勤列表</legend>
			</fieldset>

			<table class="layui-hide" id="attendance" lay-filter="attendance"></table>

		</div>

		<div class="layui-tab-item" id="tab_user"></div>

	</div>

</div>

<script type="text/html" id="users">
	<div style="padding: 12px">
		<table class="layui-table" style="text-align: center">
			<thead>
			<tr>
				<td>学号</td>
				<td>姓名</td>
				<td>操作</td>
			</tr>
			</thead>
			<tbody>{{table}}</tbody>
		</table>
	</div>
</script>

<script type="text/html" id="attendanceUsers">
	<div style="padding: 12px">
		<table class="layui-table" style="text-align: center">
			<thead>
			<tr>
				<td>时间</td>
				<td>学号</td>
				<td>姓名</td>
				<td>状态</td>
			</tr>
			</thead>
			<tbody>{{table}}</tbody>
		</table>
	</div>
</script>

<script type="text/html" id="bar">
	<a class="layui-btn layui-btn-xs" lay-event="details">查看</a>
	<a class="layui-btn layui-btn-xs layui-btn-danger" lay-event="delete">删除</a>
</script>

<script>

	layui.use('dropdown', function(){});

	layui.use('laydate', function(){
		layui.laydate.render({ elem: '#endTime', type: 'datetime' });
	});

	function moreOption(btn){
		let data;
		if(btn.name === '0'){
			data = [{title: '设为管理员', id: 'setAdmin'}]
		}else{
			data = [{title: '移除管理员', id: 'removeAdmin'}]
		}
		layui.dropdown.render({
			elem: btn,
			show: true,
			data: data,
			click: function(data){
				if(data.id === 'setAdmin'){
					layer.confirm('确定将其设为管理员？', function(index){
						let param = 'uid=' + btn.parentNode.id + '&admin=1';
						post('/master/setAdmin', param, function(json){
							getUsers(function(){});
							layer.msg(json.msg);
						})
						layer.close(index);
					});
				}else if(data.id === 'removeAdmin'){
					layer.confirm('确定移除其管理员权限？', function(index){
						let param = 'uid=' + btn.parentNode.id + '&admin=0';
						post('/master/setAdmin', param, function(json){
							getUsers(function(){});
							layer.msg(json.msg);
						})
						layer.close(index);
					});
				}
			},
			align: 'right',
			style: 'box-shadow: 1px 1px 10px rgb(0 0 0 / 12%);'
		});
	}

	get('/master/getUsers', function(json){
		document.users = json.data.users;
		document.total = json.data.total;
		let tab = document.getElementById("tab_user");
		let str = document.getElementById("users").innerText;
		let content = "";
		for(let i = 0; i < document.total; i++){
			let user = document.users[i];
			content += "<tr><td>" + user.uid + "</td><td>" +
				(user.admin === 1 ? "<i class='layui-icon layui-icon-username' style='font-size: 14px; color: #ff8d39;'></i>" : "") + user.name + "</td>" +
				"<td id='" + user.uid + "'><a class='layui-btn layui-btn-xs' name='" + user.admin + "' onclick='moreOption(this)'>更多 <i class='layui-icon layui-icon-down'></i></a></td></tr>";
		}
		str = str.replace("{{table}}", content);
		tab.innerHTML = str;
	});

	const table = layui.table;

	layui.use('table', function(){
		table.render({
			elem: '#attendance',
			url:'/master/getAttendance',
			cols: [[
				{field:'startTime',width:200,title:'开始时间',sort: true},
				{field:'endTime',width:200,title:'结束时间'},
				{field:'lateTime',width:120,title:'迟到时间'},
				{field:'arrive',width:80,title:'应到'},
				{field:'actual',width:80,title:'实到'},
				{field:'late',width:80,title:'迟到'},
				{fixed:'right',width:120,title:'操作',toolbar:'#bar',unresize:true},
			]],
			response: { statusCode: 200 },
			page: true,
			limit:10,
		});

		table.on('tool(attendance)', function(obj){
			const data = obj.data;
			if(obj.event === 'delete'){
				layer.confirm('是否删除该条考勤记录', {
						icon: 3,
						title:'提示',
						fixed: true,
						offset: '40%'
					}, function(index){
						layer.close(index);
						get('/master/deleteAttendance?time=' + data.startTime, function(json){
							layer.msg(json.msg,{icon:1});
							obj.del();
						})
					}
				);

			}else if(obj.event === 'details'){
				get('/master/getAttendance?time=' + data.startTime, function(json){

					let str = document.getElementById("attendanceUsers").innerText;

					let content = "";

					for(let i = 0; i < document.total; i++){
						let user = document.users[i];
						let time = "";
						let status = 0;
						for(let j = 0; j < json.data.length; j++){
							if(user.uid == json.data[j].uid){
								time = json.data[j].time;
								status = json.data[j].status;
								break;
							}
						}
						content += "<tr><td>" + time + "</td><td>" + user.uid + "</td><td>" + user.name + "</td><td>";
						switch(status){
							case 0:content += "未签到";break;
							case 1:content += "已签到";break;
							case 2:content += "迟到";break;
							case 3:content += "早退";break;
							case 4:content += "已签退";break;
						}
						content += "</td></tr>";
					}

					str = str.replace("{{table}}", content);

					layer.open({
						type: 1,
						title: "签到列表",
						area: ["600px", "800px"],
						btn: ['确定'],
						content: str,
						yes: function(index){ layer.close(index); }
					});
				});
			}
		});

	});

	const frame = document.getElementById('formSubmit');
	frame.onload = frame.onreadystatechange = function(){
		if(!(this.readyState && this.readyState !== 'complete')){
			const json = JSON.parse(this.contentDocument.body.innerText.match(new RegExp("(\{.*?\})"))[0]);
			if(json.code === 200){
				layer.msg(json.msg, {icon: 1});
				if(json.msg === "操作成功！"){
					table.reload('attendance',{
						url: '/master/getAttendance'
					});
				}
			}else{
				layer.msg(json.msg, {icon: 2});
			}
		}
	}

</script>

</body>
</html>