import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Template from "./pages/_shared/template";

// Error(s)
import PageNotFound from "./pages/_errors/page-not-found";

// Page(s)
import Home from "./pages/home";
import Predict from "./pages/prediction/predict";

function App() {
    return (
        <>
            <Router>
                <Template>
                    <Routes>
                        <Route exact path="/" element={<Home/>}/>
                        <Route exact path="/predict" element={<Predict/>}/>
                        <Route path="*" element={<PageNotFound/>}/>
                    </Routes>
                </Template>
            </Router>
        </>
    );
}

export default App;