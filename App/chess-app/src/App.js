import './App.css';
import Row from './components/Row.js';

function App() {

  return (
    <div className="App">
      <h1>Challenge Chess Bot</h1>
        <Row row={7} />
        <Row row={6} />
        <Row row={5} />
        <Row row={4} />
        <Row row={3} />
        <Row row={2} />
        <Row row={1} />
        <Row row={0} />
    </div>
  );
}

export default App;
