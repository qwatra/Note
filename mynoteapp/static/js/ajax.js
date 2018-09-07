var gen_note =function (note) {
	return `<div class="note ${note.favorite}" id="${note.id}">
		<h4>${note.head}</h4>
		<p>${note.body}</p>
		<button class="btn-del" title="Удалить"><span>x</span></button>
		<button class="btn-fvr" title="Избранная"></button>
	</div>`
}

var edit_note = function(){
    	$.ajax({
			type: 'GET',
			url: '/ajax/',
			data:  {action: "get",
				id: $(this).attr('id')},
			success: function(data) {
				$("input[name=id]").val(data.id)
				$("input[name=head]").val(data.head)
				tinyMCE.activeEditor.setContent(data.body);
				$('select[name=category]').prop('selectedIndex',0);
				if(data.category != null) {
					$('select[name=category]').find('option[value='+ data.category +']').attr("selected", true)
				}
				$("input[name=uuid]").val(data.uuid)
			}});

    	tinymce.init({width: 'auto'})
		$(".edit_forms").css("display", "block")
		$("#layer").css("display", "block")
    }
var delete_note = function(e){
		$.ajax({
			type: 'GET',
			url: '/ajax/',
			data:  {action: "del",
				id: $(this).parent().attr('id')},
			success: function(data) {
				if(data.succses){
					$("#"+data.id).remove()
				}
			}});
		e.stopPropagation();
	}
//Изменение избранности
var set_favorite_note = function(e){
		$.ajax({
			type: 'GET',
			url: '/ajax/',
			data:  {action: "set_favorite",
				id: $(this).parent().attr('id'),
				value: !$(this).parent().hasClass("favorite")},
			success: function(data) {
				if($("#"+data.id).hasClass("favorite")){
					$("#"+data.id).removeClass("favorite")
				} else {
					$("#"+data.id).addClass("favorite")
				}
			}});
		e.stopPropagation();
	}


$(document).ready(function() {
	//Сохранение заметки и обновление отображения
    $("#btn-save").click(
		function(){
			var form = $('#form').serialize()
			tinyMCE.triggerSave();
			form.body = $("textarea#id_body").val();
			$.ajax({
	          type: 'POST',
	          url: '/ajax/',
	          data:  $('#form').serialize(),
	          success: function(data) {
	          	$("div.invalid-feedback").remove()
	          	if(data.succses) {
	          		var note = data.note
	          		var node = $("#"+note.id)
	          		if(node.length == 1){
	          			node.find("h4").text(note.head)
	          			node.find("p").text(note.body)
	          		} else {
	          			//такой заметки еще нет создадимее
	          			$(".flex_container").append(gen_note(note))
	          			//навешиваем обработчики
	          			node = $("#"+note.id)
	          			node.click(edit_note)
	          			node.find(".btn-del").click(delete_note)
	          			node.find(".btn-fvr").click(set_favorite_note)
	          		}
	          		$(".edit_forms").css("display", "none")
    				$("#layer").css("display", "none")
	          	} else{
	          		for (var key in data.errors) {
	          			$(".edit_forms [name="+key+"]").parent().append("<div class=\"invalid-feedback\" style=\"display:block\">"+data.errors[key]+"</div>")
	          		}
	          	}
	          }});
		}
	);
	//Сортировка
	$(".order-form").change(function(){
		$.ajax({
			type: "GET",
			url: "/ajax/",
			data: "action=getsortednotes&"+$('.order-form').serialize(),
			success: function(response) {
				$(".note").remove()
				container = $(".flex_container")
				for(note of response.notes) {
					container.append(gen_note(note))
				}
				$(".note").click(edit_note)
				$(".note .btn-del").click(delete_note)
				$(".note .btn-fvr").click(set_favorite_note)
			}
		})
	})
	//Фильтрация
	$("#btn-filter").click(function(){
		$.ajax({
			type: "GET",
			url: "/ajax/",
			data: "action=getfilterednotes&"+$('.filter-form').serialize(),
			success: function(response) {
				$("div.invalid-feedback").remove()
				if(response.success) {
					$(".note").remove()
					container = $(".flex_container")
					for(note of response.notes) {
						container.append(gen_note(note))
					}
					$(".note").click(edit_note)
					$(".note .btn-del").click(delete_note)
					$(".note .btn-fvr").click(set_favorite_note)
				} else {
					for (var key in response.errors) {
						$(".filter-form [name="+key+"]").parent().append("<div class=\"invalid-feedback\" style=\"display:block\">"+response.errors[key]+"</div>")
	          		}
				}
			}
		})
	})
});

//Навешиваем обработчики
$(document).ready(function() {
	//нажатие кнопки добавления
	$("#btn-add").click(function(){
		$("input[name=id]").val("")
		$("input[name=head]").val("")
		tinyMCE.activeEditor.setContent("");
		$('select[name=category]').prop('selectedIndex',0);
		$("input[name=uuid]").val("")

    	$(".edit_forms").css("display", "block")
    	$("#layer").css("display", "block")
    });
	//нажаие на заметку
    $(".note").click(edit_note);

	$("#btn-cancel").click(function(){
		$(".edit_forms").css("display", "none")
		$("#layer").css("display", "none")
	});

	$(".btn-del").click(delete_note)
	$(".btn-fvr").click(set_favorite_note)
});