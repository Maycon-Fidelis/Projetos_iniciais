const express = require('express');
const router = express.Router();

// Objetivo:
// carros/fiat/uno

router.get('/:carro', (req,res)=>{ // /:carro define o parametro que será pego para ser trato no back
    res.send('<h1>Rota Carros é:' + req.params.carro + '</h1>'); // req.params.carro Pega o parametro específico
}); // Dessa forma é especificado que será pego um valor dinâmico chamado carro

router.get('/:carro/:marca', (req,res)=>{
    const marcas = ['fiat','volks','bmw'];
    if(marcas.includes(req.params.marca)){
        res.send('<h1>A rota de carro é: ' + req.params.carro +'</h1>' + '<h1>A rota Carros de marca é:' + req.params.marca + '</h1>');    
    } else{
        res.send('<h1>Marca não encontrada</h1>');
    }
    
})

router.get('/:carro/:marca/:modelo', (req,res)=>{
    res.send(req.params); // Parametro inteiro voltado como json
})

// Exportar o roteamento
module.exports = router;