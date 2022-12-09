import denitist from "./_shared/_images/dentist-with-patient-v2.png";

function Home() {
    return (<>

        <div className="row">
            <div className="col-12 col-md-7">
                <h1 className="main-color nunito title">Vroegdetectie van mondaandoeningen</h1>
                <p className="under-title">
                    Het doel van deze tool is om vroegtijdig de mondaandoening parodontitis te kunnen voorspellen op
                    basis van data uit het elektronisch patiëntendossier (EPD).
                    Hierbij wordt gebruik gemaakt van machine learning.
                </p>
                <button type="button" className="btn btn-primary nunito">
                    Ga naar de tool <i className="fa-solid fa-arrow-right"/>
                </button>
            </div>
            <div className="col-12 col-md-5">
                <img src={denitist} alt="" height="75%"/>
            </div>
        </div>

    </>);
}

export default Home;