import {useRef, useState} from "react";
import env from "react-dotenv";

function PredictLogic() {
    // Upload XML file for the prediction
    const fileUploadRef = useRef(null);
    const [label, setLabel] = useState("Klik hier om het EPD te uploaden!");
    const [icon, setIcon] = useState("fa-solid fa-arrow-up-from-bracket");

    // Result from prediction
    const [result, setResult] = useState(undefined);

    // We use this to open the hidden file upload input
    const fileUpload = () => {
        fileUploadRef.current.click();
    };

    // Handles the file change
    const fileChange = (event) => {
        const fileObj = event.target.files && event.target.files[0];
        if (!fileObj) return;

        // When the file change, the label and icon also need to be updated
        setLabel(fileObj.name);
        setIcon("fa-regular fa-file-lines");
    };

    // Handles when the form is submitted, so we can make the prediction(s)
    const predict = async (event) => {
        // The form has default behavior that we don't need
        event.preventDefault();

        // Get the file so when can include in our prediction request
        let formData = new FormData();
        formData.append('patient_xml', fileUploadRef.current.files[0]);

        const url = `${ env.API_URL }/api/predict/parodontitis`;
        const options = {
            method: 'POST',
            body: formData,
        };

        const response = await fetch(url, options);
        const result = await response.json();

        setResult(result);
    }

    const reset = () => {
        setResult(undefined);
    }

    return {
        ref: {
            fileUpload: fileUploadRef
        },
        values: {
            label,
            icon,
            result
        },
        onClick: {
            fileUpload,
            reset
        },
        onSubmit: {
            predict
        },
        onChange: {
            fileChange
        }
    }
}

export default PredictLogic;