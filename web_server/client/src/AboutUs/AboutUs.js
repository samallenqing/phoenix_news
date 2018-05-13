import {Link} from "react-router";
import React from 'react';

export default class AboutUs extends React.Component {
    render() {
        return (
            <div>
                <h1>This is a smart news website, it show what you want!</h1>
                <br/>
                <button><Link to='/'>Go Back</Link></button>
            </div>
        )
    }
}