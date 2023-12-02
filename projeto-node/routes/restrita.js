const express = require('express');
const router = express.Router();

router.get('/', (req,res)=>{
    res.send('<h1>Rota Restrita</h1>');  
})

router.get('/usuarios', (req,res)=>{
    res.send('<h1>Lista Usarios</h1>');  
})

module.exports = router;