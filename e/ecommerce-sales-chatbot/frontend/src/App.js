import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import ProductList from './components/ProductList';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={ProductList} />
          <Route path="/chat" component={Chatbot} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;