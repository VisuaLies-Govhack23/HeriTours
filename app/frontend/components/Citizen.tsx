import React, { useState } from 'react';
import styled from '@emotion/styled';
import { useAutoAnimate } from '@formkit/auto-animate/react';
import QuestionBox from './QuestionBox';
import Vote from './Vote';

const Column = styled.div`
    display: flex;
    flex-direction: column;
    align-items: stretch;
`;

const Header = styled.h4`
    font-weight: bold;
    font-size: 1rem;
    font-style: normal;
    padding: 0.5rem;
    margin: 1rem 0 0.5rem 0;
`;

const Textarea = styled.textarea`
    height: 5rem;
`;

const Row = styled.div`
    display: flex;
    justify-content: flex-end;
`;

const Button = styled.button``;

export interface CitizenProps {}

const Citizen: React.FC<CitizenProps> = ({}) => {
    const [vote, setVote] = useState(0);
    const [isListening, setListening] = useState(true);
    const [parent] = useAutoAnimate();

    const doSubmitStory = () => {
        setListening(false);
    };

    return (
        <div ref={parent}>
            <Header>Your Vote</Header>
            <Vote value={vote} onChange={setVote} />
            <Header>Help Us, and Earn Points</Header>
            <QuestionBox />
            {isListening && (
                <Column>
                    <Header>Share Your Story</Header>
                    <Textarea />
                    <Row>
                        <Button onClick={doSubmitStory}>Share</Button>
                    </Row>
                </Column>
            )}
            <Header>Community Stories</Header>
        </div>
    );
};

export default Citizen;
