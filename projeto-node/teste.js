const express = require('express');
const app = express();

const restrito = require('./routes/restrita');

const PORT = process.env.PORT || 3000;

app.get('/home', (req, res) => {
    res.send('<h1>Página inicial</h1>');
});

const usuarioLogado = true;

if (!usuarioLogado) {
    app.use('/', restrito);
} else {
    app.get('/', (req, res) => {
        res.redirect('/home');
    });
}

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
