function loadXMLDoc()
{
	var xmlhttp
	if (window.XMLHttpRequest){
		//  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
		xmlhttp=new XMLHttpRequest()
	}
	
	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200){
			this.nextSibling.nextSibling.innerHTML=xmlhttp.responseText
		}
	}
	xmlhttp.open("GET",this.href,true)
	xmlhttp.send()
}
