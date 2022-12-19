import {Link} from "react-router-dom";

function Privacy() {
    return (<>
        <div className="header">
            <div className="container">
                <div className="col-12 col-md-7">
                    <h1>
                        Privacy
                    </h1>
                    <p>
                        Benieuwd naar hoe wij de privacy van onze gebruikers waarborgen? Lees hieronder meer over de manier waarop wij dat doen!
                    </p>
                    <span className="badge bg-secondary">
                        <i className="fa-solid fa-shield-halved"></i> De privacy van onze gebruikers staat op de eerste plaats!
                    </span>
                </div>
            </div>
        </div>

        <div className="container">
            <div className="col-12 text-start">
                <h2 className="sub-title-3">Hoe word er om gegaan met uw informatie?</h2>
                <p>
                    Bij het gebruik van onze tool voor het vaststellen van parodontitis maken we uitsluitend gebruik van het Electronisch Patiënten Dossier (EPD) van een patient.
                    Dit EPD, dat door een arts wordt geüpload via onze website, wordt alleen gebruikt om de mondaandoening parodontitis vast te kunnen stellen.
                    We verzamelen geen andere data en delen ook geen informatie met derden.
                    Het EPD wordt na gebruik meteen verwijderd van onze servers.
                    We nemen de privacy van onze gebruikers zeer serieus en zullen altijd zorgvuldig omgaan met hun persoonlijke gegevens.
                </p>
            </div>
            <div className="row">
                <div className="col-12 col-md-4 item-feature">
                    <div className="icon-holder">
                        <i className="fa-solid fa-user icon"></i>
                    </div>
                    <div className="item-feature-name">Gebruikers staan op #1</div>
                </div>
                <div className="col-12 col-md-4 item-feature">
                    <div className="icon-holder">
                        <i className="fa-solid fa-shield-halved icon"></i>
                    </div>
                    <div className="item-feature-name">Privacy waarborging</div>
                </div>
                <div className="col-12 col-md-4 item-feature">
                    <div className="icon-holder">
                        <i className="fa-solid fa-file-invoice icon"></i>
                    </div>
                    <div className="item-feature-name">Elektronisch patiëntendossier</div>
                </div>
            </div>
        </div>
        <div className="container">
            <div className="col-12 text-start">
                <h2 className="sub-title-3">Meer informatie of vragen?</h2>
                <p>
                    Wilt u meer informatie of heeft u vragen? Neem gerust contact met ons op via de mail!
                </p>
                <span className="badge bg-primary mb-4">
                    <i className="fa-solid fa-paper-plane"></i> parodontitis@hotmail.com
                </span>
            </div>
        </div>
    </>);
}

export default Privacy;