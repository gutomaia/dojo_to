function linker(text){
	//if (link == '/login/twitter') return link;
	var regex = /(<a(.*)href="(\/[^"]+)"(.*)>([^<]+)<\/a>)/g
	return text.replace(regex,"<a$2href=\"/#!$3\"$4>$5</a>");
};
