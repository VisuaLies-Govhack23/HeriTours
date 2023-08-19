import React from 'react';
import styled from '@emotion/styled';
import { search } from 'frontend/model';
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
    const doSearch = (query: string) => {
        search(query);
    };

    return (
        <ScreenColumn>
            <Spinner isDark={true} />
            <Logo />
            <Search onSearch={doSearch} />
            <Header>Popular tours:</Header>
            <Column>
                <Tour name="Victorian Architecture" />
                <Tour name="Georgian Architecture" />
                <Tour name="First Nations" />
                <Tour name="LGBTQIA+ History" />
                <Tour name="Modernist" />
                <Tour name="Brutalist" />
                <Tour name="Federation" />
                <Tour name="Trade and Commerce" />
                <Tour name="Governor Macquarie" />
            </Column>
        </ScreenColumn>
    );
};

export default Home;
