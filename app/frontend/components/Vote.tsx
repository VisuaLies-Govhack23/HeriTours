import React, { useState } from 'react';
import styled from '@emotion/styled';
import { dark, darkGrey, primary } from 'frontend/constants';
import { MdStar, MdStarOutline } from 'react-icons/md';

const VoteBox = styled.div`
    display: flex;
    flex-direction: row;
    padding: 1rem;
`;

const StarBox = styled.div<{ hover: boolean; active: boolean }>`
    flex: 1;
    svg {
        color: ${props => (props.hover ? primary : props.active ? dark : darkGrey)};
        height: 2rem;
        width: 2rem;
    }
`;

interface StarProps {
    value: number;
    rank: number;
    hover: boolean;
    onEnter(): void;
    onClick(): void;
}

const Star: React.FC<StarProps> = ({ value, rank, hover, onEnter, onClick }) => {
    return (
        <StarBox onMouseEnter={onEnter} hover={value >= rank && hover} active={value >= rank} onClick={onClick}>
            {value >= rank ? <MdStar /> : <MdStarOutline />}
        </StarBox>
    );
};

export interface VoteProps {
    value: number;
    onChange(value: number): void;
}

const Vote: React.FC<VoteProps> = ({ value, onChange }) => {
    const [override, setOverride] = useState(0);

    const makeEnter = (value: number) => {
        return () => setOverride(value);
    };

    const makeClick = (value: number) => {
        return () => {
            onChange(value);
        };
    };

    const doLeave = () => {
        setOverride(-1);
    };

    const view = override < 0 ? value : override;

    return (
        <>
            <VoteBox onMouseLeave={doLeave}>
                <Star value={view} rank={1} onEnter={makeEnter(1)} onClick={makeClick(1)} hover={override > 0} />
                <Star value={view} rank={2} onEnter={makeEnter(2)} onClick={makeClick(2)} hover={override > 0} />
                <Star value={view} rank={3} onEnter={makeEnter(3)} onClick={makeClick(3)} hover={override > 0} />
                <Star value={view} rank={4} onEnter={makeEnter(4)} onClick={makeClick(4)} hover={override > 0} />
                <Star value={view} rank={5} onEnter={makeEnter(5)} onClick={makeClick(5)} hover={override > 0} />
            </VoteBox>
        </>
    );
};

export default Vote;
