import { Link } from "react-router-dom";
import denitist from "./_shared/_images/dentist-with-patient-v2.png";

function Home() {
    return (<>

        <div className="header">
            <div className="container">
                <div className="col-12 col-md-7">
                    <h1>
                        Artificiele intelligentie + <br/>
                        Mondzorg
                    </h1>
                    <p>
                        Door onze ontwikkelde tool is het mogelijk om door middel van AI vroegtijdig de mondaandoening parodontitis te kunnen vaststellen.
                    </p>
                    <Link to="/predict" className="btn btn-primary nunito">
                        <span>Klik hier om te beginnen</span><i className="fa-solid fa-arrow-right icon"/>
                    </Link>
                </div>
            </div>
        </div>
        
        <div className="container">
            <div className="col-12 text-center">
                <h2 className="sub-title">Hoe werkt onze tool?</h2>
                <p>lorem...</p>
            </div>
            <div className="row">
                <div className="col-12 col-md-4 item-feature">
                    <div className="icon-holder">
                        <i className="fa-solid fa-file-invoice icon"></i>
                    </div>
                    <div className="item-feature-name">Elektronisch patiëntendossier</div>
                </div>
                <div className="col-12 col-md-4 item-feature">
                    <div className="icon-holder">
                        <i className="fa-solid fa-microchip icon"></i>
                    </div>
                    <div className="item-feature-name">Artificiele intelligentie</div>
                </div>
                <div className="col-12 col-md-4 item-feature">
                    <div className="icon-holder">
                        <i className="fa-solid fa-magnifying-glass icon"></i>
                    </div>
                    <div className="item-feature-name">Vroegtijdige detectie</div>
                </div>
            </div>
        </div>
    </>);
}

export default Home;