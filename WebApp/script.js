function send(){
	var like = []
	var not_like = []
	if(document.getElementById('one').checked == true)
	{
		like.push(document.getElementById('url1').value);
	}
	else{
		not_like.push(document.getElementById('url1').value);
	}
	
	if(document.getElementById('two').checked == true)
	{
		like.push(document.getElementById('url2').value);
	}
	else{
		not_like.push(document.getElementById('url2').value);
	}
	
	if(document.getElementById('three').checked == true)
	{
		like.push(document.getElementById('url3').value);
	}
	else{
		not_like.push(document.getElementById('url3').value);
	}
	json = {'like': like, 'not like': not_like}
	console.log(json)
	axios.post('http://127.0.0.1:5002', json) 	
	window.document.write("<h2 align=center> Grazie e alla prossima!</h2>");	
}

