function Result(props) {

    const { values, onClick } = props.logic;

    return(
        <>
            <div className="row">
                <div className="col-12">
                    <h1 className="main-color nunito sub-title-2">Resultaat</h1>
                    <p className="under-title">
                        { values.result.prediction['has-not-parodontitis'] > values.result.prediction['has-parodontitis'] &&
                            <>De patient heeft <b>geen</b> parodontitis! ({ values.result.prediction['has-not-parodontitis'] * 100 }%)</>
                        }

                        { values.result.prediction['has-parodontitis'] > values.result.prediction['has-not-parodontitis'] &&
                            <>De patient heeft <b>wel</b> parodontitis! ({ values.result.prediction['has-parodontitis'] * 100 }%)</>
                        }
                    </p>

                    <img className="shap-img" src={"data:image/png;base64, " + values.result['shap-img']} alt="shap"/>

                    <button type="button" className="btn btn-primary btn-upload nunito" onClick={ onClick.reset }>
                        <span>Opnieuw</span><i className="fa-solid fa-arrow-right icon"/>
                    </button>
                </div>
            </div>
        </>
    )
}

export default Result;