import React from "react";
import './App.css';
import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.js';
import NewsPanel from "../NewsPanel/NewsPanel";

export default class App extends React.Component {
    render() {
        return (
            <div>
                <div className='container'>
                    <NewsPanel/>
                </div>
            </div>
        )
    }

}
