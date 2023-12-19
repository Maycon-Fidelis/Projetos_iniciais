function App(props) {
    const usuarios = [
        {
            id: 1,
            nome: "Maycon",
            idade: 19
        },
        {
            id: 2,
            nome: "Bruno",
            idade: 23
        },
        {
            id: 3,
            nome: "Maria",
            idade: 39
        }
    ];
    
    return (
        <ul><Item lista={usuarios} /></ul>
    );
}

function Item(props) {
    const usuarios = props.lista;
    
    return (
        usuarios.map((usuario) => 
            <li key={usuario.id.toString()}>
                Nome: {usuario.nome} <br />
                Idade: {usuario.idade} <br />
            </li> 
        )
    );
} 

ReactDOM.render(
    <App />,
    document.getElementById('root')
);
