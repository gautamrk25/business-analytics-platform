import { Routes, Route } from 'react-router-dom';
import ParamountDataProduct from './components/ParamountDataProduct';
import MeasurePage from './components/MeasurePage';
import Navigation from './components/Navigation';
import ExperiencePage from './components/ExperiencePage';
import PredictPage from './components/PredictPage';
import OptimizePage from './components/OptimizePage';

function App() {
  return (
    <>
      <Navigation />
      <Routes>
        <Route path="/" element={<ParamountDataProduct />} />
        <Route path="/measure" element={<MeasurePage />} />
        <Route path="/predict" element={<PredictPage />} />
        <Route path="/optimize" element={<OptimizePage />} />
      </Routes>
    </>
  );
}

export default App; 