$(function(){
    var jQuiz = {
        respuestas_storage: { q1: 'a', q2: 'c', q3: 'c', q4: 'c', q5: 'd', q6: 'a', q7: 'c', q8: 'b', q9: 'a',q10: 'b'},
		respuestas_peripheral: { q1: 'b', q2: 'd', q3: 'b', q4: 'c', q5: 'b'},	
		respuestas_license: { q1: 'b', q2: 'd', q3: 'b', q4: 'c', q5: 'b'},
		respuestas_network: {q1: 'c', q2: 'b', q3: 'a', q4: 'd', q5: 'c'},	
		
        comprobarPreguntas: function() {
			
			if(document.getElementById("nameApp").name == "storage"){
			    var arr = this.respuestas_storage;
			}
			else if(document.getElementById("nameApp").name == "peripheral"){
				var arr = this.respuestas_peripheral;
			}
			else if(document.getElementById("nameApp").name == "license"){
				var arr = this.respuestas_license;
			}
			else if(document.getElementById("nameApp").name == "network"){
				var arr = this.respuestas_network;
			}
			
			var ans = this.userAnswers;
            var resultArr = []
            for (var p in ans) {
                var x = parseInt(p) + 1;
                var key = 'q' + x;
                var flag = false;
                if (ans[p] == 'q' + x + '-' + arr[key]) {
                    flag = true;
                }
                else {
                    flag = false;
                }
                resultArr.push(flag);
            }
            return resultArr;
        },
        init: function(){
			var numPreguntas = document.getElementById("numberQuestions").name;
			var pr = 600/numPreguntas;					
			
            $('.btnNext').click(function(){
                if ($('input[type=radio]:checked:visible').length == 0) {
                            
                    return false;
                }
                $(this).parents('.questionContainer').fadeOut(500, function(){
                    $(this).next().fadeIn(500);
                });
                var el = $('#progress');
                el.width(el.width() + pr + 'px');
            });
            $('.btnPrev').click(function(){
                $(this).parents('.questionContainer').fadeOut(500, function(){
                    $(this).prev().fadeIn(500)
                });
                var el = $('#progress');
                el.width(el.width() - pr + 'px');
            })
            $('.btnShowResult').click(function(){
                var arr = $('input[type=radio]:checked');
                var ans = jQuiz.userAnswers = [];
                for (var i = 0, ii = arr.length; i < ii; i++) {
                    ans.push(arr[i].getAttribute('id'))
                }
            })
            $('.btnShowResult').click(function(){
                $('#progress').width(300);
                $('#progressKeeper').hide();
                var resultados = jQuiz.comprobarPreguntas();
                var conjuntoResultados = '';
                var trueCount = 0;
				var prueba = document.getElementById("nameApp").name;
				
                for (var i = 0, ii = resultados.length; i < ii; i++){
                    if (resultados[i] == true){
						trueCount++;
						conjuntoResultados += '<div> Question ' + (i + 1) + ' is ' + '<font color="green">correct</font></div>'
					}else{
					    conjuntoResultados += '<div> Question ' + (i + 1) + ' is ' + '<font color="red">wrong</font></div>'
					}					
                }
				
				var nota = ((100/numPreguntas) * trueCount);
				var mensaje = '';
				
				if(nota >= 90){
					mensaje = "You can tell your grandma that you are the best!"
				}
				else if(nota >= 60){
					mensaje = "Study just a litle bit and your grandma will be proud."
				}
				else if(nota >= 50){
					mensaje = "You pass the test but you need study more."
				}
				else{
					mensaje = "Fail! You must study harder."
				}
				
                conjuntoResultados += '<div class="totalScore">Your score is ' + nota + ' / 100</div>'
				conjuntoResultados += '<div class="mensajeNota">' + mensaje + '</div>'
				
                $('#resultKeeper').html(conjuntoResultados).show();
            })
        }
    };
    jQuiz.init();
})
