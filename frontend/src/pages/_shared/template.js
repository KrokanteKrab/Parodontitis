import './styles.css';
import { Link } from "react-router-dom";
import logo from './_images/logo-inholland.png';

function Template(props) {
    return (<>
        <div className="container">
            <nav className="navbar navbar-light bg-light">
                <Link className="navbar-brand nunito" to="/">
                    <img className="navbar-logo" src={ logo } alt="logo"/>
                </Link>
            </nav>
        </div>

        <div className="content">
            {props.children}
        </div>
        <footer>
            Ontwikkeld door Krokante Krab - 2022
        </footer>

    </>);
}

export default Template;