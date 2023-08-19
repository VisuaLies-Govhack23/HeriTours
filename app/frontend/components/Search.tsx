import React, { useState } from 'react';
import styled from '@emotion/styled';
import { dark, darkGrey, light, primary } from 'frontend/constants';
import { MdSearch } from 'react-icons/md';

const Row = styled.div`
    display: flex;
    flex-direction: row;
    align-items: stretch;
    padding: 0.5rem;
`;

const Input = styled.input`
    flex: 1;
    margin-right: 0.5rem;
    padding: 1rem;
    border-style: solid;
    border-width: 1px;
    border-radius: 0.5rem;
    border-color: ${dark};
`;

const Button = styled.button`
    background-color: ${primary};
    border: none;
    border-radius: 0.5rem;
    display: flex;
    padding: 0.5rem;
    align-items: center;
    &:hover {
        background-color: ${darkGrey};
    }
    svg {
        height: 2rem;
        width: 2rem;
        color: ${light};
    }
`;

export interface HomeProps {
    onSearch(query: string): void;
}

const Search: React.FC<HomeProps> = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const doSearch = () => {
        onSearch(query);
    };

    return (
        <Row>
            <Input type="text" value={query} onChange={e => setQuery(e.target.value)} />
            <Button onClick={doSearch}>
                <MdSearch />
            </Button>
        </Row>
    );
};

export default Search;
