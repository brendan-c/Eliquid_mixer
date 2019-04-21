// https://medium.freecodecamp.org/how-to-make-create-react-app-work-with-a-node-backend-api-7c5c48acb1b0

import React, { Component } from 'react';
import './App.css';
import Navbar from './Navbar';
import Calculator from './Calculator';
import LoginPage from './Pages/LoginPage';
import AccountPage from './Pages/RecipePage';
import ProtectedPage from './Pages/ProtectedPage';

import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom';

class App extends Component {
  render() {
      return (
      <Router>
        <div>
        <Navbar />
        <div>
          <Route exact path="/" component={Calculator} />
          <Route path = "/protected" component={ProtectedPage} />
          <Route path = "/login" component={LoginPage} />
          <Route path="/recipes" component={AccountPage} />
          <Route path = "/Calculator/:recipename" component={Calculator} />

        </div>
        </div>
      </Router>
      );
    }
  }

export default App;