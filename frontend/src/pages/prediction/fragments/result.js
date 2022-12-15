function Result(props) {

    const { values, onClick } = props.logic;

    return(
        <>
            <div className="row">
                <div className="col-12">
                    <h1 className="main-color nunito sub-title-2">Resultaat</h1>
                    <div className="under-title">


                        { values.result.predictions.map(function(prediction, index){ return (
                                <div key={ index }>
                                    { prediction['has-not-parodontitis'] > prediction['has-parodontitis'] &&
                                        <>De patient heeft <b>geen</b> parodontitis! ({ prediction['has-not-parodontitis'] * 100 }%)</>
                                    }

                                    { prediction['has-parodontitis'] > prediction['has-not-parodontitis'] &&
                                        <>De patient heeft <b>wel</b> parodontitis! ({ prediction['has-parodontitis'] * 100 }%)</>
                                    }
                                </div>
                        )})}


                    </div>

                    {/*<img className="shap-img" src={"data:image/png;base64, " + values.result['shap-img']} alt="shap"/>*/}

                    <button type="button" className="btn btn-primary btn-upload nunito" onClick={ onClick.reset }>
                        <span>Opnieuw</span><i className="fa-solid fa-arrow-right icon"/>
                    </button>
                </div>
            </div>
        </>
    )
}

export default Result;