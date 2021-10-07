window.onload = function(){

    window.setInterval(get_json_data, 2000);
}

	function get_json_data() {
		$.get('index_info', function(data) {
			const obj = JSON.parse(data)

			var mode = "OFF";
			switch(obj.mode){
			    case 0:
			    mode = "OFF";

			    $("#clean-button-container").hide()
			    $("#hand-button-container").hide()
			    $("#automatic-button-container").hide()
			    break;
			    case 1:
			    mode = "CLEAN";
			    $("#but-clean").removeClass("gray")
			    $("#but-clean").addClass("active")
			    $("#but-automatic").removeClass("active")
			    $("#but-automatic").addClass("gray")
			    $("#but-hand").removeClass("active")
			    $("#but-hand").addClass("gray")

			    $("#clean-button-container").show()
			    $("#hand-button-container").hide()
			    $("#automatic-button-container").hide()
			    break;
			    case 2:
			    mode = "HAND";
			    $("#but-clean").removeClass("active")
			    $("#but-clean").addClass("gray")
			    $("#but-automatic").removeClass("active")
			    $("#but-automatic").addClass("gray")
			    $("#but-hand").removeClass("gray")
			    $("#but-hand").addClass("active")

			    $("#clean-button-container").hide()
			    $("#hand-button-container").show()
			    $("#automatic-button-container").hide()
			    break;
			    case 3:
			    mode = "AUTOMATIC";
			    $("#but-clean").removeClass("active")
			    $("#but-clean").addClass("gray")
			    $("#but-automatic").removeClass("gray")
			    $("#but-automatic").addClass("active")
			    $("#but-hand").removeClass("active")
			    $("#but-hand").addClass("gray")

			    $("#clean-button-container").hide()
			    $("#hand-button-container").hide()
			    $("#automatic-button-container").show()
			    break;
			}
			$("#mode").html(mode)

			var status = "OFF";
			switch(obj.status){
			    case 0:
			    status = "OFF";
			    break;
			    case 1:
			    status = "FEHLER";
			    break;
			    case 2:
			    status = "INIT";
			    break;
			    case 3:
			    status = "COOLING DOWN";
			    break;
			    case 4:
			    status = "READY COOLING";
			    break;
			    case 5:
			    status = "MAKE ICE";
			    break;
			    case 6:
			    status = "PUSH OUT";
			    break;
			}
			$("#status").html(status)

			var error = " ";
			switch(obj.error){
			    case 0:
			    error = "UNRECOGNIZED";
			    break;
			    case 1:
			    error = "TEMPERATURE SENSOR";
			    break;
			    case 2:
			    error = "OVERTIME";
			    break;
			    case 3:
			    error = "STB";
			    break;
			}
			$("#description").html(error)
			$("#temperature-indoor").html(obj.temperatures.indoor)
			$("#temperature-cooling").html(obj.temperatures.cooling)
			$("#temperature-stb").html(obj.temperatures.stb)

            if (obj.components.water_inlet == true){
                $("#but-water").addClass("active");
                $("#but-water").removeClass("grey");
            } else {
                $("#but-water").addClass("gray");
                $("#but-water").removeClass("active");
            }
            if (obj.components.compressor == true){
                $("#but-compressor").addClass("active");
                $("#but-compressor").removeClass("grey");
            } else {
                $("#but-compressor").addClass("gray");
                $("#but-compressor").removeClass("active");
            }
            if (obj.components.pump == true){
                $("#but-pump").addClass("active");
                $("#but-pump").removeClass("grey");
            } else {
                $("#but-pump").addClass("gray");
                $("#but-pump").removeClass("active");
            }

		})
	}

    function send_set_mode(mode){
        $.get("set_mode/" + mode);
    }

    function send_automatic_start()
    {
        $.get("automatic_start");
    }
    function send_automatic_stop()
    {
        $.get("automatic_stop");
    }
    function send_toggle_water(){
        $.get("toggle_water");
    }
    function send_toggle_compressor(){
        $.get("toggle_compressor");
    }
    function send_toggle_pump(){
        $.get("toggle_pump");
    }
    function send_clean_start(){
        $.get("clean_start");
    }
    function send_clean_stop(){
        $.get("clean_stop");
    }
