import './styles.css';
import { Link } from "react-router-dom";
// import logo from './_images/InHolland.png';

function Template(props) {
    return (<>
        <nav className="navbar navbar-light bg-light">
            <Link className="navbar-brand nunito" to="/">
                <span className="brand-name main-color">Inholland</span>
                <span className="secondary-color"> / AI</span>
            </Link>
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