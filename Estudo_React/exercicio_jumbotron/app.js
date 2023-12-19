function App() {
    return(
    <main>
    <div class="container py-4">
        <Header/>
        <Destaque/>
        <div class="row align-items-md-stretch">
        <div class="col-md-6">
            <Card tema="dark"/>
        </div>
        <div class="col-md-6">
            <Card tema="light"/>
        </div>
        </div>
        <Footer/>
    </div>
    </main>
    )
} 

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);