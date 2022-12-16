import {useRef, useState} from "react";

function PredictLogic() {
    // Upload XML file for the prediction
    const fileUploadRef = useRef(null);
    const [label, setLabel] = useState("Klik hier om het EPD te uploaden!");
    const [icon, setIcon] = useState("fa-solid fa-arrow-up-from-bracket");

    // Show loading or failed
    const [isLoading, setIsLoading] = useState(false);
    const [isFailed, setIsFailed] = useState(false);

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

        // Reset isFailed
        setIsFailed(false);

        // Show loading bar
        setIsLoading(true);

        // Get the file so when can include in our prediction request
        let formData = new FormData();
        formData.append('epd_xml', fileUploadRef.current.files[0]);

        const url = `${ process.env.REACT_APP_API_URL }/api/predict`;
        const options = {
            method: 'POST',
            body: formData,
        };

        let result;
        try {
            const response = await fetch(url, options);
            result = await response.json();
        } catch {
            setIsFailed(true);
        }

        setIsLoading(false);
        setResult(result);
    }

    const reset = () => {
        setResult(undefined);
        setLabel("Klik hier om het EPD te uploaden!");
        setIcon("fa-solid fa-arrow-up-from-bracket");
    }

    const enableShapImg = async (event) => {
        const index = event.currentTarget.dataset.index;

        let copy;
        copy = { ...result };
        copy['predictions'][index]['show-shap'] = 1;
        setResult(copy);

        const url = `${ process.env.REACT_APP_API_URL }/api/shap-img`;
        const options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ...result.predictions[index].values })
        };

        let res;
        try {
            const response = await fetch(url, options);
            res = await response.json();
        } catch {
            setIsFailed(true);
        }

        copy = { ...result };
        copy['predictions'][index]['show-shap'] = res['shap-img'];

        setResult(copy);
    }

    return {
        ref: {
            fileUpload: fileUploadRef
        },
        values: {
            label,
            icon,
            result,
            isLoading,
            isFailed
        },
        onClick: {
            fileUpload,
            reset,
            enableShapImg
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