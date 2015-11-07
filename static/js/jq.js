$(document).ready(function () {

	var curr_country = 0;
	var curr_season = -1;
	
	var slide_interval;
	var current;
	var min;
	var max;
	var toggle_interval;
	
	var x_ax = [];
	var y_ax = [];
	var team_names = new Array(20);
	
	var teams_excluded = [];
	var season_start = 1;
	var season_len = 11;
	var img_array;
	var per_game = "false";
	var x_label_text = "";
	var y_label_text = "";
	
	

	$("#go_button").click(function() {
	
		if (x_ax.length === 0 || y_ax.length === 0)
			alert("Make sure to insert values for x and y axis");
		else{
		
			$("#img").attr("src", "static/loading.gif");
		
			// create plots
			$.ajax({
				url: '/make_graph/',
				data : {x_data: JSON.stringify(x_ax), y_data: JSON.stringify(y_ax), season_num: curr_season, season_start: $("#slider").slider("values",0), teams_excluded: JSON.stringify(teams_excluded), league: curr_country, per_game: per_game, x_text: x_label_text, y_text: y_label_text},
				type: 'POST',
				success: function(response){
					season_start = $("#slider").slider("values",0);
					img_array = [];
					img_array = JSON.parse(response);
					change_top_slide(season_len);
					change_slider($("#game_week_slider").slider("option","value"), season_len);
					$("#img").attr("src","data:image/png;base64,".concat(img_array[0]));
				},
				error: function(error){
					console.log(error);
				}
			})
		}
			
	});
	
	function change_country(new_country){
	
		curr_country = new_country;
		curr_season = -1;
		change_years(new_country);
		change_teams(curr_season);
		
		x_ax = [];
		y_ax = [];
		
		x_label_text = "";
		y_label_text = "";
		$(".xaxis")[0].childNodes[0].innerHTML = "";
		$(".yaxis")[0].childNodes[0].innerHTML = "";
		
		$("#img").attr("src", "");
		img_array = [];
	}
	
	function change_years(country){
		
		// delete old options
		var test = $(".season option").length;
		while ($(".season option").length > 0){
			$(".season option").remove();
		}
	
		years = ['02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16']
		if (country === 0)
			start = 0;
		else if (country === 4)
			start = 3;
		else if (country === 1)
			start = 5;
		else
			start = 4;
		
		index = 0;
		for (var i = start;i < years.length;++i){
			str = ['<option value="', index.toString(), '">', years[i].toString(), '</option>'].join("");
			$(".season").append(str);
			index++;
		}
		$(".season").attr("value", index);
		$(".season")[0].lastChild.selected = 'selected';
		$(".season").selectmenu().selectmenu("refresh");
	}
	
	function change_teams(curr_season){
	
		if (curr_country === 2)
			team_names = new Array(18);
	
		$.ajax({
			url: '/get_teams/',
			data: {league: curr_country, season: curr_season},
			type: 'POST',
			success: function(response){
				
				var temp_array = response.split(',');
				season_len = parseInt(temp_array.pop());
				change_top_slide(season_len);
				
				while($("#team_tab .check_div").length > 0)
					$("#team_tab .check_div").remove();
					
				for (i = 0; i < team_names.length; ++i){
					str = ['<div class="check_div"><input type="checkbox" checked="checked"><label for="check" id="check_label', i, '"></label></div>'].join("");
					$("#team_tab").append(str);
					$("#check_label" + i).text(temp_array[i]);
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	}
	
	$("#clear_button").click(function() {
		x_ax = [];
		y_ax = [];
		
		x_label_text = "";
		y_label_text = "";
		$(".xaxis")[0].childNodes[0].innerHTML = "";
		$(".yaxis")[0].childNodes[0].innerHTML = "";
		
		$("#img").attr("src", "");
		img_array = [];
	});
	
	var change_slider = function change_slider(val, max){
		$("#game_week_slider").slider("option", "value", val);
		$("#game_week_slider").slider("option", "min", val);
		$("#game_week_slider").slider("option", "max", max);
		$("#game_week_text").val(val);
		if (val >= max){
			clearInterval(slide_interval);
		}
		
		// set image
		if (typeof img_array !== "undefined" && img_array.length != 0)
			$("#img").attr("src", "data:image/png;base64,".concat(img_array[val-1]));
	}
	
	function change_top_slide(val){
		min = $("#slider").slider("values", 0);
		$("#slider").slider("option", "max", val);
		$("#slider").slider("option", "values", [min, val]);
		$("#games_text").val(min + " - " + val);
	}

	$(".season").selectmenu({
		width : 100,
		height: 100
	});

	$("#slider").slider({
		range : true,
		min : 1,
		max : season_len,
		values : [1, season_len],
		slide : function (event, ui) {
			$("#games_text").val(ui.values[0] + " - " + ui.values[1]);
			$("clear_button").click();
		}
	});
	
	$("#games_text").val($("#slider").slider("values", 0) + " - " + $("#slider").slider("values", 1));
	
	$("#game_week_slider").slider({
		value: $("#slider").slider("values",0),
		min : $("#slider").slider("values",0),
		max : $("#slider").slider("values",1),
		slide : function (event, ui) {
			$("#game_week_text").val(ui.value);
			if (typeof img_array !== "undefined" && img_array.length != 0)
				$("#img").attr("src", "data:image/png;base64,".concat(img_array[ui.value-season_start]));
		}
	});
	
	$("#game_week_text").val($("#game_week_slider").slider("value"));

	$(".drag").draggable();

	add_to = true;
	$("#axis_options_button").click(function () {
		if (add_to){
			$(".plot").animate({width:"+=140px",height:"+=120px"},500);
			add_to = false;
			$("#x_axis_label").css({"width":"620px"});
			$("#x_axis_label").css({"left":"0.5%"});
			$("#y_axis_label").css({"width":"520px"});
			$("#y_axis_label").css({"left":"-360%"});
		} else {
			$(".plot").animate({width:"-=140px",height:"-=120px"},500);
			add_to = true;
			$("#x_axis_label").css({"width":"420px"});
			$("#x_axis_label").css({"left":"8%"});
			$("#y_axis_label").css({"width":"420px"});
			$("#y_axis_label").css({"left":"-360%"});
		}
		toggle_interval = setInterval(slide_toggle(),500);
		
	});
	
	function slide_toggle(){
		$("#axis_options_holder").toggle("slide");
		$("#season_div").toggle("slide");
		$("#slider").toggle("slide");
		$("#slide_p").toggle("slide");
		$("#country_div").toggle("slide");
		clearInterval(toggle_interval);
	}
	
	$("#axis_options_holder").tabs();
	
	$(".selections").draggable({revert : true});
	
	$(".xaxis").droppable({
		accept: ".selections",
		hoverClass: "hover",
		drop: function(event, ui){
			attr_text = ui.draggable.text();
			x_ax.push(attr_text);
			change_axis_text($("#x_axis_label"), x_label_text, attr_text, true);
		}
	});
	
	$(".yaxis").droppable({
		accept: ".selections",
		hoverClass: "hover",
		drop: function(event, ui){
			attr_text = ui.draggable.text();
			y_ax.push(attr_text);
			change_axis_text($("#y_axis_label"), y_label_text, attr_text, false);
		}
	});
	
	function change_label(label, new_text){

	}
	
	$(".play_button").click(function(){
		if ($(this).text() === "Play"){
			$(this).text("Pause");
			
			min = $("#game_week_slider").slider("option", "min");
			max = $("#game_week_slider").slider("option", "max");
			
			// return to the beginning
			if ($("#game_week_slider").slider("option", "value") === max){
				change_slider(min);
			}
			
			current = $("#game_week_slider").slider("option", "value");

			slide_interval = setInterval(function() {change_slider(++current)},1000);
			
		} else{
			$(this).text("Play");
			clearInterval(slide_interval);
		}
	});
	
	$(".season").selectmenu({
		change: function(event, ui){
			test = $(".season").val();
			curr_season = parseInt($(".season").val());
			change_teams(curr_season);
		}
	});
	
	$(".country").selectmenu({
		change: function(event, ui){
			curr_country = parseInt($(".country").val());
			change_country(curr_country);
		}
	});
	
	$("#team_tab").on('change', '.check_div',function(){
		team_text = $(this).find("label").text();

		if (!$(this).children("input")[0].checked){
			teams_excluded.push(team_text);
		} else{
			ind = teams_excluded.indexOf(team_text);
			if (ind > -1)
				teams_excluded.splice(ind,1);
		}
	});
	
	$(".radio_button").change(function(){
		$(".radio_button").prop("checked", false);
		$(this).prop("checked",true);
		per_game = $(this).val().toString();
		
		change_axis_text($("#y_axis_label"), y_label_text, "", false);
		change_axis_text($("#x_axis_label"), x_label_text, "", true);
	});
	
	function change_axis_text(label, old_text, new_text, is_x){
		text_to_add = old_text;
		if (text_to_add !== "" && new_text !== "")
			text_to_add = text_to_add.concat(" / ");
		text_to_add = text_to_add.concat(new_text);
		
		if (is_x)
			x_label_text = text_to_add;
		else
			y_label_text = text_to_add;
		
		if (per_game === "true" && text_to_add !== "")
			text_to_add = text_to_add.concat(" / game");

		label.text(text_to_add);
		$("#img").attr("src", "");
	}
	
	change_country(0);
});
