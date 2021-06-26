function get(url, done){
	const xhr = new XMLHttpRequest();
	xhr.responseType = "text";
	xhr.open('GET', url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;")
	xhr.send();
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4 && xhr.status === 200){
			const json = JSON.parse(xhr.responseText);
			if(json.code === 200){
				done(json);
			}else{
				layer.msg(json.msg, {icon: 2});
			}
		}
	};
}

function post(url, data, done){
	const xhr = new XMLHttpRequest();
	xhr.responseType = "text";
	xhr.open('POST', url);
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;")
	xhr.send(data);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4 && xhr.status === 200){
			const json = JSON.parse(xhr.responseText);
			if(json.code === 200){
				done(json);
			}else{
				layer.msg(json.msg, {icon: 2});
			}
		}
	};
}