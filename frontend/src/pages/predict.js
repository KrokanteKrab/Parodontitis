import { useRef, useState } from "react";

function Predict() {

    const [label, setLabel] = useState("Klik hier om het EPD te uploaden!");
    const [icon, setIcon] = useState("fa-solid fa-arrow-up-from-bracket");
    const inputRef = useRef(null);

    const handleClick = () => {
        // 👇️ open file input box on click of other element
        inputRef.current.click();
    };

    const handleFileChange = event => {
        const fileObj = event.target.files && event.target.files[0];
        if (!fileObj) {
            return;
        }

        // 👇️ reset file input
        event.target.value = null;

        // 👇️ can still access file object here
        setLabel(fileObj.name);
        setIcon("fa-regular fa-file-lines");
    };

    return (<>

        <div className="row">
            <div className="col-12">
                <h1 className="main-color nunito title">Upload een EPD</h1>
                <p className="under-title">
                    Het elektronisch patiëntendossier (EPD) is verplicht om als xml te worden geupload.
                </p>

                <div className="dropzone" onClick={ handleClick }>
                    <div className="dropzone-text">
                        <i className={ icon + " dropzone-icon" }/>
                        <div className="dropzone-text nunito">{ label }</div>
                    </div>
                    <input id="dropzone-input" type="file" ref={inputRef} onChange={handleFileChange}/>
                </div>

                <button type="button" className="btn btn-primary nunito">
                    Upload!
                </button>

            </div>
        </div>

    </>);
}

export default Predict;