import React from 'react';
import Details from './components/Details';
import Home from './components/Home';
import TourMap from './components/TourMap';
import { Page, useAppStore } from './model';

export interface AppProps {}

const App: React.FC<AppProps> = ({}) => {
    const page = useAppStore(state => state.page);

    // A quick-and-dirty router
    switch (page) {
        case Page.home:
            return <Home />;
        case Page.map:
            return <TourMap />;
        case Page.details:
            return (
                <Details
                    item={{
                        id: 0,
                        name: 'Test Name',
                        address: 'Test Address',
                        latlng: [0, 0],
                        data: {},
                        suburb: 'Test Suburb'
                    }}
                    onClose={() => console.error('nothing to close')}
                />
            );
    }
};

export default App;
