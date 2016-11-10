function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$("#create_task").on('click', function(){
	if (document.getElementById("insert_task")) {
		$("#insert_task").remove();
	}else{
		var container = $(document.createElement('div')).css({
			margin: '5px 0',
			width: '100%'
		});
		container.attr('id', 'insert_task');
		container.attr('class', 'form-group');
		container.append('<input type="text" id="insert_new_task" placeholder="Ingrese una nueva tarea" class="form-control"></input>')
		container.append('<input type="submit" id="submit_new_task" class="form-control btn-primary" value="Ingresar Tarea"></input>')
		$("#new_task").append(container);
		submit_new_task();
	}
});

$("#create_cost").on('click', function(){
	if (document.getElementById("insert_cost")) {
		$("#insert_cost").remove();
	}else{
		var container = $(document.createElement('div')).css({
			margin: '5px 0',
			width: '100%'
		});
		container.attr('id', 'insert_cost');
		container.attr('class', 'form-group');
		container.append('<input type="text" id="insert_new_cost" placeholder="Ingrese costo en U.F." class="form-control"></input>')
		container.append('<textarea id="insert_descripcion_new_cost" required class="form-control" placeholder="Ingresar concepto del costo"></textarea>');
		container.append('<input type="submit" id="submit_new_cost" class="form-control btn-primary" value="Ingresar Costo"></input>')
		$("#new_cost").append(container);
		submit_new_cost();
	}
});

$("#users_activity").on('click', function(){
	if (document.getElementById("insert_user")) {
		$("#insert_user").remove();
	}else{
		var container = $(document.createElement('div')).css({
			margin: '5px 0',
			width: '100%'
		});
		container.attr('id', 'insert_user');
		container.attr('class', 'form-group');
		container.append('<input type="text" id="insert_new_user" required placeholder="Ingrese un nuevo usuario" class="form-control"></input>')
		container.append('<textarea id="insert_descripcion_new_user" required class="form-control" placeholder="Ingresar funciones del usuario"></textarea>');
		container.append('<input type="submit" id="submit_new_user" class="form-control btn-primary" value="Ingresar Usuario"></input>')
		$("#new_user").append(container);
		submit_new_user();
	}
});

function submit_new_cost(){
	$("#submit_new_cost").on('click', function(){
		if (document.getElementById('insert_new_cost').value && document.getElementById('insert_descripcion_new_cost').value) {
			funciones = $("#insert_descripcion_new_cost").val()
			$.ajax({
				'method': 'POST',
				'url': '/insert_cost/',
				'data': {
					'id': $("#id").val(),
					'costo': $("#insert_new_cost").val(),
					'item': funciones
				},
				'success': function(data){
					$element = $(".cost_list");
					$element.html("");
					$.each(data.response, function(key, val){
						$element.append('\
							<div class="costs" style="border-bottom: solid 1px #ccc;">\
								<span>' + val.item + '</span>\
								<b>' + val.costo +' UF</b>\
							</div>\
						');
					});
					total = 0
					$.each(data.response, function(key, val){
						total = total + val.costo
					})
					$element.append('\
						<div class="costs-total">\
							<span><b>Costo Total:</b></span>\
							<b>' + total +' UF</b>\
						</div>\
					')
					$("#insert_cost").remove();
				}
			});
		}
	});
}

function submit_new_user(){
	$("#submit_new_user").on('click', function(){
		if (document.getElementById('insert_new_user').value && document.getElementById('insert_descripcion_new_user').value) {
			funciones = $("#insert_descripcion_new_user").val()
			$.ajax({
				'method': 'POST',
				'url': '/insert_user/',
				'data': {
					'id': $("#id").val(),
					'usuario': $("#insert_new_user").val(),
					'descripcion': funciones
				},
				'success': function(data){
					$element = $(".users_list");
					$element.html("");
					$.each(data.response, function(key, val){
						$element.append('\
							<div class="users" style="border-bottom: solid 1px #ccc;">\
								<h6>\
									<b>' + val.usuario_asigando +'</b>\
								</h6>\
								<p>' + val.funciones + '</p>\
							</div>\
						');
					});
					$("#insert_user").remove();
				}
			});
		}
	});
}

