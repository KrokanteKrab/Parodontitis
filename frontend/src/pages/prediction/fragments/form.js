function Form(props) {

    const { ref, values, onClick, onSubmit, onChange } = props.logic;

    return(
        <>
            <form onSubmit={ onSubmit.predict }>
                <div className="row">
                    <div className="col-12">
                        <h2 className="main-color sub-title-2">Upload een EPD</h2>
                        <p className="under-title">
                            Het elektronisch patiëntendossier (EPD) is verplicht om als xml te worden geupload.
                        </p>

                        <div className="dropzone" onClick={ onClick.fileUpload }>
                            <div className="dropzone-text">
                                <i className={ values.icon + " dropzone-icon" }/>
                                <div className="dropzone-text nunito">{ values.label }</div>
                            </div>

                            <input className="dropzone-input" type="file" accept=".xml" ref={ ref.fileUpload } onChange={ onChange.fileChange }/>
                        </div>

                        <button type="submit" className="btn btn-primary btn-upload nunito">
                            <span>Upload</span><i className="fa-solid fa-arrow-right icon"/>
                        </button>

                    </div>
                </div>
            </form>
        </>
    )
}

export default Form;