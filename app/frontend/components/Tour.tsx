import React from 'react';
import styled from '@emotion/styled';
import { lightGrey } from '../constants';

const Card = styled.div`
    padding: 1rem;
    border: 1px solid ${lightGrey};
    border-radius: 0.5rem;
    margin-bottom: 1rem;
`;

export interface TourProps {
    name: string;
}

const Tour: React.FC<TourProps> = ({ name }) => {
    return <Card>{name}</Card>;
};

export default Tour;