function submit_new_task(){
	$("#submit_new_task").on('click', function(){
		if (document.getElementById('insert_new_task').value) {
			$.ajax({
				'method': 'POST',
				'url': '/insert_task/',
				'data': {
					'id': $("#id").val(),
					'task': $("#insert_new_task").val()
				},
				'success': function(data){
					$element = $(".tasks_list_ul");
					$element.html("");
					$.each(data.response, function(key, val){
						if (val.completado == 'true') {
							checked = 'checked'
						}else{
							checked = ''
						}
						$element.append('<li>\
							<input id="task-' + val.id + '" type="checkbox" ' + checked + '></input>\
							<label class="label_check" data-id="' + val.id + '" for="task-' + val.id + '">\
								' + val.tarea + '</label>\
						</li>')
					});
					$("#insert_task").remove();
					check();
				}
			});
		}
	});
}

function check(){
	$(".label_check").on('click', function(){
		id = $(this).data('id');
		checked = $("#task-" + id).is(':checked');
		$.ajax({
			'method': 'POST',
			'url': '/set_task/',
			'data': {
				'id': id,
				'complete': checked
			}
		});
	});
}

if ($("#uploadBtn").length) {
	document.getElementById("uploadBtn").onchange = function () {
	    document.getElementById("uploadFile").innerHTML = this.value;
	};
}

check();

$("#load_more").on('click', function(){
	var last_comment = 0;
	$(".timeline li").each(function(i, li){
		last_comment = $(li).attr('id');
	});
	$.ajax({
		'method': 'POST',
		'url': '/load_more_comments/',
		'data': {
			'id': $("#id").val(),
			'last': last_comment
		},
		'success': function(data){
			var $element = $(".timeline");
			$.each(data.response, function(key, val){
				if (val.adjunto) {
					$element.append('\
						<li id="' + val.id + '">\
							<div class="timeline-autor">\
								<span>Registrado por: <b>' + val.usuario + '</b></span>\
							</div>\
							<div class="timeline-comentario">\
								<span>' + val.comentario + '</span>\
							</div>\
							<div class="timeline-footer">\
								<small>' + val.creado + '</small>\
								<span class="archivo_adjunto" data-original-title="' + val.adjunto + '" data-toggle="tooltip" data-placement="left" title="">\
									<a href="/media/' + val.adjunto + '" download="">\
										<i class="ion-paperclip"></i>\
									</a>\
								</span>\
							</div>\
						</li>\
					')
				}else{
					$element.append('\
						<li id="' + val.id + '">\
							<div class="timeline-autor">\
								<span>Registrado por: <b>' + val.usuario + '</b></span>\
							</div>\
							<div class="timeline-comentario">\
								<span>' + val.comentario + '</span>\
							</div>\
							<div class="timeline-footer">\
								<small>' + val.creado + '</small>\
							</div>\
						</li>\
					')
				}
			});
			$('[data-toggle="tooltip"]').tooltip();
		}
	});
});

$("#user_assigned").change(function() {
    var option = $(this).find('option:selected');
    $.ajax({
    	'method': 'POST',
    	'url': '/change_assigned/',
    	'data': {
    		'id': $("#id").val(),
    		'user_assigned': option.val()
    	},
    	'success': function(data){
    		location.reload();
    	}
    });
});

$("#area_assigned").change(function() {
    var option = $(this).find('option:selected');
    $.ajax({
    	'method': 'POST',
    	'url': '/change_area/',
    	'data': {
    		'id': $("#id").val(),
    		'area_assigned': option.val()
    	},
    	'success': function(data){
    		location.reload();
    	}
    });
});

$("#type_assigned").change(function() {
    var option = $(this).find('option:selected');
    $.ajax({
    	'method': 'POST',
    	'url': '/type_assigned/',
    	'data': {
    		'id': $("#id").val(),
    		'type_assigned': option.val()
    	},
    	'success': function(data){
    		location.reload();
    	}
    });
});

