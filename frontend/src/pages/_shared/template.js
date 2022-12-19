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
                            <Link to="/" className="navbar-link">
                                <i className="fa-solid fa-house-chimney"></i> Home
                            </Link>
                        </div>
                        <div className="col-auto">
                            <Link to="/predict" className="navbar-link">
                                <i className="fa-solid fa-microchip"></i> Tool
                            </Link>
                        </div>
                        <div className="col-auto">
                            <Link to="/" className="navbar-link">
                                <i className="fa-solid fa-user-shield"></i> Privacy
                            </Link>
                        </div>
                        <div className="col-auto">
                            <Link to="/" className="navbar-link">
                                <i className="fa-solid fa-people-group"></i> Over ons
                            </Link>

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