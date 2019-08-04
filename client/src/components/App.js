// https://medium.freecodecamp.org/how-to-make-create-react-app-work-with-a-node-backend-api-7c5c48acb1b0

import React, { Component } from 'react';
import './App.css';
import Navbar from './Navbar';
import Calculator from './Calculator';
import LoginPage from './Pages/LoginPage';
import AccountPage from './Pages/RecipePage';
import SignUpPage from './Pages/SignUpPage';
import { UserContext } from './Context/ContextProvider';
import ReactGA from 'react-ga';
import createHistory from 'history/createBrowserHistory';
import { toast, Bounce } from 'react-toastify';
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom';
import { userService } from '../services/user-service';

toast.configure({
	autoClose: 3000,
	transition: Bounce,
	position: "bottom-right",
	hideProgressBar: true,
});

const history = createHistory()
console.log(history);
ReactGA.initialize('UA-144103260-1');
history.listen((location, action) => {
    ReactGA.pageview(location.pathname + location.search);
	console.log('hello')
    console.log(location.pathname)
});

class App extends Component {
	constructor(props) {
		super(props);

		this.login = (username, password) => {
			userService.login(username, password)
			.then(response => response.success ? this.setState({isLoggedIn: true}) : null);
		}

		this.logout = () => {
			userService.logout()
			.then(this.setState({isLoggedIn: false}))
		}

		this.refreshLogin = () => {
			this.setState({isLoggedIn: userService.isLoggedIn()});
		}

		this.state = {
			isLoggedIn: false,
			login: this.login,
			logout: this.logout,
			refreshLogin: this.refreshLogin,
		};
	}

	componentDidMount() {
		this.refreshLogin();
	}

	render() {
		return (
			<UserContext.Provider value={this.state}>
				<Router>
					<div>
						<Navbar />
						<div>
							<Route exact path="/" component={Calculator} />
							<Route path = "/login" component={LoginPage} />
							<Route path = "/create_account" component={SignUpPage} />
							<Route path="/recipes" component={AccountPage} />
							<Route path = "/Calculator/:recipename" component={Calculator} />
						</div>
					</div>
				</Router>
			</UserContext.Provider>
		);
    }
}

export default App;