$(".datepicker").change(function(){
	var valor = $(this).val();
	$.ajax({
    	'method': 'POST',
    	'url': '/change_espired/',
    	'data': {
    		'id': $("#id").val(),
    		'date': valor
    	},
    	'success': function(data){
    		location.reload();
    	}
    });
});

$("#hide-menu").on('click', function(){
	$("aside").toggle("slow");
});

$(".collapse_li").on('click', function(){
	var $id = $(this).data('id');
	$(".collapse_li").css('background-color', '#00669E');
	$(this).siblings('li').hide();
	$("li[data-id=" + $id + "]").slideToggle();
	$(this).css('background-color', '#0087d1');
});

function ReplaceNumberWithCommas(yourNumber) {
    var components = yourNumber.toString().split(",");
    components [0] = components [0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return components.join(",");
}

$("#sidemenu > li > a").on('click', function(){
	if ($(this).hasClass('collapse')) {
		$(".open").removeClass("open").addClass("collapse").siblings('ul').remove();
		var valor = $(this).data('id');
		var publico = $(this).data('publico');
		var $element = $(this).parent();
		$.ajax({
	    	'method': 'POST',
	    	'url': '/get_areas/',
	    	'data': {
	    		'id': valor,
	    		'publico': publico
	    	},
	    	'success': function(data){
	    		var dom = '<ul>'
	    		$.each(data.response, function(key, val){
	    			if (val.area != null) {
		    			dom += '<li>\
		    						<a data-id="' + val.id + '" href="javascript:void(0);">\
		    							' + val.area + '\
		    						</a>\
		    					</li>';
	    			}else{
	    				dom += '<li>\
		    						<a data-id="' + val.id + '" href="javascript:void(0);">\
		    							Área sin asignar\
		    						</a>\
		    					</li>';
	    			}
	    		});
	    		dom += '</ul>';
	    		$element.append(dom);
	    		$element.children("a").removeClass("collapse").addClass("open");
	    		$("#sidemenu > li > ul > li > a").on('click', function(){
	    			$('.li_project').remove();
					var $element = $(this).parent();
					$.ajax({
				    	'method': 'POST',
				    	'url': '/get_projects/',
				    	'data': {
				    		'id': $(this).data('id'),
				    		'estado': $(this).parent().parent().siblings('a').data('id'),
				    		'publico': $(this).parent().parent().siblings('a').data('publico')
				    	},
				    	'success': function(data){
				    		var domInner = '<ul class="li_project">'
				    		$.each(data.response, function(key, val){
				    			domInner += '<li>\
				    						<a data-id="' + val.id + '" href="/task/' + val.id + '">\
				    							<i class="ion-link"></i>\
				    							<span>' + val.actividad + '</span>\
				    						</a>\
				    					</li>';
				    		});
				    		domInner += '</ul>';
				    		$element.append(domInner);
				    	}
				    });
				});
	    	}
	    });
	}else{
		$(this).siblings('ul').remove();
		$(this).removeClass("open").addClass("collapse");
	}
});

$("#table_costos > tbody > tr").on('click', function(){
	if ($(this).next().attr('id') == "detalle_area") {
		$(".tr_data").remove();
	}else{
		$(".tr_data").remove();
		var $element = $(this);
		$.ajax({
	    	'method': 'POST',
	    	'url': '/get_projects_table/',
	    	'data': {
	    		'id': $(this).data('id')
	    	},
	    	'success': function(data){
	    		var dom = '';
	    		$.each(data.response, function(key, val){
	    			dom += '<tr class="tr_data" id="detalle_area"_' + val.id + '>\
	    					<td style="padding-left: 60px; cursor: default;" colspan="2">\
						   		' + val.actividad + '\
							</td>\
							<td>\
								' + val.costo + ' UF\
							</td>'
	    			dom += '</tr>'
	    		});
	    		console.log(dom);
	    		$(dom).insertAfter($element);
	    	}
	    });
	}
});