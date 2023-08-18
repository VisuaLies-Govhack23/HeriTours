import React from 'react';
import Home from './components/Home';
import TourMap from './components/TourMap';
import { Page, useAppStore } from './model';

export interface AppProps {}

const App: React.FC<AppProps> = ({}) => {
    const page = useAppStore().page;

    // A quick-and-dirty router
    switch (page) {
        case Page.home:
            return <Home />;
        case Page.map:
            return <TourMap />;
    }
};

export default App;
