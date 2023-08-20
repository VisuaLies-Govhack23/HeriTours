import React from 'react';
import styled from '@emotion/styled';
import { search, useAppStore } from '../model';
import Logo from './Logo';
import Search from './Search';
import Spinner from './Spinner';
import Tour from './Tour';

const ScreenColumn = styled.div`
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: stretch;
`;

const Column = styled.div`
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    padding: 0.5rem;
    overflow-y: scroll;
`;

const Header = styled.h2`
    font-size: 1rem;
    font-weight: normal;
    padding: 0.5rem;
    margin: 1rem 0 0.5rem 0;
`;

export interface HomeProps {}

const Home: React.FC<HomeProps> = ({}) => {
    const nearby = useAppStore(state => state.nearest);

    const doSearch = (query: string) => {
        void search(query);
    };

    const makeSearch = (query: string, title: string) => {
        return () => void search(query, title);
    };

    return (
        <ScreenColumn>
            <Spinner isDark={true} />
            <Logo />
            <Header>To create an instant tour, enter a search:</Header>
            <Search onSearch={doSearch} />
            <Header>Or choose from a popular search:</Header>
            <Column>
                <Tour
                    name="Local Surprises"
                    subtitle={nearby?.question && `Near you: ${nearby.question}`}
                    onClick={makeSearch('', 'Local Surprises Tour')}
                />
                <Tour name="Victorian Architecture" onClick={makeSearch('victorian', 'Victorian Architecture')} />
                <Tour name="Georgian Architecture" onClick={makeSearch('georgian', 'Georgian Architecture')} />
                <Tour name="Indigenous History" onClick={makeSearch('aboriginal', 'Indigenous History')} />
                <Tour name="LGBTQIA+ History" onClick={makeSearch('homosexual', 'LGBTQIA+ History')} />
                <Tour name="Mid-Century Modern" onClick={makeSearch('mid-century modern', 'Mid-Century Modern Tour')} />
                <Tour name="Brutalist Architecture" onClick={makeSearch('brutalist', 'Brutalist Architecture')} />
                <Tour
                    name="Federation Architecture"
                    onClick={makeSearch('federation-style', 'Federation Architecture')}
                />
                <Tour name="Trade and Commerce" onClick={makeSearch('trade', 'Trade and Commerce')} />
                <Tour name="Governor Macquarie" onClick={makeSearch('governor macquarie', 'Governor Macquarie')} />
            </Column>
        </ScreenColumn>
    );
};

export default Home;
