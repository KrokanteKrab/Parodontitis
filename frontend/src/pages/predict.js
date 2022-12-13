import { useRef, useState } from "react";

function Predict() {

    const [label, setLabel] = useState("Klik hier om het EPD te uploaden!");
    const [icon, setIcon] = useState("fa-solid fa-arrow-up-from-bracket");

    const [result, setResult] = useState(undefined);

    const inputRef = useRef(null);

    const handleClick = () => {
        // 👇️ open file input box on click of other element
        inputRef.current.click();
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        let formData = new FormData();
        formData.append('patient_xml', inputRef.current.files[0]);

        const requestOptions = {
            // headers: {'Content-Type': 'application/json'},
            method: 'POST',
            body: formData,
        };

        fetch('http://localhost:3000/api/predict/parodontitis', requestOptions)
            .then((response) =>
                response.json())
            .then((data) => {
                console.log(data);
                setResult(data)
            });
    }

    const handleFileChange = (event) => {
        const fileObj = event.target.files && event.target.files[0];
        if (!fileObj) {
            return;
        }

        // 👇️ can still access file object here
        setLabel(fileObj.name);
        setIcon("fa-regular fa-file-lines");
    };

    const reset = () => {
        setResult(undefined);
    }

    return (<>


        <div className="header">
            <div className="container">
                <div className="col-12">
                    <div className="card">


                        { result === undefined &&
                            <form onSubmit={ handleSubmit }>
                                <div className="row">
                                    <div className="col-12">
                                        <h2 className="main-color sub-title-2">Upload een EPD</h2>
                                        <p className="under-title">
                                            Het elektronisch patiëntendossier (EPD) is verplicht om als xml te worden geupload.
                                        </p>

                                        <div className="dropzone" onClick={ handleClick }>
                                            <div className="dropzone-text">
                                                <i className={ icon + " dropzone-icon" }/>
                                                <div className="dropzone-text nunito">{ label }</div>
                                            </div>

                                            <input className="dropzone-input" type="file" accept=".xml" ref={ inputRef } onChange={ handleFileChange }/>
                                        </div>

                                        <button type="submit" className="btn btn-primary btn-upload nunito">
                                            <span>Upload</span><i className="fa-solid fa-arrow-right icon"/>
                                        </button>

                                    </div>
                                </div>
                            </form>
                        }

                        { result !== undefined &&
                            <div className="row">
                                <div className="col-12">
                                    <h1 className="main-color nunito sub-title-2">Resultaat</h1>
                                    <p className="under-title">
                                        { result.prediction['has-not-parodontitis'] > result.prediction['has-parodontitis'] &&
                                            <>De patient heeft <b>geen</b> parodontitis! ({ result.prediction['has-not-parodontitis'] * 100 }%)</>
                                        }

                                        { result.prediction['has-parodontitis'] > result.prediction['has-not-parodontitis'] &&
                                            <>De patient heeft <b>wel</b> parodontitis! ({ result.prediction['has-parodontitis'] * 100 }%)</>
                                        }
                                    </p>

                                    <img className="shap-img" src={"data:image/png;base64, " + result['shap-img']} alt="shap"/>

                                    <button type="button" className="btn btn-primary btn-upload nunito" onClick={ reset }>
                                        <span>Opnieuw</span><i className="fa-solid fa-arrow-right icon"/>
                                    </button>
                                </div>
                            </div>
                        }


                    </div>
                </div>
            </div>
        </div>




    </>);
}

export default Predict;