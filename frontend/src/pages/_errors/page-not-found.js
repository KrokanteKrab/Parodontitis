import { Link } from "react-router-dom";

function PageNotFound() {
    return (
        <>
            <div className="col-12">
                <h1>Oeps... could not find the requested page!</h1>
                <Link to="/" className="btn btn-outline-light btn-start-predict">Return to home page</Link>
            </div>
        </>
    );
}

export default PageNotFound;