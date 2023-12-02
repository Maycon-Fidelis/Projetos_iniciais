// app.js
const express = require('express');
const app = express();

const restrita = require('./routes/restrita');

const PORT = process.env.PORT || 3000;

// Função que verifica se o usuário está logado
function usuarioLogado() {
    // Coloque aqui a lógica de autenticação, por exemplo:
    return false; // Troque para true se o usuário estiver autenticado
}

// Middleware
function verificaUsuarioLogado(req, res, next) {
    if (usuarioLogado()) {
        next();
    } else {
        res.redirect('/home');
    }
}

app.get('/home', (req, res) => {
    res.send('<h1>Página inicial</h1>');
});

app.use('/home/restrita', verificaUsuarioLogado, restrita);

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
