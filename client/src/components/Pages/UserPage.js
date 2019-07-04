import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { userService } from '../../services/user-service.js';
import LoginPage from './LoginPage';
import LogoutPage from './LogoutPage';
import UserContext from '../Context/ContextProvider';

class UserPage extends React.Component {
  render() {
	  if (this.context.isLoggedIn) {
          return <Redirect to="/" />
	  } else {
		  return (
			  <LoginPage />
		  )
	  }
  }
}
UserPage.contextType = UserContext;

export default UserPage;
