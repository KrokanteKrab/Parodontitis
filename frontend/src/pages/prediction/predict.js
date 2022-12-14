import PredictLogic from "./predict-logic"
import Form from "./fragments/form";
import Result from "./fragments/result";

function Predict() {

    const { ref, values, onClick, onSubmit, onChange } = new PredictLogic()

    return (<>
        <div className="header">
            <div className="container">
                <div className="col-12">
                    <div className="card">

                        {/* SHOW PREDICTION FORM */}
                        { (values.result === undefined) &&
                            <Form logic={{ ref, values, onClick, onSubmit, onChange }} />
                        }

                        {/* SHOW RESULT FROM PREDICTION */}
                        { (values.result !== undefined) &&
                            <Result logic={{ ref, values, onClick, onSubmit, onChange }} />
                        }

                    </div>
                </div>
            </div>
        </div>




    </>);
}

export default Predict;