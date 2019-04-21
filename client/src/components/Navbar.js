import React, { Component } from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';
import * as routes from '../constants/routes';

class Navbar extends Component {
  render() {
    return (
      <div className="navbar">
        <ul>
          <li><Link to={'/protected'}>Protected Page</Link></li>
          <li><Link to={'/login'}>Sign In</Link></li>
          <li><Link to={'/recipes'}>Recipes</Link></li>
          <li><Link to={'/'}>Home</Link></li>
        </ul>
      </div>
    );
  }
}

export default Navbar;
