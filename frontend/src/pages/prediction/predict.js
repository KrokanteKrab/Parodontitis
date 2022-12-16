import PredictLogic from "./predict-logic";
import Loading from "./fragments/loading";
import Form from "./fragments/form";
import Result from "./fragments/result";

function Predict() {

    let { ref, values, onClick, onSubmit, onChange } = new PredictLogic()

    return (<>
        <div className="header">
            <div className="container">
                <div className="col-12">
                    <div className="card">

                        {/* SHOW PREDICTION FORM */}
                        { (values.result === undefined && !values.isLoading) &&
                            <Form logic={{ ref, values, onClick, onSubmit, onChange }} />
                        }

                        {/* SHOW RESULT FROM PREDICTION */}
                        { (values.result !== undefined) &&
                            <Result logic={{ ref, values, onClick, onSubmit, onChange }} />
                        }

                        {/* SHOW LOADING SPINNER */}
                        { (values.isLoading) &&
                            <Loading logic={{ ref, values, onClick, onSubmit, onChange }} />
                        }

                        {/* SHOW LOADING SPINNER */}
                        { (values.isFailed) &&
                            <div className="alert alert-danger" role="alert">
                                Something went wrong!
                            </div>
                        }

                    </div>
                </div>
            </div>
        </div>
    </>);
}

export default Predict;