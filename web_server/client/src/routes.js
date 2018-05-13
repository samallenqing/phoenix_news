import Base from './Base/Base';
import App from './App/App';
import LoginPage from './Login/LoginPage';
import SignUpPage from './SignUp/SignUpPage';
import Auth from './Auth/Auth';
import AboutUs from "./AboutUs/AboutUs";

const routes = {
    component: Base,
    childRoutes: [
        {
            path: '/',
            getComponent: (location, callback) => {
                if (Auth.isUserAuthenticated()) {
                    callback(null, App);
                } else {
                    callback(null, LoginPage);
                }
            }
        },
        {
            path: '/aboutus',
            component: AboutUs
        },

        {
            path: '/login',
            component: LoginPage
        },

        {
            path: '/signup',
            component: SignUpPage
        },

        {
            path: '/logout',
            onEnter: (nextState, replace) => {
                Auth.deauthenticateUser();
                replace('/');
            }
        }
    ]
};

export default routes;