function calcular() {

    var orcamento = Number(document.getElementById("orcamento").value);
    var alimentacao = Number(document.getElementById("alimentacao").value);
    var transporte = Number(document.getElementById("transporte").value);
    var lazer = Number(document.getElementById("lazer").value);

    var total = alimentacao + transporte + lazer;
    var restante = orcamento - total;

    document.getElementById("total").innerText = "R$ " + total.toFixed(2);
    document.getElementById("restante").innerText = "R$ " + restante.toFixed(2);


    var alerta = document.getElementById("alerta");
    if (total > orcamento) {
        alerta.innerText = "Você ultrapassou o orçamento!";
        alerta.style.background = "#d9534f";
    } else {
        alerta.innerText = "Você está dentro do orçamento.";
        alerta.style.background = "#5cb85c";
    }

 
    mostrarBarra("barraAlimentacao", "Alimentação", alimentacao, total);
    mostrarBarra("barraTransporte", "Transporte", transporte, total);
    mostrarBarra("barraLazer", "Lazer", lazer, total);
}

function mostrarBarra(id, nome, valor, total) {
    var porcentagem = 0;
    if (total > 0) {
        porcentagem = (valor / total) * 100;
    }
    
    var barra = document.getElementById(id);
    barra.style.width = porcentagem + "%";
    barra.innerText = nome + ": R$ " + valor.toFixed(2);
}

var campos = document.querySelectorAll("input");
for (var i = 0; i < campos.length; i++) {
    campos[i].addEventListener("input", calcular);
}

calcular();

