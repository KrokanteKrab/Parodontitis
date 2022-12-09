import './styles.css';
// import logo from './_images/InHolland.png';

function Template(props) {
    return (<>
        <nav className="navbar navbar-light bg-light">
            <a className="navbar-brand nunito" href="#">
                <span className="brand-name main-color">Inholland</span>
                <span className="secondary-color"> / AI</span>
            </a>
        </nav>

        <main>
            <div className="container">
                {props.children}
            </div>
        </main>
        <footer>
            Ontwikkeld door Krokante Krab - 2022
        </footer>

    </>);
}

export default Template;