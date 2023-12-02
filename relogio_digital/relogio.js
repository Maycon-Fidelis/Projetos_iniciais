// Variaveis base
var dia;
var horas;
var minutos;
var segundos;
var dia;
var dias_da_semana = ["Domingo", "Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado"];
// Variaveis base 

// Pegando os valores do relogio
hora_atual = new Date;
minutos = hora_atual.getMinutes();
segundos = hora_atual.getSeconds();
horas = hora_atual.getHours();
dia = hora_atual.getDay();
// Pegando os valores do relogio

// Pegando os valores do html onde será impresso
var segundos_tela = document.getElementsByClassName("segundos");
var minutos_tela = document.getElementsByClassName("minuto");
var horas_tela = document.getElementsByClassName("hora");
var relogio_dia = document.getElementsByClassName("relogio_dia_h2");
// Pegando os valores do html onde será impresso

function imprimir(variavel_tela,tempo){
        if(tempo < 10){
            tempo = "0" + tempo;
    }
    variavel_tela[0].textContent = tempo;
}

function contar_o_tempo(){
    if(segundos >= 59){
        segundos = 0;
        contar_minutos();
    } else{
        segundos++;
    }
    imprimir(segundos_tela,segundos);
}

function contar_minutos(){
    if(minutos >= 59){
        minutos = 0;
        contar_horas();
    } else {
        minutos++;
    }
    imprimir(minutos_tela,minutos);
}

function contar_horas(){
    if(horas >= 23){
        horas = 0;
        contar_dias();
    } else{
        horas++;
    }
    imprimir(horas_tela,horas);
}

function contar_dias(){
    if(dia >= 6){
        dia = 0;
    } else {
        dia++;
    }
    imprimir(relogio_dia, dias_da_semana[dia]);
}

imprimir(segundos_tela,segundos);
imprimir(minutos_tela,minutos);
imprimir(horas_tela,horas);
imprimir(relogio_dia, dias_da_semana[dia]);
setInterval(contar_o_tempo,1000);