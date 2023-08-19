import React from 'react';
import styled from '@emotion/styled';
import confetti from 'canvas-confetti';

const Question = styled.div`
    display: flex;
    flex-direction: column;
    padding: 1rem;
`;

const Text = styled.div`
    text-align: center;
`;

const Row = styled.div`
    display: flex;
    flex-direction: row;
`;

const Answer = styled.button``;

export interface QuestionBoxProps {}

const QuestionBox: React.FC<QuestionBoxProps> = ({}) => {
    const doSubmit = () => {
        void confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    };

    return (
        <Question>
            <Text>Is there a car here?</Text>
            <Row>
                <Answer onClick={doSubmit}>Yes</Answer>
                <Answer onClick={doSubmit}>No</Answer>
                <Answer onClick={doSubmit}>Not Sure</Answer>
            </Row>
        </Question>
    );
};

export default QuestionBox;
