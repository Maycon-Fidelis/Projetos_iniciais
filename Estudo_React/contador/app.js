function App() {
    return(
    <main>
    <div class="container py-4">
        <Contador btnNome={false} />
    </div>
    </main>
    )
} 

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);