import React from 'react';
import styled from '@emotion/styled';
import { lightGrey } from '../constants';

const Card = styled.div`
    padding: 1rem;
    border: 1px solid ${lightGrey};
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    cursor: pointer;
`;

const Subtitle = styled.div`
    font-size: 0.8rem;
`;

export interface TourProps {
    name: string;
    subtitle?: string | null;
    onClick(): void;
}

const Tour: React.FC<TourProps> = ({ name, subtitle, onClick }) => {
    return (
        <Card onClick={onClick}>
            {name}
            {subtitle && <Subtitle>{subtitle}</Subtitle>}
        </Card>
    );
};

export default Tour;
