import { v4 as uuid } from 'uuid';

function Result(props) {

    let { values, onClick } = props.logic;

    return(
        <>
            <div className="row">
                <div className="col-12">
                    <h1 className="main-color nunito sub-title-2">Patient dossier</h1>
                    {/* PATIENT INFO */}
                    <div className="row">
                        <div className="col-auto">

                            <div className="person-profile-img">
                                { values.result.patient['GENDER_MALE'] === 1 &&
                                    <i className="fa-solid fa-person"></i>
                                }

                                { values.result.patient['GENDER_FEMALE'] === 1 &&
                                    <i className="fa-solid fa-person-dress"></i>
                                }
                            </div>
                        </div>
                        <div className="col-auto patient_attribute_holder">

                            <div className="patient_attribute">
                                <i className="fa-solid fa-id-badge"></i> { values.result.patient['PATIENT_ID'] }
                            </div>

                            <div className="patient_attribute">
                                { values.result.patient['GENDER_MALE'] === 1 &&
                                    <>
                                        <i className="fa-solid fa-mars"></i> man
                                    </>
                                }

                                { values.result.patient['GENDER_FEMALE'] === 1 &&
                                    <>
                                        <i className="fa-solid fa-venus"></i> vrouw
                                    </>
                                }
                            </div>

                            <div className="patient_attribute">
                                    <i className="fa-solid fa-cake-candles"></i> { values.result.patient['BIRTH_DATE'] } ({ values.result.patient['AGE'] })
                            </div>
                        </div>
                        <div className="col-12 spacer" />
                    </div>

                    {/* VISIT(S) */}
                    <div className="row">

                        { values.result.predictions.map((prediction, i) =>
                            <div className="col-12 spacer" key={ i }>

                                <div className="row">
                                    <div className="col-auto">
                                        <div className="visit_attribute">
                                            <i className="fa-solid fa-calendar-day"></i> { values.result.visits[i]['VISIT_DATE'] }
                                        </div>
                                    </div>
                                    <div className="col-auto">
                                        <div className="visit_attribute">
                                            <i className="fa-solid fa-user-doctor"></i>

                                            { prediction.values['TREATING_PROVIDER_DENTIST'] === 1 && <>Tandarts</> }
                                            { prediction.values['TREATING_PROVIDER_FACULTY'] === 1 && <>Faculteit</> }
                                            { prediction.values['TREATING_PROVIDER_STUDENT'] === 1 && <>Student</> }

                                        </div>
                                    </div>
                                    <div className="col-auto">
                                        <div className="visit_attribute">
                                            <i className="fa-solid fa-arrow-trend-up"></i>

                                            { prediction.values['AGE_RANGE_20'] === 1 && <>20+</> }
                                            { prediction.values['AGE_RANGE_40'] === 1 && <>40+</> }
                                            { prediction.values['AGE_RANGE_60'] === 1 && <>60+</> }

                                        </div>
                                    </div>

                                </div>

                                <div className="col-12">
                                    <p>
                                        { prediction['has-not-parodontitis'] > prediction['has-parodontitis'] &&
                                            <>De patient heeft <b>geen</b> parodontitis! ({ (prediction['has-not-parodontitis'] * 100).toFixed(2) }%)</>
                                        }

                                        { prediction['has-parodontitis'] > prediction['has-not-parodontitis'] &&
                                            <>De patient heeft <b>wel</b> parodontitis! ({ (prediction['has-parodontitis'] * 100).toFixed(2) }%)</>
                                        }

                                        { prediction['show-shap'] === 0 &&
                                            <small>
                                                <br/><br/>
                                                Klik <b onClick={ onClick.enableShapImg } data-index={ i } >hier</b> voor meer informatie over de voorspelling.
                                            </small>
                                        }
                                        { (prediction['show-shap'] === 1) &&
                                            <small>
                                                <br/><br/>
                                                De uitleg wordt geladen...
                                            </small>
                                        }
                                    </p>



                                    { (prediction['show-shap'] !== 0 && prediction['show-shap'] !== 1) &&
                                       <div>
                                           <img className="shap-img" src={"data:image/png;base64, " + prediction['show-shap']} alt="shap"/>
                                       </div>
                                    }
                                </div>

                            </div>
                        )}


                    </div>

                    <button type="button" className="btn btn-primary btn-upload nunito" onClick={ onClick.reset }>
                        <span>Sluit</span><i className="fa-solid fa-arrow-right icon"/>
                    </button>
                </div>
            </div>
        </>
    )
}

export default Result;