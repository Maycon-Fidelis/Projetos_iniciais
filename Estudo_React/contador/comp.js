// Componente de classNamee
// className Contador extends React.Component{
//     constructor(props){
//         super(props);
//         this.state = {
//             count: 0
//         }
//     }

//     // SetState para mudar o valor do estado
//     add = ()=>{
//         this.setState(function(prevState){
//             return { count: prevState.count + 1}
//         })
//     }

//     sub = ()=>{
//         this.setState(function(prevState){
//             return { count: prevState.count - 1}
//         })
//     }

//     render(){
//         return(
//             <div className="p-5 mb-4 bg-body-tertiary rounded-3">
//             <div className="container-fluid py-5">
//               <h1 className="display-5 fw-bold">Contador: {this.state.count}</h1>
//               <p className="col-md-8 fs-4">Aprendendo state (Estado)</p>
//               <div className="row gap-5">
//               <button onClick={this.sub} className="col btn btn-danger btn-lg" type="button">Subtrair - </button>
//               <button onClick={this.add} className="col btn btn-success btn-lg" type="button">Adicionar + </button>
//               </div>
//             </div>
//         </div>    
//         )
//     }

// }


function Explodiu(props){
    return(
        <h1 className="text-danger">EXPLODIU!</h1>
    )
}

// Componente funcional
function Contador(props) {

    let tema = props.tema;
    let btnNome = props.btnNome;

    // CRIAR UM STATE
    // O primeiro é qual que é o valor
    // O segundo é o nome da função
    // Após é definido que vai ser igual a um método nesse caso o useState()
    const [count, setCount] = React.useState(0);
    const [nome, setNome] = React.useState(btnNome);

    // UseEffect que é ativado após a renderização
    React.useEffect(() => {
        console.log('ATIVOU EFEITO COLATERAL')
    })
    // Vai definir o efeito colateral que vai acontecer
    // Ele é um efeito colateral que só acontece depois de renderizado
    // Mesmo estando em cima o console.log abaixo foi renderizado primeiro

    // UseEffect que é ativado após quando um STATE é alterado
    React.useEffect(() => {
        document.title = 'Contador:' + + count;
        console.log('ATIVOU EFEITO COLATERAL DO COUNT')
        if(count >= 5){
            setNome('Maycon');
        }
    }, [count])
    // Quando o count tiver uma alteração o useEffect será alterado

    // UseEffect que é ativado após quando um STATE é alterado
    React.useEffect(() => {
        console.log('ATIVOU EFEITO COLATERAL DO NOME')
    }, [nome])
    // Quando o count tiver uma alteração o useEffect será alterado

    // Definir para o efeito colateral acontecer só uma vez
    React.useEffect(() => {
        console.log('ATIVOU EFEITO COLATERAL APÉNAS NA MONTAGEM')
    }, [])

    function add() {
        setCount(count + 1);
    }

    function sub() {
        setCount(count - 1);
    }

    function trocaNome() {
        setNome('Maycon');
    }

    console.log('RENDERIZADO COMPONENTE!');

    if(count > 10){
        return (
            <div className="p-5 mb-4 bg-dark rounded-3">
                <div className="container-fluid py-5">
                    <Explodiu/>
                </div>
            </div>
        )        
    }

    return (
        <div className="p-5 mb-4 bg-body-tertiary rounded-3">
            <div className="container-fluid py-5">
                {
                    nome && <h1 className="display-5 fw-bold">Nome: {nome}</h1>
                }

                {
                    count > 10 ? <Explodiu /> : <h1 className="display-5 fw-bold">Contador: {count}</h1>
                }
                <p className="col-md-8 fs-4">Aprendendo state (Estado)</p>
                <div className="row gap-5">
                    <button onClick={sub} className="col btn btn-danger btn-lg" type="button">Subtrair - </button>
                    <button onClick={add} className="col btn btn-success btn-lg" type="button">Adicionar + </button>
                </div>
                <button onClick={trocaNome} className="col btn btn-primary btn-lg" type="button">Trocar Nome</button>
            </div>
        </div>
    )
}