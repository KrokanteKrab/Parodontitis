import './main.css';
import { Link } from "react-router-dom";
import logo from './_images/logo-inholland.png';

function Template(props) {
    return (<>
        <div className="nav-holder">

            <div className="container">
                <nav className="navbar navbar-light bg-light">
                    <Link className="navbar-brand nunito" to="/">
                        <img className="navbar-logo" src={ logo } alt="logo"/>
                    </Link>

                    <div className="row">
                        <div className="col-auto">
                            <Link to="/" className="navbar-link">Home</Link>
                        </div>
                    </div>
                </nav>

            </div>
        </div>

        <main>
            {props.children}
        </main>
        <footer>
            Ontwikkeld door Krokante Krab 🦀 - 2022
        </footer>

    </>);
}

export default Template;