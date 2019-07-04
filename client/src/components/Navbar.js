import React, { Component } from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';
import * as routes from '../constants/routes';
import { userService } from '../services/user-service';
import { UserContext } from './Context/ContextProvider';

class Navbar extends Component {

  render() {
    console.log(this.context)
    let accountLink = this.context.isLoggedIn ? <Link onClick={this.context.logout}>Log Out</Link> : <Link to={'/account'}>Log In</Link>;
    return (
      <div className="navbar">
        <ul>
          <li>{accountLink}</li>
          {this.context.isLoggedIn ? <li><Link to={'/recipes'}>My Recipes</Link></li> : null}
          <li><Link to={'/'}>Calculator</Link></li>
        </ul>
      </div>
    );
  }
}
Navbar.contextType = UserContext;

export default Navbar;
