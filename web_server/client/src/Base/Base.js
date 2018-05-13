import Auth from '../Auth/Auth';
import {Link} from 'react-router';
import React from 'react';
import './Base.css';

const Base = ({children}) => (
    <div>
        <nav className="nav-bar indigo lighten-1">
            <div className="nav-wrapper">
                <Link to="/" className="brand-logo">
                    <img className="logoImage" src={require('./favicon.png')}/>
                </Link>
                <ul id="nav-mobile" className="right">
                    {Auth.isUserAuthenticated() ?
                        (<div>
                                <li>{Auth.getEmail()}</li>
                                <li><Link to="/logout">Log out</Link></li>
                                <li><Link to="/aboutus">About Us</Link></li>
                            </div>
                        )
                        :
                        (<div>
                                <li><Link to="/login">Log in</Link></li>
                                <li><Link to="/signup">Sign up</Link></li>
                                <li><Link to="/aboutus">About Us</Link></li>
                            </div>
                        )}
                </ul>
            </div>
        </nav>
        <br/>
        {children}
    </div>
);

export default Base;