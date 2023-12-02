// MÓDULO DE ARQUIVOS DO SISTEMA FILE SYSTEM
const { Console } = require('console');
const fs = require('fs');

/*** MANIPULAÇÃO DE PASTAS ***/

//fs.existsSync() - Verificar se o caminho existe
//fs.mkdirSync() - Cria uma pasta nova

/*if(!fs.existsSync('/public')){ // Verificar se a pasta existe
    fs.mkdirSync('./public', (err)=>{ // Criação de uma pasta
        if(err){
            throw err; 
        } else{
            console.log('Pasta criada com sucesso!');
        }
    })
} else {
    console.log('A pasta "public" já existe!');
}

fs.existsSync('./pasta' || fs.mkdirSync("./public")); // A lógica do código funciona como se existir ele não faz nada e se não existir ele cria a pasta

// Outro metodo para ser feito
*/

//fs.renameSync - Renomear a pasta

/*if(fs.existsSync('./public')){ // Verificar se a pasta existe
    fs.renameSync('./public','./maycon', (err)=>{ // Criação de uma pasta
        if(err){
            throw err; 
        } else{
            console.log('Pasta renomeada com sucesso!');
        }
    })
} else {
    console.log('Impossível renomear por que "public" não existe!');
} // Nesse código ele verifica se existe a pasta caso sim ele renomeia, caso não ele não renomeia 
*/

// fs.rmdir() - Serve para deletar uma pasta
// {recursive:true} - Para deletar uma pasta com intens

/*if(fs.existsSync('./maycon')){ // Verificar se a pasta existe
    fs.rmdir('./maycon',{recursive:true},(err)=>{ // Exclusão de uma pasta que não seja vazia
        if(err){
            throw err; 
        } else{
            console.log('Pasta deletada com sucesso!');
        }
    })
} else {
    console.log('Impossível deletar por que a pasta "maycon" não existe!');
}*/


/*** CRIAR ARQUIVOS / ATUALIZAR ***/

// fs.writeFile() - Substitui o arquivo e o conteudo caso exista, se não exisitir ele criar um novo arquivo com o conteudo que você passar.

// fs.appendFile() - Adiciona conteudo num arquivo, se o arquivo não existir ele cria.

// fs.open() - Abre um arquivo para leitura, se o arquivo não existir ele criar vazio. Para criar um arquivo usa-se a flag "w" para writing escrita.

// É necessário ter cuidado ao usar o writeFile, pois ele subtitui um arquivo caso ele exista, assim subescrevendo o arquivo caso já exista
// Por isso é recomendado verificar se o arquivo já existe
/*fs.writeFile('test.txt', 'test e conteúdo!', (err)=>{
    if(err){
        throw err;
    } else {
        console.log("Arquivo criado com sucesso!");
    }
})*/ // Primeiro parametro é o nome do arquivo, o segundo parametro é o conteudo que estara dentro

// Criando pra verificar se o arquivo já existe para não subescrever

/*if(!fs.existsSync('./public/teste2.txt')){
    fs.writeFile('./public/teste2.txt','teste de conteúdo, para o segundo!', (err)=>{
        if(err){
            throw err;
        } else{
            console.log('Arquivo Criado com Sucesso!');
        }   
    })
} else{
    console.log("Arquivo já existe!");
}*/

/*fs.appendFile('teste.txt','\nAdicionar Conteúdos!', // Primeiro parametro o nome do arquivo e o que será adicionado
(err)=>{
    if(err){
        throw err;
    } else {
        console.log("Arquivo atualizado!");
    }
});*/
// Caso o arquivo não exista ele ira criar um novo

/*fs.open('arquivo.txt','w', (err, file)=>{
    if(err){
        throw err;
    } else {
        console.log('Salvo');
    }
})*/ // Ele vai criar um arquivo vazio, é mais recomendado usar outros métodos 

/*** LER ARQUIVOS ***/

/*** RENOMEAR / EXCLUIR ***/

// fs.rename() - Renomear, excluir

/*fs.rename('arquivo.txt', 'maycon.txt', (err)=>{
    if(err){
        throw err;
    } else {
        console.log("Arquivo renomeado!");
    }
}) */// Primeiro parametro é o arquivo existente e o novo nome que você vai querer dar ao arquivo

// fs.unlink() - Excluir arquivo

/*fs.unlink('maycon.txt', (err)=>{
    if(err){
        throw err;
    } else {
        console.log('Arquivo deletado com sucesso!');
    }
})*/

/*** LER ARQUIVOS ***/

// fs.read() - Serve para ler arquivos 

if(url === '/arquivo'){
    fs.readFile('./public/index.html', (err,conteudo)=>{
        if(err){
            throw err;
        } else {
            res.statusCode = 200;
            res.setHeader('content-type', 'text/html; charset=utf-8');
            res.end(conteudo);        
        }
    })
} // Enviado uma arquivo para um servidor web