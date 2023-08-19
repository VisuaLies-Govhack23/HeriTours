import React, { useState } from 'react';
import styled from '@emotion/styled';
import confetti from 'canvas-confetti';
import { darkGrey, light, primary } from '../constants';
import { QuestionData } from '../types';

const Question = styled.div`
    display: flex;
    flex-direction: column;
    padding: 1rem;
`;

const Note = styled.div`
    font-size: 0.8rem;
    text-align: center;
`;

const Text = styled.div`
    text-align: center;
`;

const Row = styled.div`
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    justify-content: center;
    margin: 1rem;
`;

const Answer = styled.button`
    background-color: ${primary};
    border: none;
    border-radius: 0.5rem;
    padding: 1rem;
    margin: 0.25rem 0.25rem;
    min-width: 5rem;
    text-align: center;
    font-weight: 900;
    color: ${light};
    &:hover {
        background-color: ${darkGrey};
    }
`;

export interface QuestionBoxProps {
    questions: QuestionData[];
    answered: string[];
    onAnswer(questionId: string, answerId: string): void;
}

let idGenerator = 0;

const QuestionBox: React.FC<QuestionBoxProps> = ({ questions, answered, onAnswer }) => {
    const [skipped, setSkipped] = useState<string[]>([]);
    const nextQuestion = questions.find(question => !answered.includes(question.id) && !skipped.includes(question.id));

    if (!nextQuestion) {
        return (
            <Question>
                <Text>You've answered all our questions. Thanks!</Text>
            </Question>
        );
    }

    const doSubmit = (questionId: string, answerId: string) => {
        onAnswer(questionId, answerId);

        // Skip the question locally so the user doesn't need to wait for the server
        setSkipped([...skipped, questionId]);

        void confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    };

    const doSkip = (questionId: string) => {
        setSkipped([...skipped, questionId]);
    };

    return (
        <Question>
            <Text>{nextQuestion.question}</Text>
            <Row>
                {nextQuestion.answers.map(answer => (
                    <Answer key={idGenerator++} onClick={() => doSubmit(nextQuestion.id, answer.id)}>
                        {answer.answer}
                    </Answer>
                ))}
                <Answer key={idGenerator++} onClick={() => doSkip(nextQuestion.id)}>
                    Skip
                </Answer>
            </Row>
            <Note>(Answer as many questions as you wish)</Note>
        </Question>
    );
};

export default QuestionBox;
