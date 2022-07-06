document.addEventListener('DOMContentLoaded', function() {
	function load_server_list(){
		var server_list =  document.getElementById('server_id')
		server_list.innerHTML = '' //empty server list
		server.forEach(s => {
			var server_option = document.createElement("option")
			server_option.value = s.server_id
			server_option.text = s.server_name
			server_list.appendChild(server_option)
		})
	
	}
	//
	// account data reader
	//
	function AccountData() {
		this.data = [];
		this.list = document.getElementById("accountlist");

		// create html
		this.create = function(id, data) {
			var link = document.getElementById("ad_" + id);
			if (link) {
				this.list.removeChild(link);
			}
			
			var li = document.createElement("li");
			li.setAttribute("id", "ad_" + id);

			var link = document.createElement("a");
			link.setAttribute("href", "https://www.r2games.com/play/?game=10&server=" + data.server_id + "&account=" + data.account + "&password=" + data.password);
			link.setAttribute("class", "account");
			link.setAttribute("target", "_blank");
			link.innerText = data.name || data.mail || data.account;
			li.appendChild(link);

			this.list.appendChild(li);
		}

		// load data
		this.load = function(callback) {
			var self = this;
			accounts.forEach((a, i) => {
				self.create(i, a)
			})
		}
	}

	var AC = new AccountData();
	AC.load();
	load_server_list();
	// add button
});