var config = {
	mode: "low",
	state: "enabled"
};

var is_dl_check = window.location.href.indexOf('account=') !== -1;
var is_in_destination = window.location.href.indexOf('r2cdn') !== -1;

function set_flash_config() {
	var mode = (config.state === "enabled" && config.mode !== "high") ? config.mode : "high";
	var swf = document.getElementById("customRightClick");
	if (swf) {
		if (swf.getAttribute("quality") !== mode) {
			swf.setAttribute("quality", mode);
			var parent = swf.parentNode;
			parent.removeChild(swf);
			if (!is_dl_check) parent.appendChild(swf);
		}
	}
}

// function get_credential() {
// 	var dl_id = (window.location.href.match(/\&create\_dl\=([0-9]+)/) || [null, null])[1];
// 	return accounts[dl_id]
// }

function login() {
	// let {account, password} =  get_credential()
	// let {account, password} =  get_credential()
	const urlParams = new URLSearchParams(window.location.search);
	const account = urlParams.get('account');
	const password = urlParams.get('password');
	console.log(account,password)
	// var account = (window.location.href.match(/\&account\=([0-9]+)/) || [null, null])[1];
	// var password = (window.location.href.match(/\&password\=([0-9]+)/) || [null, null])[1];
	// alert(get_credential())
	var req = new XMLHttpRequest();
	req.open("POST", "../user/?ac=login", true);
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	req.onreadystatechange = () => {
		if (req.status === 200) {
			var data = JSON.parse(req.responseText);
			if (data.state === true) redirect_to_game()
			return 
		}
		alert("Invalid Credential")
	}
	req.send("login_id=" + account + "&login_pwd=" + password + "&code=&keep_login=0");
}

function redirect_to_game(){
	var iframe = document.querySelector("iframe[name='gameframe']");
	var game_url = iframe.getAttribute('src')
	window.location.href  = game_url
}

window.addEventListener('load', () =>{	
	if(is_dl_check)  login()
	if(is_in_destination) set_flash_config()
} )


