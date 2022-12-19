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

                        <div className="file-upload" onClick={ onClick.fileUpload }>
                            <div className="file-upload-text">
                                <i className={ values.icon + " file-upload-icon" }/>
                                <div>{ values.label }</div>
                            </div>

                            <input className="file-upload-input" type="file" accept=".xml" ref={ ref.fileUpload } onChange={ onChange.fileChange }/>
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